from dataclasses import dataclass
from typing import List, TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from .ident import Ident, SchemaObjectIdent
    from .object_type import ObjectType


@dataclass
class MaskingPolicyReference:
    object_type: "ObjectType"
    object_name: "SchemaObjectIdent"
    columns: List["Ident"]


@dataclass
class RowAccessPolicyReference:
    object_type: "ObjectType"
    object_name: "SchemaObjectIdent"
    columns: List["Ident"]


@dataclass
class TagReference:
    object_type: "ObjectType"
    object_name: "SchemaObjectIdent"
    column_name: Optional["Ident"]
    tag_value: str
