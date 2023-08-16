import json
import re
from abc import abstractmethod
from datetime import datetime
from collections.abc import Sequence
from typing import Any
from xia_fields import BaseField, ComplexField
from xia_engine.base import Base, BaseDocument, BaseEmbeddedDocument, BaseExternalField


class EmbeddedDocumentField(BaseField):
    """An embedded document field - with a declared document_type of an Embedded Document.
    """
    db_form = dict
    internal_form = BaseEmbeddedDocument
    display_form = dict

    def __init__(self, document_type, **kwargs):
        if not issubclass(document_type, BaseEmbeddedDocument):
            raise TypeError("Document type must be Embedded Document")
        self.document_type_class = document_type
        super().__init__(**kwargs)

    def get_sample(self):
        return self.document_type_class.get_sample()

    def validate(self, value: Any, runtime_value: Any = None, /):
        if not isinstance(value, self.document_type_class):
            raise TypeError(f"Type should be {self.document_type_class.__name__}")
        value.validate()

    def from_db(self, value: Any, /, decoder: callable = None, engine=None):
        value = value if not decoder else decoder(value)
        return self.document_type_class.from_db(_engine=engine, **value)

    def to_db(self, value: Any, runtime_value: Any = None, /,
              catalog: dict = None, encoder: callable = None, ignore_unknown: bool = False, engine=None):
        value = value.to_db(catalog=catalog, ignore_unknown=ignore_unknown, engine=engine) if value else None
        return value if not encoder else encoder(value)

    def from_display(self, value: Any, runtime_display: Any = None, /):
        if isinstance(value, dict):
            return self.document_type_class.from_display(**value)
        else:
            raise TypeError(f"Embedded Document Type should be dictionary")

    def to_display(self, value: Any, runtime_value: Any = None, /,
                   lazy: bool = True, catalog: dict = None, show_hidden: bool = False, **kwargs):
        if isinstance(value, BaseEmbeddedDocument):
            return value.get_display_data(lazy=lazy, catalog=catalog, show_hidden=show_hidden)
        else:
            return value


class ListRuntime:
    """Run Time of List Field which has member of External Field

    The main purpose is for the lazy load in the case of the field is of type Reference field.
    Only loading the real object, which means using [0] or [field_value].
    """
    def __getitem__(self, key):
        if isinstance(key, int):
            if self.runtime_values[key] is None:
                self.runtime_values[key] = self.field.get_value(self.internal_values[key], acl=self.acl)[1]
            return self.runtime_values[key]
        elif isinstance(key, slice):
            new_runtime = self.__class__(field=self.field, internal_values=self.internal_values[key])
            new_runtime.runtime_values = self.runtime_values[key]
            return new_runtime
        elif isinstance(key, str):
            idx = self.internal_values.index(key)
            self.runtime_values[idx] = self.field.get_value(self.internal_values[idx], acl=self.acl)[1]
            return self.runtime_values[idx]

    def __len__(self):
        return len(self.internal_values)

    def __eq__(self, other):
        if not isinstance(other, ListRuntime):
            return False
        if self.field.__class__ != other.field.__class__:
            return False
        if self.internal_values != other.internal_values:
            return False
        if self.runtime_values.count(None) != other.runtime_values.count(None):
            return False
        return True

    def __init__(self, field: BaseField, internal_values: list, runtime_values: list = None, acl=None):
        self.field = field
        self.internal_values = internal_values
        self.runtime_values = [None for _ in internal_values] if not runtime_values else runtime_values
        self.acl = acl


class ListField(ComplexField):
    """List of basic fields

    """
    def __init__(self, field, min_length=None, max_length=None, **kwargs):
        self.field = field
        if self.field.runtime:
            kwargs["runtime"] = True
        self.field_class = field.__class__
        self.min_length = min_length
        self.max_length = max_length
        if not isinstance(self.field, (BaseField, BaseEmbeddedDocument, BaseDocument)):
            raise ValueError("Could only create a list of field / embedded document / document")
        self.cascade = getattr(field, "cascade", None)
        super().__init__(**kwargs)

    def get_sample(self):
        if self.field.runtime:
            internal_values = [self.field.sample[0]]
            runtime_sample = ListRuntime(field=self.field, internal_values=internal_values)
            runtime_sample.runtime_values = [self.field.sample[1]]
            return internal_values, runtime_sample
        else:
            return [self.field.sample]

    def validate(self, value: Any, runtime_value: Any = None, /):
        if value is None:
            return  # Pass all None value
        if not isinstance(self.field, BaseField):
            raise TypeError(f"List field only accept Base Field as member")
        if self.max_length and len(value) > self.max_length:
            raise ValueError(f"List item > max defined number: {self.max_length}")
        if self.min_length and len(value) < self.min_length:
            raise ValueError(f"List value < max defined number: {self.min_length}")
        if self.field.runtime and runtime_value:
            for item, runtime_value in zip(value, runtime_value):
                self.field.validate(value, runtime_value)
        else:
            for item in value:
                self.field.validate(item)

    def from_db(self, value: Any, /, decoder: callable = None, engine=None):
        if value is None:
            return None
        if decoder is None or decoder == (None, None):
            return [self.field.from_db(item, engine=engine) for item in value]
        result = decoder[0](value) if decoder[0] else value
        return [self.field.from_db(item, decoder=decoder[1], engine=engine) for item in result]

    def to_db(self, value: Any, runtime_value: Any = None, /,
              catalog: dict = None, encoder: callable = None, ignore_unknown: bool = False, engine=None):
        if value is None:
            return None
        if encoder is None or encoder == (None, None):
            return [self.field.to_db(item, catalog=catalog, engine=engine, ignore_unknown=ignore_unknown)
                    for item in value if item is not None]
        result = [self.field.to_db(item, catalog=catalog, encoder=encoder[1], ignore_unknown=ignore_unknown,
                                   engine=engine)
                  for item in value if item is not None]
        return encoder[0](result) if encoder[0] else result

    def from_display(self, value: Any, runtime_display: Any = None, /):
        if value is None:
            return None if not self.field.runtime else (None, None)
        runtime_display = [] if runtime_display is None else runtime_display
        internal_values, runtime_values = [], None
        if self.field.runtime:
            internal_values = [self.field.from_display(item)[0] for item in value]
            runtime_values = ListRuntime(field=self.field, internal_values=internal_values)
            if runtime_display:
                runtime_values.runtime_values = []
                for item, runtime_item in zip(value, runtime_display):
                    internal, runtime = self.field.from_display(item, runtime_item)
                    runtime_values.runtime_values.append(runtime)
        else:
            internal_values = [self.field.from_display(item) for item in value]
        internal_values = None if not internal_values else internal_values
        return internal_values if not self.field.runtime else (internal_values, runtime_values)

    def to_display(self, value: Any, runtime_value: Any = None, /,
                   lazy: bool = True, catalog: dict = None, show_hidden: bool = False, **kwargs):
        if value is None:
            return None if not self.field.runtime else (None, None)
        runtime_value = [] if runtime_value is None else runtime_value
        display_values, detail_values = [], []
        if self.field.runtime and isinstance(runtime_value, ListRuntime):
            for item, runtime_item in zip(value, runtime_value.runtime_values):
                display_value, detail_value = self.field.to_display(item, runtime_item,
                                                                    lazy=lazy, catalog=catalog, show_hidden=show_hidden)
                display_values.append(display_value)
                detail_values.append(detail_value)
        elif self.field.runtime:
            display_values = [self.field.to_display(item, None, lazy=lazy, catalog=catalog, show_hidden=show_hidden)[0]
                              for item in value]
        else:
            display_values = [self.field.to_display(item, None, lazy=lazy, catalog=catalog, show_hidden=show_hidden)
                              for item in value]
        display_values = [] if not display_values else display_values
        detail_values = [None for _ in display_values] if not detail_values else detail_values
        return display_values if not self.field.runtime else (display_values, detail_values)

    def get_value(self, value: Any = None, runtime_value: Any = None, /, acl=None, **kwargs):
        if value is None:
            return None if not self.field.runtime else (None, None)
        if runtime_value and isinstance(runtime_value, ListRuntime):
            return value, runtime_value
        if not self.field.runtime:
            return value
        internal_values, runtime_values = [], []
        for item in value:
            internal_value, runtime_value = self.field.get_value(item, None, acl=acl, **kwargs)
            internal_values.append(internal_value)
            runtime_values.append(runtime_value)
        return internal_values, ListRuntime(
            field=self.field, internal_values=internal_values, runtime_values=runtime_values, acl=acl
        )

    def from_runtime(self, runtime_value: Any, /):
        if runtime_value is None:
            return None
        return [self.field.from_runtime(item) for item in runtime_value]

    def guess_value(self, value: Any = None):
        if value is None:
            return (None, None) if self.field.runtime else None
        internal_value = [self.field.guess_value(item) for item in value]
        if self.field.runtime:
            internal_values = [value[0] for value in internal_value]
            runtime_values = ListRuntime(field=self.field, internal_values=internal_values)
            runtime_values.runtime_values = [value[1] for value in internal_value]
            return internal_values, runtime_values
        else:
            return internal_value


class ExternalField(BaseExternalField):
    """The field mapped to other documents

    Attributes:
        document_type: member document class
        field_map: mapping current field name and external class field name as current: external
        list_length: 0 means don't show as list. list_length > 1 means show as listing with max length = list_length
        dependent: It will trigger two things:
            1. The data validation will check if the external document exists or not.
            2. The external data deletion will fail if it detects it still needs to support another document
    """
    def __init__(self, document_type, field_map: dict, list_length: int = 0, dependent: bool = False, **kwargs):
        if not issubclass(document_type, BaseDocument):
            raise TypeError("External type must be Document")
        self.db_form = type(None)
        self.internal_form = type(None)
        self.display_form = dict
        self.document_type_class = document_type
        self.field_map = field_map
        self.as_list = True if list_length > 0 else False
        self.list_length = list_length
        if self.as_list and dependent:
            raise ValueError("dependant is not compatible with External Document List. Please set list_length to 0")
        self.dependent = dependent
        kwargs["stateful"] = False
        kwargs["runtime"] = True
        super().__init__(**kwargs)

    def validate(self, value: Any, runtime_value: Any = None, /):
        """No need to validate"""

    def guess_value(self, value: Any = None):
        """No need to guess value"""
        return None, None

    def get_sample(self):
        ref_object = self.document_type_class.get_sample()
        if self.as_list:
            return None, [ref_object]
        else:
            return None, ref_object

    def get_value(self, value: Any = None, runtime_value: Any = None, /, acl=None, **kwargs):
        if runtime_value is not None:
            # Data is already present
            return value, runtime_value
        else:
            # Fetch data from database
            internal_data = kwargs.get("internal_data", {})
            batch = kwargs.get("batch", None)
            query_dict = {}
            for k in self.field_map:
                query_key = self.field_map[k]
                query_value = internal_data.get(k, None)
                if query_value is None:
                    return None, None  # Return nothing if one of the query value is not presented
                elif isinstance(query_value, list):
                    query_value = [str(item) for item in query_value]
                else:
                    query_value = str(query_value)
                query_dict[query_key] = query_value
            if self.as_list:
                query_result = list(self.document_type_class.objects(
                    **query_dict, _batch=batch, _limit=self.list_length, _acl=acl
                ))
            else:
                query_result = self.document_type_class.load(**query_dict, _batch=batch, _acl=acl)
            if query_result:
                return None, query_result
            # Return nothing in other cases
            return None, None

    def to_display(self, value: Any, runtime_value: Any = None, /,
                   lazy: bool = True, catalog: dict = None, show_hidden: bool = False, **kwargs):
        if runtime_value is not None:
            if isinstance(runtime_value, list):
                return value, [item.get_display_data(lazy=lazy, catalog=catalog, show_hidden=show_hidden)
                               for item in runtime_value]
            elif isinstance(runtime_value, BaseDocument):
                return value, runtime_value.get_display_data(lazy=lazy, catalog=catalog, show_hidden=show_hidden)
        else:
            how_to_guide = {"_class": self.document_type_class.__name__,
                            "_mode": "lazy",
                            "_lazy": lazy,
                            "_catalog": catalog,
                            "_show_hidden": show_hidden,
                            "_field_map": self.field_map,
                            "_as_list": True if self.list_length > 0 else False}
            return None, how_to_guide
