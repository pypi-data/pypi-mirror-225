from __future__ import annotations
from typing import Any, Type, Union
from collections import OrderedDict
import json
import base64
import itertools
from xia_fields import BaseField, ComplexField


class BaseExternalField(ComplexField):
    """External Field Base Defintion"""


class MetaBase(type):
    def __new__(mcs, *args, **kwargs):
        cls = super().__new__(mcs, *args, **kwargs)
        cls._supporting = {}  # Current dependency should be initialized with parent
        cls._all_fields = {}  # All fields should be calculated instead of explicitly assigned
        current_all_fields = {k: v for k, v in args[2].items() if isinstance(v, BaseField)}
        for parent in args[1]:
            if isinstance(parent, MetaBase):
                cls._all_fields.update(parent._all_fields)  # List fields of parent field
                cls._all_fields.update(current_all_fields)
                cls._supporting.update(parent._supporting)  # Should inherit parent's supporting list

        for field in [fn for fn in cls._all_fields.values() if isinstance(fn, BaseExternalField)]:
            if not field.is_list and field.dependent:
                # Updating all subclass to keep the dependent table updated
                for klass in ([field.document_type_class] + list(set(field.document_type_class._get_subclasses()))):
                    klass._supporting[cls] = field.field_map
        return cls


class MetaDocument(MetaBase):
    """It is a python level metaclass which handles advanced class initialization"""
    def __new__(mcs, *args, **kwargs):
        class_kwarg = args[2]
        # Set abstract to False if the class is not explict defined as abstract class
        if "_meta" in class_kwarg:
            if not class_kwarg["_meta"].get("abstract", False):
                class_kwarg["_meta"]["abstract"] = False
        else:  # No _meta defined, so we just set abstract to false for the constructor
            class_kwarg["_meta"] = {"abstract": False}
        cls = super().__new__(mcs, *args, **kwargs)
        # Address if data model should ignore the inheritance
        if "_address" not in class_kwarg:
            cls._address = {}
        # Each document should have its own version table / active status
        cls._version_listener_active = False
        cls._version_table = OrderedDict()
        # Set unique constraints
        cls._uniques = []
        key_fields = cls._key_fields if "_key_fields" in dir(cls) else []
        for key in [fn for fn in dir(cls) if not fn.startswith("_")]:
            field = getattr(cls, key)
            if isinstance(field, BaseField):
                # Action 1: update _uniques list by unique / unique_with attributes
                if field.unique:
                    cls._uniques.append([key])
                elif field.unique_with:
                    cls._uniques.append([key] + field.unique_with)
                # Action 2: Force required if key
                if key in key_fields:
                    field.required = True
                    # Action 3: Key combination is always unique
                    if key == key_fields[0]:
                        cls._uniques.append(key_fields)
        return cls


class MetaEngine(type):
    """It is a python level metaclass which handles advanced class initialization"""
    def __new__(mcs, *args, **kwargs):
        cls = super().__new__(mcs, *args, **kwargs)
        cls._database = {}  # Each engine will have its own connection databases
        return cls


class BaseEngine(metaclass=MetaEngine):
    """Engine Definition

    Attributes:
        * encoders map ('Field.class': 'callable'): Which field type should use which encoder function
        * decoder map ('Field.class': 'callable'): Which field type should use which decoder function
    """
    #: search options
    OPERATORS = {"__lt__": "<", "__le__": "<=", "__gt__": ">", "__ge__": ">=", "__ne__": "!=", "__eq__": "=="}
    ORDER_TYPES = {"__asc__": "asc", "__desc__": "desc"}  #: order options
    UPDATE_TYPES = {"__append__": "append", "__remove__": "remove", "__delete__": "delete"}  #: update options

    encoders = {}  #: Engine specific value encoder
    decoders = {}  #: Engine specific value decoder

    key_required: bool = False  # Document must have primary key predefined to be saved
    support_unknown: bool = True  # Supporting saving unknown fields

    engine_scope_check: bool = False  #: Scope check will be performed at engine level (pass document level check)
    engine_unique_check: bool = False  #: Unique check will be performed at engine level (pass document level check)
    engine_foreign_key_check: bool = False  #: Dependency check will be performed at engine level

    scan_and_fetch: bool = False  #: Possible to separate the search operation into scan and fetch

    store_embedded_as_table: bool = False  #: Store embedded document as separate tables
    engine_param: str = None  #: Engine parameter name
    engine_connector: callable = None  #: Connector function
    engine_db_shared = True  #: if the value is False, each data model will have its own connector by default
    engine_connector_class = None  #: Connector Class use an object to handler parameters
    engine_default_connector_param: dict = {}  #: default connection parameter

    analyzer = None  #: Analytic Compiler
    backup_coder = None  #: Coder to be used to backup / restore
    backup_storer = None  #: Storer to be used to backup / restore

    @classmethod
    def _get_encoder(cls, field: type):
        if field in cls.encoders:
            return cls.encoders[field]
        for klass, encoder in cls.encoders.items():
            if issubclass(field, klass):
                cls.encoders[field] = encoder
                return encoder
        cls.encoders[field] = None
        return None

    @classmethod
    def get_encoder(cls, field: type, inner_field: type = None) -> callable:
        """Get Encoder for a field

        Args:
            field (type): class type of field class
            inner_field (type): class type of inner field (Such qs ListField)

        Returns:
            Encoder function
        """
        if inner_field:
            return cls._get_encoder(field), cls._get_encoder(inner_field)
        else:
            return cls._get_encoder(field)

    @classmethod
    def _get_decoder(cls, field: type) -> callable:
        if field in cls.decoders:
            return cls.decoders[field]
        for klass, decoder in cls.decoders.items():
            if issubclass(field, klass):
                cls.decoders[field] = decoder
                return decoder
        cls.decoders[field] = None
        return None

    @classmethod
    def get_decoder(cls, field: type, inner_field: type = None) -> callable:
        """Get Decoder for a field

        Args:
            field (type): class type of field class
            inner_field (type): class type of inner field (Such qs ListField)

        Returns:
            Decoder function
        """
        if inner_field:
            return cls._get_decoder(field), cls._get_decoder(inner_field)
        else:
            return cls._get_decoder(field)

    @classmethod
    def parse_search_option(cls, key: str):
        """Reference to search method for the specifications

        Args:
            key (str):

        Returns:
            key, operator, order
        """
        field, operator, order = key, cls.OPERATORS.get("__eq__", "=="), None
        for op in cls.OPERATORS:
            if key.endswith(op):
                operator = cls.OPERATORS[op]
                field = key[:-len(op)]
                break
        for order_by in cls.ORDER_TYPES:
            if key.endswith(order_by):
                operator = None
                order = cls.ORDER_TYPES[order_by]
                field = key[:-len(order_by)]
                break
        if "__" in field:
            field = field.replace("__", ".")
        return field, operator, order

    @classmethod
    def parse_update_option(cls, key: str):
        """Reference to update method for the specifications

        Args:
            key (str):

        Returns:
            key, update
        """
        field, operator = key, None
        for update in cls.UPDATE_TYPES:
            if key.endswith(update):
                operator = cls.UPDATE_TYPES[update]
                field = key[:-len(update)]
        if "__" in field:
            field = field.replace("__", ".")
        return field, operator


class BaseAnalyzer:
    """Analytic request translator"""
    @classmethod
    def compile(cls, document_class: Type[BaseDocument], engine: Type[BaseEngine],
                analytic_request: dict, acl_condition=None):
        """Compile the analysis request

        Args:
            document_class (`subclass` of `BaseDocument`): Document definition
            engine: (`subclass` of `BaseEngine`): Engine for which the analytical model should be executed
            analytic_request: analytic request
            acl_condition: Extra where condition given by user acl objects

        Returns:
            A analytic model which could be executed by the engine
        """


class Base(metaclass=MetaBase):
    """Base of the document or embedded document"""
    _meta = {}  #: Meta information.
    _engine = BaseEngine  #: Engine to be used to hold document. MUST be overridden in each implementation
    _actions = {}  #: Authorized actions
    _key_fields = []
    _all_fields = {}  #: All fields dictionary [key, field_obj]

    _version_listener_active = False  #: Listener is active for get real time object change information
    _version_table = None  #: dict[doc_id, version code] => used for lru cache identification and validation
    _version_table_size: int = 1024  #: The maximum hash table entries, default 1024 entries

    # Scope Operator Direction is reversed due to the compare sequence
    OPERATORS = {"==": "__eq__", ">=": "__le__", ">": "__lt__", "<=": "__ge__", "<": "__gt__", "in": "__contains__"}

    def _set_field_internal_value(self, field: BaseField, key: str, value: Any):
        """Set field value from internal value

        Args:
            field (`BaseField`): field configuration
            key (str): key to be set
            value (Any): internal value, could be tuple as (internal_value, runtime_value)
        """
        if field.runtime:
            if isinstance(value, tuple):
                # Case 1: internal value + runtime value assign
                self._data[key] = value[0].copy() if isinstance(value[0], (list, dict)) else value[0]
                self._runtime[key] = value[1].copy() if isinstance(value[1], (list, dict)) else value[1]
            else:
                # Case 2: Only one value is provided, so we should guess
                self._data[key] = field.guess_value(value)[0]
        else:
            # Case 3: Runtime is off so it must be a internal data
            self._data[key] = value.copy() if isinstance(value, (list, dict)) else value

    def __init__(self, **kwargs):
        self._data = {"_unknown": {}}
        self._runtime = {}
        self._batch = None  # Object is under batch context

        for key in self.__dir__():
            field = object.__getattribute__(self, key)
            if not key.startswith("_") and isinstance(field, BaseField) and field.stateful:
                # Step 1: Set default field
                if field.default is not None:
                    self._set_field_internal_value(field, key, field.default)

    def __str__(self):
        return json.dumps(self.get_display_data(), ensure_ascii=False)

    def __getattribute__(self, item):
        field = object.__getattribute__(self, item)
        if isinstance(field, BaseField):
            if field.runtime:
                if field.stateful:
                    # Example: Reference Field
                    self._runtime[item] = field.get_value(self._data.get(item, None),
                                                          self._runtime.get(item, None),
                                                          batch=self._batch,
                                                          acl=self._acl)[1]
                else:
                    # Example: External Field => Need to pass internal data
                    self._runtime[item] = field.get_value(self._data.get(item, None),
                                                          self._runtime.get(item, None),
                                                          batch=self._batch,
                                                          internal_data=self._data,
                                                          acl=self._acl)[1]
                return self._runtime[item]
            return self._data.get(item, None)
        return field

    def __getattr__(self, item):
        return None

    def __setattr__(self, key: str, value):
        try:
            field = object.__getattribute__(self, key)
        except AttributeError:
            object.__setattr__(self, key, value)
            return
        if isinstance(field, BaseField):
            self._set_field_internal_value(field, key, field.guess_value(value))
            return
        object.__setattr__(self, key, value)

    def __eq__(self, other: Base):
        return isinstance(other, Base) and self.get_raw_data() == other.get_raw_data()

    def calculate_id(self) -> Union[str, None]:
        """Calculate document id from current attributes

        Returns:
            Document id as string if having key field defined else None
        """
        if not self._key_fields:
            return None
        values = [getattr(self, k) for k in self._key_fields]
        return base64.urlsafe_b64encode(json.dumps(values, ensure_ascii=False).encode()).decode().rstrip("=")

    @classmethod
    def dict_to_id(cls, key_values: dict) -> str:
        """Calculate document id from key_values

        Args:
            key_values (dict): Key value dictionary

        Returns:
            Document id as string
        """
        if not cls._key_fields:
            raise ValueError(f"Key fields is not defined for the class {cls.__name__}")
        values = [key_values[k] for k in cls._key_fields]
        return base64.urlsafe_b64encode(json.dumps(values, ensure_ascii=False).encode()).decode().rstrip("=")

    @classmethod
    def dict_to_id_list(cls, key_values: dict) -> list:
        """Calculate document id from key_values. Accepting list as value. Output will always be list

        Args:
            key_values (dict): Key value dictionary

        Returns:
            Document id as string
        """
        if not cls._key_fields:
            raise ValueError(f"Key fields is not defined for the class {cls.__name__}")
        new_values = {k: v if isinstance(v, list) else [v] for k, v in key_values.items()}
        key_values_list = [dict(zip(new_values.keys(), combo)) for combo in itertools.product(*new_values.values())]
        return [cls.dict_to_id(value) for value in key_values_list]

    @classmethod
    def id_to_dict(cls, doc_id: str) -> dict:
        """From document id to key

        Args:
            doc_id (str): Document ID

        Returns:
            A dictionary who holds the key fields and the values
        """
        if not cls._key_fields:
            raise ValueError(f"Key fields is not defined for the class {cls.__name__}")
        # Python will remove the useless ending =
        values = json.loads(base64.urlsafe_b64decode((doc_id + "===").encode()))
        return dict(zip(cls._key_fields, values))

    @classmethod
    def get_actions(cls):
        """Get action supported by this document

        Returns:
            dictionary[str: Base]
        """
        return cls._actions

    @classmethod
    def collection_action(cls, action_name, acl=None, payload: dict = None):
        """Doing a collection level action

        Args:
            action_name: The action name
            acl: Access Control List
            payload: Parameters of action

        """
        payload = {} if payload is None else payload
        if action_name in cls._actions:
            action_method = getattr(cls, action_name, None)
            if list(cls._actions.get(action_name, {}).get("in", {})) == ["payload"] and "payload" not in payload:
                # Payload itself is the payload parameter value
                return action_method(_acl=acl, payload=payload)
            else:
                return action_method(_acl=acl, **payload)
        else:
            raise ValueError(f"Action {action_name} is not a public API of object {cls.__name__}")

    def action(self, action_name: str, acl=None, payload: dict = None):
        """Doing an action of a document

        Args:
            action_name: The action name
            acl: Access Control List
            payload: Parameters of action
        """
        payload = {} if payload is None else payload
        if action_name in self._actions:
            action_method = getattr(self, action_name, None)
            if list(self._actions.get(action_name, {}).get("in", {})) == ["payload"] and "payload" not in payload:
                # Payload itself is the payload parameter value
                return action_method(_acl=acl, payload=payload)
            else:
                return action_method(_acl=acl, **payload)
        else:
            raise ValueError(f"Action {action_name} is not a public API of object {self.__class__.__name__}")

    def validate(self):
        """Validate if all of the component of document follows the predefined rules

        Returns
            Always None. No exception raised means the validation passed
        """
        for field_name in [fn for fn in self.__dir__() if not fn.startswith("_")]:
            field_type = object.__getattribute__(self, field_name)
            if isinstance(field_type, BaseField) and field_type.stateful:
                field_value = self._data.get(field_name, None)
                if not field_value and field_type.required:
                    raise ValueError(f"Required field {field_name} can not be empty")
                elif field_value is not None:
                    field_type.validate(field_value)
                if callable(field_type.validation):
                    field_type.validation(field_value)
            elif isinstance(field_type, BaseExternalField) and field_type.dependent and not field_type.is_list:
                should_check = all([self._data.get(ext_fn, None) is not None for ext_fn in field_type.field_map])
                if should_check:  # No need to check if ext dependencies are all none
                    field_value = getattr(self, field_name, None)
                    if field_value is None:
                        raise RuntimeError(f"Dependent check failed on {self.__class__.__name__}/{field_name}")

    @classmethod
    def get_sample(cls):
        """Get a sample document data"""
        payload = {}
        for key in cls.__dict__.keys():
            field = object.__getattribute__(cls, key)
            if not key.startswith("_") and isinstance(field, BaseField):
                payload[key] = field.sample
        first_level_sample = cls(**payload)
        # For inherited class, we must call the method second time to get a full document
        for key in [fn for fn in first_level_sample.__dir__() if not fn.startswith("_")]:
            field = object.__getattribute__(first_level_sample, key)
            if not key.startswith("_") and isinstance(field, BaseField):
                payload[key] = field.sample
        return cls(**payload)

    @classmethod
    def get_all_fields(cls) -> dict:
        """Get All fields of current class
        """
        return cls._all_fields

    def get_raw_data(self):
        """Get Raw data (materialized form of data)

        Returns:
            python dict object
        """
        return self._data.copy()

    def get_runtime_data(self):
        """Get Runtime data (calculated from raw data when runtime is activated)

        Returns:
            python dict object
        """
        runtime_data = {}
        for key in list(set(self._data) | set(self._runtime)):
            if key in self._runtime:
                runtime_data[key] = (self._data.get(key, None), self._runtime[key])
            else:
                runtime_data[key] = self._data[key]
        return runtime_data

    @classmethod
    def _get_field_lazy_status(cls, field_name: str, lazy: bool, catalog: dict) -> bool:
        """ Get lazy status of a field

        Args:
            field_name: field name on catalog
            lazy: global lazy setting
            catalog: Catalog Parameters

        Returns:
            lazy status. True = lazy otherwise False

        Notes:
            * Case 1: when no catalog or field name is given None in the catalog. We use the global lazy setting
            * Case 2: Catalog contains sub category, we will use the global lazy setting to see if we should load it
            * Case 3: Return the value defined in the catalog
        """
        catalog_settings = catalog.get(field_name, None) if isinstance(catalog, dict) else None
        if catalog_settings is None or isinstance(catalog_settings, dict):
            return lazy
        else:
            return bool(catalog_settings)

    def get_display_data(self, lazy: bool = True, catalog: dict = None, show_hidden: bool = False):
        """Get Display data (visualized form of data)

        Args:
            lazy (bool): Left the fields as is if they are not explicitly loaded
            catalog (dict): The catalog of display field in the following format:
                * {field1: false, field2: false, field3: {sub-field1: true, sub-field2: true}}
                * field1, field2 is the top-level normal field
                * field3 is an embedded field/reference field/external field while sub-field1, sub-field2 is its fields
                * True or false will override the lazy setting, none means using lazy settings
            show_hidden (bool): If hidden value should be shown or not

        Returns:
            python dict object

        Notes:
            We will return the detail form if it is possible
        """
        result = {}
        catalog = {} if catalog is None else catalog  # function parameters shouldn't be mutual
        # Standard fields
        for key, internal_value in self._data.items():
            if catalog and key not in catalog:
                continue  # Field is not requested
            field = object.__getattribute__(self, key) if not key.startswith("_") else None
            if isinstance(field, BaseField) and field.hidden and not show_hidden:
                continue  # Field should be hidden
            if isinstance(field, BaseField) and field.stateful:
                if field.runtime:
                    lazy_status = self._get_field_lazy_status(key, lazy, catalog)
                    if not lazy_status and self._runtime.get(key, None) is None:
                        self._runtime[key] = field.get_value(internal_value, None, acl=self._acl)[1]
                    display_value = field.to_display(internal_value, self._runtime.get(key, None),
                                                     lazy=lazy, catalog=catalog.get(key, None), show_hidden=show_hidden)
                    # Will try to display detail information if it is possible
                    if isinstance(display_value[1], list):
                        result[key] = []
                        for i in range(len(display_value[0])):
                            result[key].append(display_value[1][i] if display_value[1][i] else display_value[0][i])
                    else:
                        result[key] = display_value[1] if display_value[1] else display_value[0]
                else:
                    result[key] = field.to_display(internal_value, lazy=lazy, catalog=catalog.get(key, None),
                                                   show_hidden=show_hidden)
            else:
                result[key] = internal_value
        # External fields
        for key in [fn for fn in self.__dir__() if not fn.startswith("_")]:
            if catalog and key not in catalog:
                continue  # Field is not requested
            field = object.__getattribute__(self, key)
            if isinstance(field, BaseField) and not field.stateful:
                lazy_status = self._get_field_lazy_status(key, lazy, catalog)
                if not lazy_status and self._runtime.get(key, None) is None:
                    self._runtime[key] = field.get_value(internal_data=self._data, acl=self._acl)[1]
                if key in self._runtime:
                    result[key] = field.to_display(None, self._runtime[key], lazy=lazy,
                                                   catalog=catalog.get(key, None), show_hidden=show_hidden)[1]
                else:
                    result[key] = field.to_display(None, None, lazy=lazy, catalog=catalog.get(key, None),
                                                   show_hidden=show_hidden)[1]
        if self._id:
            result["_id"] = self._id
        if not self._data.get("_unknown", {}) or catalog:
            # If _unknown doesn't exist or catalog is given, we won't show unknown data
            result.pop("_unknown", None)
        return result

    def to_db(self, *, catalog: dict = None, ignore_unknown: bool = False, engine: Type[BaseEngine] = None):
        """Translate the runtime data into raw data (materialized form of data)

        Args:
            catalog(dict): Data catalog to be parsed
            ignore_unknown (bool): When a field is not defined in the document, should we send it back to the database
            engine: engine to be used for db data conversion

        Returns:
            python dict object
        """
        result = {}
        engine = engine if engine else self._engine
        catalog = {} if catalog is None else catalog  # function parameters shouldn't be mutual
        for key, value in self._data.items():
            if catalog and key not in catalog and key not in self._key_fields:
                continue  # Field is not requested
            field = object.__getattribute__(self, key) if not key.startswith("_") else None
            if isinstance(field, BaseField):
                if field.stateful:
                    if isinstance(field.field, BaseField):  # Inner field exists
                        encoder = engine.get_encoder(field.__class__, field.field.__class__)
                    else:
                        encoder = engine.get_encoder(field.__class__)
                    result[key] = field.to_db(value, catalog=catalog.get(key, None), encoder=encoder,
                                              ignore_unknown=ignore_unknown, engine=engine)
            else:
                result[key] = value
        if self._id:
            result["_id"] = self._id
        unknown_fields = result.pop("_unknown", {})
        if not ignore_unknown and engine.support_unknown:
            for key, value in unknown_fields.items():
                if key not in result:  # We won't override existed fields
                    result[key] = value
        return result

    @classmethod
    def from_db(cls, _engine: Type[BaseEngine] = None, **kwargs):
        """Transform database data to internal data

        Args:
            _engine : engine to be used for convert data
            **kwargs (object): python dict got from system

        Returns:
            python dict object
        """
        engine = _engine if _engine else cls._engine  # using attached engine if no engine is specified
        payload = {}
        for key, value in kwargs.items():
            field = getattr(cls, key, None) if not key.startswith("_") else None
            if isinstance(field, BaseField):
                if field.stateful:
                    if isinstance(field.field, BaseField):  # Inner field exists
                        decoder = engine.get_decoder(field.__class__, field.field.__class__)
                    else:
                        decoder = engine.get_decoder(field.__class__)
                    field_value = field.from_db(value, decoder=decoder, engine=engine)
                    payload[key] = field_value[0] if field.runtime and isinstance(field_value, tuple) else field_value
            else:
                payload[key] = value
        obj = cls(**payload)
        if "_id" in kwargs:
            obj._id = kwargs["_id"]
        return obj

    @classmethod
    def from_display(cls, **kwargs):
        """Transform Display data to internal data

        Args:
            **kwargs (object): display object got from front end

        Returns:
            python dict object
        """
        payload = {}
        for key, value in kwargs.items():
            field = getattr(cls, key, None) if not key.startswith("_") else None
            if isinstance(field, BaseField):
                if field.stateful:
                    payload[key] = field.guess_value(value)
            else:
                payload[key] = value
        return cls(**payload)


class BaseDocument(Base, metaclass=MetaDocument):
    """The abstract definition of a documen

    Attributes:
        _uniques: Auto-calculated unique constraints of table
        _address: Where and which part of the database could be found

    Address Attributes:
        _db: the database id, will be used to separate different data connection of the same data Engine
        _catalog: The target database, only data of the catalog will be operated.
        _scope: The target engine handles only part of data model. Scope has the same syntax as the searching criteria
        _tables: Could be used to overwrite the default table name. {"": collection_name}
        abcd: All attributes not starting with '_' will be passed to engine connector's init method
        _abcd: Other "_" attributes could be used for each engine

    Catalog Object Format:
        Catalog object define the data field to be shown. The catalog is in the following format:
            * {field1: None, field2: None, field3: {sub-field1: None, sub-field2: None}}
            * field1, field2 is the top-level normal field
            * field3 is an embedded field/reference field/external field while sub-field1, sub-field2 is its fields
            * None means all fields

    Scope Object Format:
        Scope object only applies for the top level fields with multiple line following format.
        Condition of each line must be met. Each line has the following format:
            * {"fn": field_name, "op": operator, "val": value}
            * operator could be one of {"==", "<=", "<", ">=", ">", "in"}

    """
    #: If the document is not abstract, the collection_name should be provided
    _meta = {"abstract": True}
    _uniques = []

    @classmethod
    def get_address(cls, engine: Union[Type[BaseEngine], str] = None):
        """Get address for an engine

        Args:
            engine: Engine class or engine parameter name. default value is the engine attached to the document

        Returns:
            Engine related address parameters
        """
        if isinstance(engine, str):
            return cls._address.get(engine, {})
        elif isinstance(engine, type) and issubclass(engine, BaseEngine):
            return cls._address.get(engine.engine_param, {})
        elif not engine:
            return cls._address.get(cls._engine.engine_param, {})
        raise ValueError(f"engine should be type str or BaseEngine, get {type(engine)} instead")

    @classmethod
    def set_address(cls, engine: Union[Type[BaseEngine], str], address_content: dict):
        """Set address parameter for an Engine

        Args:
            engine: Engine class or engine parameter name. default value is the engine attached to the document
            address_content: Content of address
        """
        if isinstance(engine, str):
            cls._address[engine] = address_content
        elif isinstance(engine, type) and issubclass(engine, BaseEngine):
            cls._address[engine.engine_param] = address_content
        else:
            raise ValueError(f"engine should be type str or BaseEngine, get {type(engine)} instead")

    def __init__(self, **kwargs):
        super().__init__()
        # Try to set id
        self._id = kwargs.get("_id", None)
        # Access Control List
        self._acl = kwargs.get("_acl", None)
        # Try to restore unknown values
        new_kwargs = kwargs.get("_unknown", {}).copy()
        new_kwargs.update(kwargs.copy())
        new_kwargs.pop("_unknown", {})
        # Check all defined Fields
        for key, value in new_kwargs.items():
            if key.startswith("_"):
                continue  # internal fields cannot be loaded
            try:
                field = object.__getattribute__(self, key)
            except AttributeError:
                self._data["_unknown"][key] = value
                continue
            if isinstance(field, BaseField):
                self._set_field_internal_value(field, key, value)
            else:
                self._data["_unknown"][key] = value

    def get_id(self):
        """Get document id

        Returns:
            str: Document ID
        """
        return self._id
    
    @classmethod
    def _get_subclasses(cls):
        """Get subclass including the class itself"""
        for subclass in cls.__subclasses__():
            yield from subclass._get_subclasses()
            yield subclass

    @classmethod
    def _get_user_id_from_acl(cls, acl, id_field: str):
        """Extract User ID from User's ACL"""
        for acl_item in acl.content:
            if acl_item.obj.startswith(f"{cls.__name__}/{id_field}/"):
                return acl_item.obj.split("/")[-1]
        return None


class BaseEmbeddedDocument(Base):
    """Abstract definition of an embedded Document
    """
    def __init__(self, **kwargs):
        super().__init__()
        # Try to restore unknown values
        new_kwargs = kwargs.copy()
        new_kwargs.update(new_kwargs.pop("_unknown", {}))
        # Check all defined Fields
        for key, value in new_kwargs.items():
            if key.startswith("_"):
                continue  # internal fields cannot be loaded
            try:
                field = object.__getattribute__(self, key)
            except AttributeError:
                self._data["_unknown"][key] = value
                continue
            if isinstance(field, BaseField):
                self._set_field_internal_value(field, key, value)
            else:
                self._data["_unknown"][key] = value


class EmbeddedDocument(BaseEmbeddedDocument):
    """Embedded Document is attach to a Document.
    """
    @classmethod
    def get_meta_data(cls):
        meta_data = {}
        if getattr(cls, "_table_name", None):
            meta_data["table_name"] = cls._table_name
        if getattr(cls, "_key_fields", None):
            meta_data["key_fields"] = cls._key_fields
        if getattr(cls, "_fields_map", None):
            meta_data["fields_map"] = cls._fields_map
        return meta_data
