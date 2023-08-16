from __future__ import annotations

from typing import Union, Type
from functools import lru_cache
from collections import OrderedDict
import uuid
import json
from datetime import datetime
from xia_engine.base import MetaDocument, BaseField
from xia_engine.base import BaseDocument, EmbeddedDocument
from xia_engine.fields import ListField, EmbeddedDocumentField, ExternalField
from xia_engine.engine import RamEngine, BatchEngine, BaseEngine, BaseLogger
from xia_engine.exception import AuthorizationError, AuthenticationError, OutOfScopeError
from xia_engine.exception import NotFoundError, ConflictError, UnprocessableError
from xia_engine.acl import Acl


class InternalEngine(RamEngine):
    """For document update validation usage"""


class SpaceEngine(BatchEngine):
    """For batch space usage

    Comments:
        Only usable when batch is given. Table name is like batch_id-table_name
    """


class DeleteEngine(BatchEngine):
    """For batch delete usage

    Comments:
        Only usable when batch is given. Table name is like batch_id-table_name
    """


class Batch:
    """Batch Operations

    """
    def __init__(self, engine):
        self.id = str(uuid.uuid4())  #: Batch ID
        self.engine = engine  #: Connected Main Engine

        self.originals = {}  # Original Status to be used during the rollback
        self.operations = []  # Target operations
        self.log_contents = []  # Logs to be saved and send

        self.error = False  # Error detected

    def record_original(self, cls: Type[BaseDocument], doc_id: str, content: dict):
        if cls._engine != self.engine:
            raise RuntimeError("Main engine of the document is not the same as the batch's engine")
        if (cls, doc_id) not in self.originals:
            self.originals[(cls, doc_id)] = {"content": content}

    def record_operation(self, op: str, cls: Type[BaseDocument], doc_id: str, content: dict, log=None):
        if cls._engine != self.engine:
            raise RuntimeError("Main engine of the document is not the same as the batch's engine")
        if op == "I":
            cls._space_engine.create(cls, content, doc_id, self.id)
        elif op == "U":
            cls._space_engine.set(cls, doc_id, self.originals[(cls, doc_id)]["content"], self.id)
            cls._space_engine.update(cls, doc_id, self.id, **content)
        elif op == "S":
            cls._space_engine.set(cls, doc_id, content, self.id)
        elif op == "D":
            cls._delete_engine.set(cls, doc_id, content, self.id)
        self.operations.append({"op": op, "cls": cls, "doc_id": doc_id, "content": content})
        if log:
            self.log_contents.append(log)

    def commit(self, clean_on_failed: bool = False):
        """Commit batch

        Args:
            clean_on_failed: Clean the batch even when the batch is failed

        Returns:
            commit result with error message (in the case of errors)
        """
        result, message = self.engine.batch(self.operations, self.originals)
        if result:
            # Save all log when it is successful
            for log_content in self.log_contents:
                log_content.save()
            self.clean()
        elif clean_on_failed:
            self.clean()
        return result, message

    def clean(self):
        class_list = set([klass for klass, doc_id in self.originals] + [Document])  # Document for empty batch cases
        for doc_class in class_list:
            doc_class._space_engine.drop_batch(self.id)
            doc_class._delete_engine.drop_batch(self.id)
        self.originals, self.operations, self.log_contents = {}, [], []


class Document(BaseDocument, metaclass=MetaDocument):
    """Document is an information mapper

    Class Attributes:
        _meta: Define meta level information. Abstract or not, collection name
        _engine: Database Engine to be used
        _key_fields: Table primary keys, will also be the default privilege_keys
        _partition_info = Table Partition Information
        _cluster_fields: Cluster information
        _privilege_keys: How the authorization will be checked by using the keys. Could contain several key set
        _field_groups: Filter the field to display based on ACL

    Acl operation explanations:
        drop: drop - collection level
        save: create if id is None, else write
        delete: delete
        load: read
        update: write

    Relationship with other documents:
        * When cascade mode is on: the modification / delete will also impact in the cascaded document
    """
    _meta = {"abstract": True}
    _domain_name: str = None  #: Data Domain Name
    _description = ""

    _engine = RamEngine
    _engine_feedback = False  #: Engine could help to fill the document

    _supporting = {}  #: Possible have some documents depend on this document

    _space_engine: BatchEngine = SpaceEngine  #: Store user isolation level insert / update for batch / transaction
    _delete_engine: BatchEngine = DeleteEngine  #: Store user isolation level deleted data for batch / transaction

    _logger: BaseLogger = None  #: Log changes made to engine
    _logger_name: str = None  #: Logger Name of the current data model
    _log_content = False  #: Generate data content (work when _logger is not none)

    _listener_is_active: bool = False  #: There is an active listener to receive real time object changes
    _read_cache = None  # An engine which holds the read cache
    _search_engine = None  # An engine which could handle the search tasks
    _direct_search = []  # The field set in the list will be searched directly by main engine

    _replicas: dict = {}  #: Replicas will save part of data

    _cluster_fields = []
    _partition_info = {}
    _privilege_keys = {}
    _field_groups = {}

    def __hash__(self):
        # There is still a very little chance of collision but hash code by its definition has collection probability
        doc_id = self.get_id()
        if not doc_id:
            raise RuntimeError(f"Document ID missing for calculating hash code")
        version_code = self.get_version(doc_id)
        return str([version_code, id(self)]).__hash__()

    @classmethod
    def purge_version_table(cls):
        """Purge version table

        """
        cls._version_table = OrderedDict()

    @classmethod
    def get_version(cls, doc_id: str) -> str:
        """Get a version code (uuid) for the given object

        Args:
            doc_id (str): Document ID

        Returns:
            UUID as version code
        """
        if not doc_id:
            raise RuntimeError(f"Document ID missing for calculating version code")
        if cls._version_table_size == 0:  # Always give a random version code
            return str(uuid.uuid4())
        if doc_id not in cls._version_table:
            if len(cls._version_table) >= cls._version_table_size:
                cls._version_table.popitem(last=False)
            cls._version_table[doc_id] = str(uuid.uuid4())
        cls._version_table.move_to_end(doc_id)
        # print("get", cls.__name__, doc_id, cls._version_table[doc_id], len(cls._version_table))
        return cls._version_table[doc_id]

    @classmethod
    def set_version(cls, doc_id: str, version_code: str = None):
        """Set a different version code (uuid) for the given object

        Args:
            doc_id (str): Document ID
            version_code (str): Version Code to be set. A new UUID if code is not given

        Returns:
            UUID as version code
        """
        if not doc_id:
            raise RuntimeError(f"Document ID missing for calculating version code")
        if cls._version_table_size == 0:
            # Version table is disabled
            return str(uuid.uuid4())
        version_code = version_code if version_code else str(uuid.uuid4())
        if doc_id not in cls._version_table and len(cls._version_table) >= cls._version_table_size:
            cls._version_table.popitem(last=False)
        cls._version_table[doc_id] = version_code
        cls._version_table.move_to_end(doc_id)
        # print("set", cls.__name__, doc_id, cls._version_table[doc_id], len(cls._version_table))
        if cls._read_cache:  # Remove the entry from read cache
            cls._read_cache.delete(cls, doc_id)
        return version_code

    @classmethod
    def get_meta_data(cls):
        """Get Meta-data of a table

        Returns:
            Meta data dictionary
        """
        meta_data = {
            "domain_name": cls._domain_name,
            "logger_name": cls._logger_name,
            "log_content": cls._log_content,
            "collection_name": cls.get_collection_name(cls._engine),
            "description": cls._description if cls._description else cls.__name__,
            "key_fields": cls._key_fields,
            "unique_lists": cls._uniques,
            "cluster_fields": cls._cluster_fields,
            "partition_info": cls._partition_info,
        }
        meta_data.update(cls._meta)
        return meta_data

    @classmethod
    def set_meta_data(cls, **kwargs):
        """Set Meta-data of a table

        Returns:
            None
        """
        if "domain_name" in kwargs:
            cls._domain_name = kwargs.pop("domain_name")
        if "logger_name" in kwargs:
            cls._logger_name = kwargs.pop("logger_name")
        if "log_content" in kwargs:
            cls._log_content = kwargs.pop("log_content")
        if "description" in kwargs:
            cls._description = kwargs.pop("description")
        if "key_fields" in kwargs:
            cls._key_fields = kwargs.pop("key_fields")
        if "cluster_fields" in kwargs:
            cls._cluster_fields = kwargs.pop("cluster_fields")
        if "partition_info" in kwargs:
            cls._partition_info = kwargs.pop("partition_info")
        cls._meta.update(kwargs)

    @classmethod
    def get_replica_engines(cls):
        """Get engines for the keeping replicas

        Returns:
            replica dictionary: db_param: Engine class
        """
        return cls._replicas

    @classmethod
    def set_replica_engine(cls, replica_name: str, replica_engine: Type[BaseEngine]):
        """Set replica engine

        Args:
            replica_name: name of replica
            replica_engine: Replica Engine class
        """
        cls._replicas[replica_name] = replica_engine

    def get_display_data(self, lazy: bool = True, catalog: dict = None, show_hidden: bool = False):
        engine_catalog = self.get_address(self._engine).get("_catalog", {})
        if not catalog and engine_catalog:  # We use engine related catalog when no catalog is given
            catalog = engine_catalog
        return super().get_display_data(lazy=lazy, catalog=catalog, show_hidden=show_hidden)

    @classmethod
    def create_collection(cls, acl: Acl = None):
        """Create the collection

        Hard way to delete the collection. No cascade relation will be considered
        """
        cls.check_acl(acl, "create", None)
        cls._engine.create_collection(cls)

    @classmethod
    def replicate(cls, task_list: list, acl: Acl = None):
        """Replicate documents

        Args:
            task_list:  List of dictionary with the following keys:
                * content: document
                * op: operation type: "I" for insert, "D" for delete, "U" for update, "L" for load
            acl: User Access List

        Returns:
            task_results: List of dictionary with the following keys:
                * id: document id
                * op: operation type: "I" for insert, "D" for delete, "U" for update, "L" for load
                * time: time when data is replicated
                * status: status code of HTTP protocol
        """
        task_results, engine_task_list = [], []
        for task in task_list:
            if task["content"].__class__.__name__ != cls.__name__:
                task_results.append({"id": task["content"].get_id(), "op": task["op"],
                                    "time": datetime.now().timestamp(), "status": 400})
                continue  # Wrong content type
            if task["op"] == "W":
                continue  # Don't treat type "Watch" for engine
            elif task["op"] in ("I", "L"):
                check_result = cls.check_acl(acl, "new", task["content"])
            elif task["op"] == "U":
                check_result = cls.check_acl(acl, "write", task["content"])
            elif task["op"] == "D":
                check_result = cls.check_acl(acl, "delete", task["content"], raise_error=False)
            else:
                task_results.append({"id": task["content"].get_id(), "op": task["op"],
                                    "time": datetime.now().timestamp(), "status": 400})
                continue  # Wrong operation type
            if not check_result:
                task_results.append({"id": task["content"].get_id(), "op": task["op"],
                                    "time": datetime.now().timestamp(), "status": 403})
                continue  # Not authorized
            doc_id = task["content"].get_id() if task["content"].get_id() else task["content"].calculate_id()
            engine_task = {"id": doc_id, "content": task["content"].to_db(), "op": task["op"]}
            engine_task_list.append(engine_task)
            engine_task_results = cls._engine.replicate(cls, engine_task_list)
            task_results.extend(engine_task_results)
        return task_results

    @classmethod
    def drop(cls, acl: Acl = None):
        """Drop the collection

        Hard way to delete the collection. No cascade relation will be considered
        """
        cls.check_acl(acl, "drop", None)
        cls._version_table = OrderedDict()
        cls._engine.drop(cls)
        if cls._read_cache:
            cls._read_cache.drop(cls)

    @classmethod
    def backup(cls, location: str = None, data_encode: str = None, data_format: str = None, data_store: str = None,
               acl: Acl = None, **kwargs):
        """Backup data of a model

        Args:
            acl: User Access List
            data_encode (str): Backup Data Code
            data_format (str): Backup Data Format
            data_store (str): Backup Data Store location
            location(str): Data location to e used by data store
            **kwargs: parameter to be passed at engine level
        """
        cls.check_acl(acl, "drop", None)
        cls._engine.backup(cls, location=location, data_encode=data_encode, data_format=data_format,
                           data_store=data_store, **kwargs)

    @classmethod
    def restore(cls, location: str = None, data_encode: str = None, data_format: str = None, data_store: str = None,
                acl: Acl = None, **kwargs):
        """Restore data of a model


        Args:
            acl: User Access List
            data_encode (str): Backup Data Code
            data_format (str): Backup Data Format
            data_store (str): Backup Data Store location
            location(str): Data location to e used by data store
            **kwargs: parameter to be passed at engine level
        """
        cls.check_acl(acl, "drop", None)
        cls._version_table = OrderedDict()
        cls._engine.restore(cls, location=location, data_encode=data_encode, data_format=data_format,
                            data_store=data_store, **kwargs)

    @classmethod
    def delete_all(cls, acl: Acl = None):
        """Delete every instance of this document type"""
        delete_result = []
        for obj in cls.objects():
            delete_result.extend(obj.delete(acl=acl))
        return delete_result

    @classmethod
    def get_field(cls, parent_object, field_path: str) -> Union[BaseField, None]:
        """Get field object from a field path

        Args:
            parent_object: Parent class object
            field_path: field path in format "a.b.c"

        Returns
            The field object
        """
        if not field_path:
            return None  #: Ignore empty input
        path_chain = field_path.split(".")
        try:
            sub_field = object.__getattribute__(parent_object, path_chain[0])
        except AttributeError:
            return None
        if isinstance(sub_field, ListField) and isinstance(sub_field.field, EmbeddedDocumentField):
            sub_doc = sub_field.field.document_type_class.get_sample()
        elif isinstance(sub_field, (EmbeddedDocumentField, ExternalField)):
            sub_doc = sub_field.document_type_class.get_sample()
        else:
            sub_doc = None  # No sub doc
        if len(path_chain) == 1:
            return sub_field
        elif sub_doc:
            return cls.get_field(sub_doc, ".".join(path_chain[1:]))

    @classmethod
    def _catalog_to_list(cls, catalog: dict) -> list:
        """Catalog object to list

        Args:
            catalog: Input Format is like {"field1": None, "field2": {"field3": None}}

        Returns
            Result list: ["field1", "field2.field3"]

        Notes:
            "field1" means "field1.*"
        """
        results =[]
        for key, value in catalog.items():
            if isinstance(value, dict):
                results += [key + "." + item for item in cls._catalog_to_list(value)]
            else:
                results.append(key)
        return results

    @classmethod
    def _get_privilege_keys(cls):
        """Get privilege keys

        Rules:
            key_fields + predefined privilege key sets. If none of them are defined, raise authorization error

        Returns:
            Dictionary of privilege key sets
        """
        privilege_keys = {}
        if cls._key_fields:
            privilege_keys["key"] = cls._key_fields
        if cls._privilege_keys:
            privilege_keys.update(cls._privilege_keys)
        if not privilege_keys:
            raise AuthorizationError(f"Check can't be performed because no privilege key set defined of {cls.__name__}")
        return privilege_keys

    def _get_privilege_values(self):
        """Get privilege values based on privilege keys

        Returns:
            List of privilege values (because we could have multiple authorization key sets)
        """
        result = []
        for key_id, key_set in self._get_privilege_keys().items():
            values = [self.__class__.__name__, key_id]
            for key in key_set:
                value = "*"
                paths = key.split(".")
                for i, path in enumerate(paths):
                    if i == 0:
                        value = self._data.get(path, "*")
                    elif isinstance(value, EmbeddedDocument):
                        value = getattr(value, path, "*")
                    elif isinstance(value, dict):
                        value = value.get(path, "*")
                    else:
                        value = "*"
                values.append(str(value))
            values = "/".join(values)
            if values:
                result.append(values)
        return result

    @classmethod
    def check_update_acl(cls, _acl: Acl, _doc: Document = None, **kwargs):
        """Special ACL check for update. Supporting field group settings

        Args:
            _acl: User Access Control
            _doc: document to be updated
            **kwargs: update parameters

        Returns:
            will raise AuthorizationError when check fails
        """
        if _doc.check_acl(_acl, "write", _doc, False):  # Full Authorization Check
            return
        else:
            if _doc._field_groups:
                v_fields = []
                # it is possible that user has access to part of the fields (field group)
                for group_name, group_fields in _doc._field_groups.items():
                    if _doc.check_acl(_acl, "write." + group_name, _doc, False):
                        v_fields.extend(group_fields)
                update_fields = [key.split("__")[0] for key in kwargs]
                if set(v_fields) > set(update_fields):
                    return
            raise AuthorizationError("User has no write authorization or cannot cover all the fields to be updated")

    @classmethod
    def check_acl(cls, acl: Acl, act: str, doc: Document = None, raise_error: bool = True):
        """Check user authorization

        Args:
            acl: User's ACL List
            doc: Document to be controlled
            act: Action to be performed
            raise_error: Raise Error

        Notes:
            when acl is None => Check is deactivated => User has all authorization
        """
        if not acl:
            return True
        if not acl.content:
            # Empty ACL = No authorization at all
            if raise_error:
                raise AuthorizationError(f"Authorization check failed: Empty ACL")
            else:
                return False
        if doc is None:
            # Collection level authorization
            if acl.check(f"{cls.__name__}/*", act):
                return True
            elif raise_error:
                raise AuthorizationError(f"{cls.__name__} Authorization check failed: {act}-collection")
            else:
                return False
        else:
            # Field level
            if any([acl.check(obj, act) for obj in doc._get_privilege_values()]):
                return True
            elif raise_error:
                # Raise error only if none of check has been passed
                raise AuthorizationError(f"{cls.__name__} Authorization check failed: {act}-"
                                         f"{json.dumps(cls._get_privilege_keys(), ensure_ascii=False)}")
            else:
                return False

    @classmethod
    def check_dependency(cls, old_data: dict, new_data: dict = None, batch: Batch = None):
        """Check if this document supports other document

        Args:
            old_data (dict): Old data to be checked
            new_data (dict): New data to compare
            batch (Batch): Batch data

        Returns:
            Tuple(result, message)
        """
        if cls._engine.engine_foreign_key_check:  # Foreign key check at database level
            return True, ""
        for dependent, field_map in cls._supporting.items():
            query_params = {fn: old_data.get(key, None) for fn, key in field_map.items()}
            if None not in query_params.values():  # No need to check when None is presented in the current document
                new_data = {} if not new_data else new_data
                new_params = {fn: new_data.get(key, None) for fn, key in field_map.items()}
                if new_params != query_params:  # No need to check when New value is the same as the old one
                    for _ in dependent.objects(_batch=batch, **query_params):
                        return False, f"Dependency found at {dependent.__name__} with {query_params.values()}"
        return True, ""

    def _check_unique(self, batch: Batch = None):
        """Check uniqueness of an item

        Args:
            batch: check unique in the context of Batch

        Returns:
            no raise error means check is passed
        """
        for unique_check in self._uniques:
            # Check should be done once per unique list
            check_dict = {k: v for k, v in self._data.items() if k in unique_check}
            if all([not v for _, v in check_dict.items()]):
                continue  # accept duplicated empties
            if not batch:
                for obj in self.objects(_batch=batch, **check_dict):
                    if obj.get_id() != self.get_id():
                        raise ConflictError("Unique condition {} violated".format(unique_check))

    def check_scope(self, scope: list):
        """Check if data match the data scope

        Returns
            no exception raise = test passed
        """
        if scope is None:
            return
        for constraint in scope:
            if not getattr(constraint["val"], self.OPERATORS[constraint["op"]])(getattr(self, constraint["fn"])):
                raise OutOfScopeError(f"Data out of scope for engine {self._engine.__name__}")

    @classmethod
    def _get_document_class_from_field(cls, field: BaseField):
        """If a field is a reference or list of reference or external fields, get the document class of the reference

        Args:
            field: A field object

        Returns:
            field class type. Return None if not found
        """
        if isinstance(field, ExternalField):
            return field.document_type_class

    @classmethod
    def migrate(cls, original_doc: BaseDocument, copy_data: bool = False):
        """Migrate a document from the original one into new one. Mostly used for data migration between engines

        Args:
            original_doc: Original document
            copy_data: The new data will be a copy of old one

        Returns:
            The new document with the original reference

        Notes:
        """
        if not issubclass(cls, original_doc.__class__):
            raise ValueError
        migrated_doc = cls()
        migrated_doc._data = original_doc._data.copy() if copy_data else original_doc
        return migrated_doc

    def lock(self, timeout: int = None, acl: Acl = None):
        """Lock the document for update

        Args:
            timeout: Should wait for this amount of time before go timeout
            acl (Acl): User Acl to be checked
        """
        self.check_acl(acl, "write", self)
        doc_id = self._id if self._id else self.calculate_id()
        return self._engine.lock(self.__class__, doc_id, timeout)

    def unlock(self, acl: Acl = None):
        """Unlock the document for update

        Args:
            acl (Acl): User Acl to be checked
        """
        self.check_acl(acl, "write", self)
        doc_id = self._id if self._id else self.calculate_id()
        return self._engine.unlock(self.__class__, doc_id)

    def _feedback_sync(self):
        feedback_content = self._engine.get(self.__class__, self.get_id())
        self._data = self.__class__.from_db(**feedback_content).get_raw_data()
        self._runtime = {}
        if self._logger:  # Should send updated data to log
            log_content = self._logger.generate_log(self, "U", with_data=self._log_content)
            log_content.save()

    def save(self, *, validate: bool = True, check_unique: bool = True, batch: Batch = None, acl: Acl = None):
        """Save a document to engine

        Args:
            validate (bool): Should the validation to be passed or not
            check_unique (bool): Unique check
            batch (Batch): Batch object
            acl (Acl): User Acl to be checked

        Returns:
            itself (with document id in the case of a new created document)
        """
        engine_params = self.get_address(self._engine)  # Get the engine related setting
        self._batch = batch
        if not self._engine.engine_scope_check:
            self.check_scope(engine_params.get("_scope", []))
        if self._id is None:
            self.check_acl(acl, "new", self)
        else:
            self.check_acl(acl, "write", self)
        if validate:
            self.validate()
        if check_unique and not self._engine.engine_unique_check:
            # Engine might have already implemented unique check process
            self._check_unique(batch=batch)

        saved_doc = self.load(self._id) if self._id else None

        if saved_doc is not None:  # Need to check the dependency
            dep_check, dep_message = self.check_dependency(saved_doc.get_raw_data(), self._data, batch=batch)
            if not dep_check:
                raise RuntimeError(dep_message)
            if batch:  # We must save a copy for the future rollback for batch
                batch.record_original(cls=self.__class__, doc_id=self._id, content=saved_doc.to_db())

        # Save the original document
        db_content = self.to_db(catalog=engine_params.get("_catalog", None))
        if self._id is None or saved_doc is None:
            # It is a new document
            self._id = new_doc_id = self.calculate_id()
            log_content = self._logger.generate_log(self, "I", with_data=self._log_content) if self._logger else None
            if batch:
                batch.record_operation("I", cls=self.__class__, doc_id=new_doc_id, content=db_content, log=log_content)
                return  # In the batch mode, there is no need to return anything
            self._id = self._engine.create(self.__class__, db_content, new_doc_id)
            if self._key_fields and self._id and self._id != new_doc_id:  # Some key fields has been generated
                self._data.update(self.id_to_dict(self._id))
        else:
            # Update document
            log_content = self._logger.generate_log(self, "U", with_data=self._log_content) if self._logger else None
            if batch:
                batch.record_operation("S", cls=self.__class__, doc_id=self._id, content=db_content, log=log_content)
                return  # In the batch mode, there is no need to return anything
            self._engine.set(self.__class__, self._id, db_content)
        if self._read_cache:
            self._read_cache.set(self.__class__, self._id, db_content)
        if self._logger:
            log_content.save()
        # Engine Feedback
        if self._engine_feedback:
            self._feedback_sync()
        return self

    def delete(self, batch: Batch = None, acl: Acl = None):
        """Delete a document

        Args:
            batch (Batch): Batch object
            acl (Acl): User Acl list

        Returns:
            deleted object list with collection name, id, operation result
        """
        self._batch = batch
        # All delete check must use original document
        to_be_deleted = self.load(self.get_id(), _batch=batch)
        if not to_be_deleted:  # Item doesn't find, nothing to do
            return [{"collection": self.get_collection_name(self._engine), "id": self.get_id(), "result": 200}]

        # Check 1: ACL Check
        check_result = self.check_acl(acl, "delete", to_be_deleted, raise_error=False)
        if not check_result:
            return [{"collection": self.get_collection_name(self._engine), "id": self.get_id(), "result": 403}]

        # Check 2: Dependency check
        check_result, check_message = to_be_deleted.check_dependency(to_be_deleted.get_raw_data(), batch=batch)
        if not check_result:
            return [{"collection": self.get_collection_name(self._engine), "id": self.get_id(), "result": 409,
                     "message": check_message}]

        # Perform delete at engine level
        try:
            log_content = self._logger.generate_log(self, "D", with_data=self._log_content) if self._logger else None
            if batch:
                db_content = to_be_deleted.to_db()
                batch.record_original(cls=self.__class__, doc_id=self._id, content=db_content)
                batch.record_operation(op="D", cls=self.__class__, doc_id=self._id, content=db_content, log=log_content)
                return  # In the batch mode, there is no need to return anything
            self._engine.delete(self.__class__, self._id)
        except Exception as e:
            return [{"collection": self.get_collection_name(self._engine), "id": self.get_id(),
                     "result": 500, "message": str(e)}]
        if self._read_cache:
            self._read_cache.delete(self.__class__, self._id)
        if self._logger:
            log_content.save()
        return [{"collection": self.get_collection_name(self._engine), "id": self.get_id(), "result": 200}]

    def reload(self, batch: Batch = None, acl: Acl = None):
        """Reload the document from the engine

        Attributes:
            batch (Batch): Batch object
            acl (Acl): User ACL to be checked

        Returns:
            itself with refreshed data
        """
        self._batch = batch
        new_self = self.load(self._id, _batch=batch, _acl=acl)
        if not new_self:
            # reload an deleted object
            self._data = {}
            self._runtime = {}
            self._id = None
            return self
        self._data = new_self.get_raw_data().copy()
        self._runtime = {}  # Remove all runtime data
        return self

    def update(self, _validate=True, _batch: Batch = None, _acl: Acl = None, **kwargs):
        """ Update existed fields

        Args:3
            _validate (bool): Should the data be validated before update or not
            acl (Acl): User ACL to be checked
            **kwargs: update parameters

        Returns:
            updated document in the form of python object

        Notes:
            Update String Specifications
            * embedded update: a__b means b component of a. a.b means the key's name is a.b
            * operators: key is end with __op__. The following op are supported:
                * __append__: Append an item to array
                * __remove__: Remove an item
                * __delete__: Delete the field

        Notes:
            We need to update the data from all sources
        """
        if not self._id:
            raise UnprocessableError("Only saved document could be updated")

        self._batch = _batch
        # All update check must use original document
        to_be_updated = self.load(self.get_id(), _batch=_batch)
        if not to_be_updated:
            raise UnprocessableError("Only saved document could be updated")

        engine_params = self.get_address(self._engine)  # Get the engine related setting
        self.check_update_acl(_acl, to_be_updated, **kwargs)  # Authorization check, support field set
        # From display value into internal value to construct
        ram_kwargs, engine_kwargs = {}, {}
        catalog_list = self._catalog_to_list(engine_params.get("_catalog", {}))  # Data catalog
        for key, value in kwargs.items():
            # Step 1: Pre-checks
            if key.startswith("_"):
                # ignore case 1: internal fields cannot be loaded
                continue
            field_name, operator = self._engine.parse_update_option(key)
            field = self.get_field(self, field_name)
            if field is None:
                # ignore case 2: don't update unknown fields
                continue
            if not isinstance(field, BaseField) or self._get_document_class_from_field(field):
                # ignore case 3: wrong field type. Referenced field is not supported by using update
                continue
            if catalog_list and all([not (field_name + ".").startswith(catalog + ".") for catalog in catalog_list]):
                # ignore case 4: field is not requested
                continue
            # Step 2: Get Internal value and then convert to DB Value
            field_class = field.field_class if isinstance(field, ListField) else field.__class__
            internal_value = field.guess_value(value)
            ram_kwargs[key] = field.to_db(internal_value)
            engine_kwargs[key] = field.to_db(internal_value, encoder=self._engine.get_encoder(field_class))

        # Check the updated object by using Ram Engine
        check_doc_id = InternalEngine.create(self.__class__, to_be_updated.to_db(), self.get_id())
        check_doc_content = InternalEngine.update(self.__class__, check_doc_id, **ram_kwargs)
        check_doc = self.__class__.from_db(**check_doc_content)
        if self._key_fields and check_doc.calculate_id() != check_doc_id:
            raise ValueError("Update on primary key is not supported. Please delete and recreate explicitly")
        self.check_update_acl(_acl, check_doc, **kwargs)  # Authorization check again for the to be saved document
        InternalEngine.delete(self.__class__, check_doc_id)
        if not self._engine.engine_scope_check:
            check_doc.check_scope(engine_params.get("_scope", []))
        check_doc._id = self._id
        if _validate:
            check_doc.validate()
        check_doc._check_unique(batch=_batch)

        # Need to check the dependency
        dep_check, dep_message = self.check_dependency(self.get_raw_data(), check_doc.get_raw_data(), batch=_batch)
        if not dep_check:
            raise RuntimeError(dep_message)

        # Engine update
        log_content = self._logger.generate_log(check_doc, "U", with_data=self._log_content) if self._logger else None
        if _batch:
            db_content = to_be_updated.to_db()
            _batch.record_original(cls=self.__class__, doc_id=self._id, content=db_content)
            _batch.record_operation(op="U", cls=self.__class__, doc_id=self._id, content=engine_kwargs, log=log_content)
            return  # In the batch mode, there is no need to return anything
        doc_dict = self._engine.update(self.__class__, self._id, **engine_kwargs)
        updated_doc = self.__class__.from_db(**doc_dict)
        if self._logger:
            log_content.save()
        if self._read_cache:
            self._read_cache.set(self.__class__, self._id, db_content=doc_dict)
        self._data, self._runtime = updated_doc.get_raw_data(), {}
        # Engine Feedback
        if self._engine_feedback:
            self._feedback_sync()
        return self

    @classmethod
    def _get_acl_condition(cls, acl=None):
        """From user acl to get acl condition

        Args:
            acl: User Access List

        Returns:
            A search object to apply
        """
        return {}

    @classmethod
    def _scan_query(cls, _batch: Batch = None, _acl_queries: list = None, _limit: int = 1000, **kwargs):
        """Scan the document and get the match entries

        Args:
            _batch (Batch): Batch object
            _acl_queries (list): Queries generated by user's ACL
            _limit (int): Scan shouldn't return more than 1000 items
            **kwargs: Searching criteria

        Algorithm:
            Try to use search cache or read cache if available
        """
        batch_id, space_id_list, delete_id_list = "", [], []  # Save results for Batch operations
        if _batch:
            # Get search results inside a batch context
            batch_id = _batch.id
            delete_id_list = cls._delete_engine.scan(cls, _batch_id=batch_id, **kwargs)
            space_id_list = cls._space_engine.scan(cls, _batch_id=batch_id, **kwargs)
        if cls._search_engine:
            doc_id_list = cls._search_engine.scan(cls, _acl_queries=_acl_queries, _limit=_limit, **kwargs)
        else:
            if not cls._engine.scan_and_fetch:
                raise RuntimeError(f"Engine {cls._engine.__name__} doesn't support document id scan")
            doc_id_list = cls._engine.scan(cls, _acl_queries=_acl_queries, _limit=_limit, **kwargs)
        if delete_id_list or space_id_list:
            doc_id_list = list(set(doc_id_list + space_id_list - delete_id_list))
        return doc_id_list

    @classmethod
    def _search_query(cls, *args, _batch: Batch = None, _acl_queries: list = None, _limit: int = 50, **kwargs):
        """Do the searching job

        Args:
            *args: Document ID List
            _batch (Batch): Batch object
            _acl_queries (list): Queries generated by user's ACL
            **kwargs: Searching criteria

        Algorithm:
            Try to use search cache or read cache if available
        """
        doc_id_list = args
        batch_id, space_id_list, delete_id_list = "", [], []  # Save results for Batch operations
        if _batch:
            # Get search results inside a batch context
            batch_id = _batch.id
            if not args:
                delete_id_list = cls._delete_engine.scan(cls, _batch_id=batch_id, **kwargs)
                space_id_list = cls._space_engine.scan(cls, _batch_id=batch_id, **kwargs)
            else:
                delete_id_list = [d_id for d_id, _ in cls._delete_engine.fetch(cls, batch_id, *doc_id_list)]
                space_id_list = [s_id for s_id, _ in cls._space_engine.fetch(cls, batch_id, *doc_id_list)]
        # Case 1: Searching by criteria
        if not args:
            is_direct_search = (set(kwargs) in cls._direct_search) and kwargs
            if cls._key_fields and set(cls._key_fields) == set(kwargs):
                # Case 1.1: Search by key fields means search by id
                doc_id_list = cls.dict_to_id_list(kwargs)
            elif cls._search_engine and (cls._engine.scan_and_fetch or cls._read_cache) and not is_direct_search:
                # Case 1.2 We have a search engine and the current engine has advantage by separating scan and fetch
                # If the data model has read cache, we considered that it is always good to separate scan and fetch
                doc_id_list = cls._search_engine.scan(cls, _acl_queries=_acl_queries, _limit=_limit, **kwargs)
            else:
                # Case 1.3 Just using the original searching model
                for doc_id in space_id_list:  # Case 1: Return the data in the batch context
                    yield cls._space_engine.get(cls, doc_id, batch_id=batch_id)  # Case 2: Inserted in space context
                for doc_dict in cls._engine.search(cls, *args, _acl_queries=_acl_queries, _limit=_limit, **kwargs):
                    if doc_dict["_id"] in delete_id_list or doc_dict["_id"] in space_id_list:
                        continue  # Case 2: Deleted or data already returned
                    yield doc_dict
                return  # End of iteration

        # Case 2: Searching by id list
        if cls._read_cache:
            # Case 2.1 We will try to use read cache to accelerate
            # Order of doc_id_list should be respected, so let's build an OrderedDict
            result = OrderedDict([(doc_id, {}) for doc_id in doc_id_list])
            # Algo: Attributing {} at first. Cache could return None
            for cached_doc_id, cached_doc in cls._read_cache.fetch(cls, *doc_id_list):
                result[cached_doc_id] = cached_doc
            todo_list = [doc_id for doc_id, v in result.items() if v == {}]
            for normal_doc_id, normal_doc in cls._engine.fetch(cls, *todo_list):
                result[normal_doc_id] = normal_doc
                cls._read_cache.set(cls, normal_doc_id, normal_doc)
            for not_found_doc_id in [doc_id for doc_id, v in result.items() if v == {}]:
                cls._read_cache.set(cls, not_found_doc_id, None)
            result = {k: v for k, v in result.items() if v}.items()  # Not None and Not {}
        else:
            # Case 2.2 No read cache is define, so using the original engine
            result = cls._engine.fetch(cls, *doc_id_list)
        # Generate results with taking consideration of batch
        for doc_id in space_id_list:  # Case 1: Return the data in the batch context
            yield cls._space_engine.get(cls, doc_id, batch_id=batch_id)  # Case 2: Inserted in space context
        for doc_id, doc_dict in result:
            if doc_id in delete_id_list or doc_id in space_id_list:
                continue  # Case 2: Deleted or data already returned
            else:
                yield doc_dict  # Case 3: Normal case

    @classmethod
    def objects(cls, *args, _batch: Batch = None, _acl: Acl = None, _limit: int = 50, _id_only: bool = False, **kwargs):
        """Search documents

        Args:
            _batch (Batch): Batch object
            _acl (Acl): User ACL to be checked
            _limit (int): Limit result entries length
            _id_only (bool): Only return document ids
            **kwargs: Search Configuration

        Returns:
            generator of a found document

        Notes:
            * key, str pair: single value search
            * key, list pair: array_contains_any search
            * embedded search: a__b means b component of a. a.b means the key's name is a.b
            * operators: key is end with __op__. The following op are supported:
                * __eq__: Needn't be added because it is a by default behavior
                * __lt__, __le__, __gt__, __ge__, __ne__: as is supposed by the name
                * __asc__, __desc__: the result will be ordered by the fields
        """
        # Search will take into account subclasses
        for subclass in ([cls] + list(set(cls._get_subclasses()))):
            if issubclass(subclass, BaseDocument):
                meta_data = getattr(subclass, "_meta", None)
                if type(meta_data) is dict and not meta_data.get("abstract", False):
                    acl_queries = [{}]
                    if _acl is not None:
                        acl_queries, message = _acl.get_search_conditions(cls, *args, **kwargs)
                        if acl_queries is None:  # User's ACL cannot cover the searching parameters
                            raise AuthorizationError(message)
                    if not _id_only:
                        for doc_dict in subclass._search_query(*args, _batch=_batch, _acl_queries=acl_queries,
                                                               _limit=_limit, **kwargs):
                            load_doc = subclass.from_db(**doc_dict)
                            load_doc._id = doc_dict["_id"]
                            if not subclass.check_acl(_acl, "read", load_doc, False):
                                if subclass._field_groups:
                                    v_fields = []
                                    # it is possible that user has access to part of the fields (field group)
                                    for group_name, group_fields in subclass._field_groups.items():
                                        if subclass.check_acl(_acl, "read." + group_name, load_doc, False):
                                            v_fields.extend(group_fields)
                                    if v_fields:
                                        # Only keeping the authorized fields
                                        load_doc._data = {k: v for k, v in load_doc._data.items() if k in v_fields}
                                        if any(key_field not in v_fields for key_field in subclass._key_fields):
                                            load_doc._id = None  # Partial output shouldn't contain ID information
                                    else:
                                        # Still no match entries
                                        continue
                                else:
                                    # No authorization or already yield the document
                                    continue
                            yield load_doc
                    else:
                        for doc_id in subclass._scan_query(_batch=_batch, _acl_queries=acl_queries,
                                                           _limit=_limit, **kwargs):
                            yield doc_id

    @classmethod
    def load(cls, *args, _batch: Batch = None, _acl: Acl = None, **kwargs):
        """Load a Document from engine

        Args:
            _batch (Batch): Batch object
            _acl(Acl): User Acl to be checked
            *args: a list document id (should only have one valid)
            **kwargs:

        Returns:
            loaded document instance
        """
        # Should only have one or will raise an error
        active_doc, active_doc_id, active_sub_class = None, None, None
        for subclass in ([cls] + list(set(cls._get_subclasses()))):
            if issubclass(subclass, BaseDocument):
                meta_data = getattr(subclass, "_meta", None)
                if type(meta_data) is dict and not meta_data.get("abstract", False):
                    acl_queries = [{}]
                    if _acl is not None:
                        acl_queries, message = _acl.get_search_conditions(cls, *args, **kwargs)
                        if acl_queries is None:  # User's ACL cannot cover the searching parameters
                            raise AuthorizationError(message)
                    for doc_dict in subclass._search_query(*args, _batch=_batch, _acl_queries=acl_queries, **kwargs):
                        if active_doc_id == doc_dict.get("_id", ""):
                            continue  # Will occur when parent / child class share the same collection
                        if active_doc:
                            raise UnprocessableError(f"Found more than one item of the given criteria")
                        active_doc = doc_dict.copy()
                        active_doc_id = doc_dict.get("_id", "")
                        active_sub_class = subclass
        if active_doc:
            load_doc = active_sub_class.from_db(**active_doc)
            calculated_doc_id = load_doc.calculate_id()
            if calculated_doc_id is not None and active_doc_id and calculated_doc_id != active_doc_id:
                # Document id is not correct, need to migrate the document id into new value
                active_doc_id = active_sub_class._engine.update_doc_id(
                    active_sub_class, active_doc, active_doc_id, calculated_doc_id
                )
                if calculated_doc_id != active_doc_id:
                    raise UnprocessableError(f"Doc ID: {calculated_doc_id} can not be adapted to key field value")
            load_doc._id = active_doc_id
            if active_sub_class.check_acl(_acl, "read", load_doc, False):  # Authorization Check
                load_doc._batch = _batch
                return load_doc
            else:
                if active_sub_class._field_groups:
                    v_fields = []
                    # it is possible that user has access to part of the fields (field group)
                    for group_name, group_fields in active_sub_class._field_groups.items():
                        if active_sub_class.check_acl(_acl, "read." + group_name, load_doc, False):
                            v_fields.extend(group_fields)
                    if v_fields:
                        # Only keeping the authorized fields
                        load_doc._data = {k: v for k, v in load_doc._data.items() if k in v_fields}
                        if any(key_field not in v_fields for key_field in load_doc._key_fields):
                            load_doc._id = None  # Partial key output shouldn't contain ID information
                        load_doc._batch = _batch
                        return load_doc
        else:
            return None

    @classmethod
    @lru_cache(maxsize=1024)
    def get_collection_name(cls, engine: Type[BaseEngine] = None):
        """Get collection name of current class

        Attributes:
            engine: The collection name is engine dependent

        Returns:
            str: collection name
        """
        engine = engine if engine else cls._engine
        engine_related_address = cls.get_address(engine).get("_tables", {}).get(cls.__name__, None)
        if engine_related_address:
            return engine_related_address
        if "collection_name" in cls._meta:
            return cls._meta["collection_name"]
        if cls._meta.get("abstract", False):
            raise TypeError("Abstract document has no collection name")
        for super_class in reversed(list(cls.__mro__)):
            meta_data = getattr(super_class, "_meta", None)
            if type(meta_data) is dict and meta_data.get("collection_name", None):
                return meta_data["collection_name"]
        return cls.__name__

    def action(self, action_name: str, acl=None, payload: dict = None):
        return super().action(action_name=action_name, acl=acl, payload=payload)

    @classmethod
    def analyze(cls, analytic_request: dict, acl=None) -> list:
        """Give analyzing results

        Args:
            analytic_request: analytic request
            acl: User Access Control List

        Returns
            List of dictionary which holds data
        """
        acl_condition = cls._get_acl_condition(acl)
        analyze_model = cls._engine.compile(cls, analytic_request, acl_condition=acl_condition)
        result = cls._engine.analyze(cls, analyze_model)
        return result


