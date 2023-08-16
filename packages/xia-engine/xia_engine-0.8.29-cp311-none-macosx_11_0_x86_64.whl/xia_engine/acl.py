from __future__ import annotations
import math
from typing import Type
from itertools import product, permutations
from xia_fields.fields import StringField
from xia_engine.fields import ListField, EmbeddedDocumentField
from xia_engine.base import EmbeddedDocument, BaseDocument
from xia_engine.exception import ServerError


class AclItem(EmbeddedDocument):
    """Access Control List Item

    Attributes:
        obj: object. Should keep hierarchy with "/" like Obj_A/key_set/sub_B/sub_C/...
        act: action. Like new, read, write, delete, drop or action/action_name

    Notes:
        * obj is composed by three parts. Given the example of Obj_A/key_set/sub_B/sub_C/:
            * Object Part: Obj_A. In the most case, it is the Document class's class name
            * Key name Part: Key_set
                * If key name is "key", the privilege is calculated by using primary keys
                * In the other case, the privilege is calculated by using key set defined in _privilege_keys[key_set]
            * Value Part:
                * Value divided by "/". Using * to match an element
                * obj accept variable embraced by {}.
                Like Obj_A/key_set/{user_name}. user_name is filled during the run time.
    """
    ITEM_FILL_LIMIT = 100

    obj: str = StringField()
    act: str = StringField()

    def validate(self):
        """Design Time Validation

        This validation is for removing obvious errors. Could still have errors during the runtime

        """
        if self.obj.count("*") > 1 or self.act.count("*") > 1:
            raise ValueError("Can not have more than 2 wildcard in obj or act")
        if len(self.obj.split("/")) == 2 and not self.obj.endswith("/*"):
            raise ValueError("obj/* is the only allowed pattern when no value is given")
        if len(self.obj.split("/")) == 3 and self.obj.endswith("/*"):
            raise ValueError("obj/key_set/* is the same as obj/*, please use obj/* instead")
        if "*" in self.obj and "*" not in self.obj.split("/"):
            raise ValueError("wildcard * could only replace whole value. /*somthing is not supported")
        for sub_obj in self.obj.split("/"):
            if sub_obj.startswith("{") and sub_obj.endswith("}"):
                sub_key = sub_obj[1:-1]
                if "*" in sub_key:
                    raise ValueError("wildcard * cannot present in variable name")
        for act in self.act.split(","):
            if "*" in act and not act.strip().endswith("*"):
                raise ValueError("act only supports wildcard at the end")

    @classmethod
    def key_match(cls, key1: str, key2: str) -> bool:
        """ Customized match algo, * can be @middle

        Args:
            key1: key to compare
            key2: item from acl content

        Returns:
            object: True if match else False

        Comments:

        """
        if "*" == key2:
            return True
        elif "*" not in key2:
            return True if key1 == key2 else False
        elif key2.startswith("*"):
            return True if key1.endswith(key2[1:]) else False
        elif key2.endswith("*"):
            return True if key1.startswith(key2[:-1]) else False
        else:
            start, end = key2.split("*", 1)
            return True if key1.startswith(start) and key1.endswith(end) else False

    @classmethod
    def act_match(cls, key1: str, key2: str) -> bool:
        """Comparison for act, possible to have several acts seperated by ','

        Args:
            key1: key to compare
            key2: item from acl content

        Returns:
            object: object: True if match else False
        """
        key2_list = key2.split(",")
        return any(cls.key_match(key1, key.strip()) for key in key2_list)

    def acl_match(self, obj: str, act: str):
        return True if self.key_match(obj, self.obj) and self.act_match(act, self.act) else False

    @classmethod
    def key_subtract(cls, key1: str, key2: str):
        """ How to handler the double limitations:

        - '*' - any = any
        - text - any = key_match(text, any) = text or None in the other case
        - 'a*b' - 'x*y' = biggest a and x + '*' + biggest b and y

        Args:
            key1: key to compare
            key2: item from acl content

        Returns:
            object: True if match else False
        """
        if '*' not in key1:
            return key1 if cls.key_match(key1, key2) else None
        if '*' not in key2:
            return key2 if cls.key_match(key2, key1) else None
        k1_1, k1_2 = (' ' + key1 + ' ').split('*')
        k2_1, k2_2 = (' ' + key2 + ' ').split('*')
        k1_1, k1_2, k2_1, k2_2 = k1_1.strip(), k1_2.strip(), k2_1.strip(), k2_2.strip()
        if k1_1.startswith(k2_1) or k2_1.startswith(k1_1):
            k_1 = k1_1 if k1_1.startswith(k2_1) else k2_1
        else:
            return None
        if k1_2.endswith(k2_2) or k2_2.endswith(k1_2):
            k_2 = k1_2 if k1_2.endswith(k2_2) else k2_2
        else:
            return None
        return k_1 + '*' + k_2

    @classmethod
    def act_compact(cls, act_list: list) -> list:
        temp = set([act for act in act_list if act is not None])  # remove None objects and redundant objects
        ignore_table = [act_1 for act_1, act_2 in permutations(temp, 2) if act_1 == cls.key_subtract(act_1, act_2)]
        return [act for act in temp if act not in ignore_table]

    @classmethod
    def act_subtract(cls, key1: str, key2: str):
        key1_list, key2_list = key1.split(","), key2.split(",")
        result = [cls.key_subtract(act_1.strip(), act_2.strip()) for act_1, act_2 in product(key1_list, key2_list)]
        return "*" if "*" in result else ",".join(cls.act_compact(result))

    def get_filled_acl_item(self, profile: dict) -> list:
        profile = {} if not profile else profile
        sub_objs = []
        for sub_obj in self.obj.split("/"):
            if sub_obj.startswith("{") and sub_obj.endswith("}"):
                sub_key = sub_obj[1:-1]
                if sub_key not in profile:
                    # Case 1.1: key word not present in profile so the user has no authorization at all
                    return []
                elif isinstance(profile[sub_key], list):
                    sub_objs.append([str(v) for v in profile[sub_key]])
                else:
                    sub_objs.append([str(profile[sub_key])])
            else:
                sub_objs.append([sub_obj])
        # So we have now a list of list [["Obj_A"], ["Sub_B1", "Sub_B2"], ..]. Do a c-prod and then we are done
        if math.prod([len(sub_obj) for sub_obj in sub_objs]) > self.ITEM_FILL_LIMIT:
            raise ServerError(f"Single dynamic ACL item can't be filled more than {self.ITEM_FILL_LIMIT} entries")
        final_filled_acl = [AclItem(obj="/".join(item), act=self.act) for item in product(*sub_objs)]
        return final_filled_acl

    def __init__(self, **kwargs):
        if "act" in kwargs:
            kwargs["act"] = ",".join([item.strip() for item in kwargs["act"].split(",")])
        super().__init__(**kwargs)

    def __sub__(self, other: AclItem):
        new_obj = self.key_subtract(self.obj, other.obj)
        new_act = self.act_subtract(self.act, other.act)
        return None if not new_obj or not new_act else self.__class__(obj=new_obj, act=new_act)

    def __and__(self, other: AclItem):
        new_obj = self.key_subtract(self.obj, other.obj)
        new_act = self.act_subtract(self.act, other.act)
        return None if not new_obj or not new_act else self.__class__(obj=new_obj, act=new_act)

    def __eq__(self, other: AclItem):
        if other is None:
            return False
        assert isinstance(self.act, str) and isinstance(other.act, str)
        return True if self.obj == other.obj and set(self.act.split(",")) == set(other.act.split(",")) else False


class Acl(EmbeddedDocument):
    """Access Control List

    """
    TOTAL_FILL_LIMIT = 1024

    content: list = ListField(EmbeddedDocumentField(document_type=AclItem), default=[])

    @classmethod
    def acl_compact(cls, acl_list: list) -> list:
        temp = [acl for acl in acl_list if acl is not None]  # Remove None
        ignore_table = [acl_1 for acl_1, acl_2 in permutations(temp, 2) if acl_1 == (acl_1 - acl_2)]
        return [acl for acl in temp if acl not in ignore_table]

    def get_filled_acl(self, profile: dict) -> Acl:
        total_filled_acl = []
        for acl in self.content:
            total_filled_acl.extend(acl.get_filled_acl_item(profile))
        if len(total_filled_acl) > self.TOTAL_FILL_LIMIT:
            raise ServerError(f"Filled ACL has more than {self.TOTAL_FILL_LIMIT} entries")
        return Acl(content=total_filled_acl)

    def _get_search_acl_list(self, document_class: Type[BaseDocument]):
        """Get search related acl lists

        Args:
            document_class: Document class

        Returns:
            List of related acl items (only contains entries cover the class and read scope),
            List of authorized searching fields
        """
        group_names = ["." + gn for gn in document_class._field_groups] + [""]
        acl_list, field_set = [], set()
        for acl_item in self.content:
            match = False
            for group_name in group_names:
                if (acl_item.obj == "*" or acl_item.obj.startswith(f"{document_class.__name__}/")) \
                        and acl_item.act_match("read" + group_name, acl_item.act):
                    if acl_item.obj == "*":
                        match = True
                    else:
                        privilege_keyname = acl_item.obj.split("/")[1]
                        if privilege_keyname not in ["*", "key"] \
                                and privilege_keyname not in document_class._privilege_keys:
                            continue  # Warning: ACL has no effect because it is a wrong key
                        match = True
                    if group_name == "":
                        field_set.add("*")
                    else:
                        field_set |= set(document_class._field_groups[group_name[1:]])
            if match:
                acl_list.append(acl_item)
        # User could always search by using key fields
        field_set = {"*"} if "*" in field_set else (field_set | set(document_class._key_fields))
        return acl_list, field_set

    @classmethod
    def _get_criteria_from_obj(cls, document_class: Type[BaseDocument], obj: str) -> dict:
        """Attention, we don't control document_class here. We suppose that obj match the requested document class

        Args:
            document_class: document class
            obj: obj value of Acl key

        Returns:
            Query presented as dictionary with {key_name: value in internal form}
        """
        segments = obj.split("/")
        if len(segments) < 3:  # Case 1: "*" or "Model/*" pattern, so return empty supplementary query
            return {}
        fields = document_class._key_fields if segments[1] == "key" else document_class._privilege_keys[segments[1]]
        # fill segments with extra *
        segments = segments[2:]
        segments = [elem for elem in segments for _ in range((len(fields) - len(segments) + 1) if elem == '*' else 1)]
        query = {}
        for field_name, display_value in zip(fields, segments):
            if display_value != "*":  # wildcard so remove from query
                field = object.__getattribute__(document_class.get_sample(), field_name)
                query[field_name] = field.from_display(display_value)
        return query

    @classmethod
    def _query_result_contains(cls, query_1: dict, query_2: dict):
        return all(item in query_2.items() for item in query_1.items())

    @classmethod
    def _compact_queries(cls, queries: list):
        """Make queries more compact.

        Args:
            queries: list of dictionary
        """
        filtered_queries = []
        for query in queries:
            for existed_query in filtered_queries.copy():
                if cls._query_result_contains(query, existed_query):
                    filtered_queries.remove(existed_query)
                elif cls._query_result_contains(existed_query, query):
                    break
            else:
                filtered_queries.append(query)
        return filtered_queries

    def get_search_conditions(self, document_class: Type[BaseDocument], *args, **kwargs):
        """Get search condition

        Args:
            document_class:
            **kwargs:

        Returns:
            None means ACL is not compatible with
            message
        """
        search_fields = set([param.split("__")[0] for param in kwargs])
        acl_list, field_set = self._get_search_acl_list(document_class)
        if field_set != {"*"} and bool(search_fields - field_set):
            return None, "User's field level authorization doesn't cover the search criteria"
        queries = [self._get_criteria_from_obj(document_class, acl_item.obj)
                   for acl_item in acl_list if "read" in acl_item.act or acl_item.act == "*"]
        if {} in queries:
            queries = [{}]  # User has wildcard in on of his ACL
        if not kwargs and not args and {} not in queries:
            return None, "User has no authorization to do full scan, please provide at least one search criteria"
        compacted_queries = self._compact_queries(queries)
        return compacted_queries, ""

    def check(self, obj: str, act: str):
        return any([acl_item.acl_match(obj, act) for acl_item in self.content])

    def __sub__(self, other: Acl):
        acl_1 = self.acl_compact(self.content)
        acl_2 = self.acl_compact(other.content)
        temp = [item_1 - item_2 for item_1, item_2 in product(acl_1, acl_2)]
        return self.__class__(content=self.acl_compact(temp))

    def __and__(self, other: Acl):
        acl_1 = self.acl_compact(self.content)
        acl_2 = self.acl_compact(other.content)
        temp = [item_1 & item_2 for item_1, item_2 in product(acl_1, acl_2)]
        return self.__class__(content=self.acl_compact(temp))
