from dataclasses import dataclass, field
from enum import IntEnum, unique


@dataclass(eq = False, frozen = True, kw_only = True, slots = True)
class NamespaceData:
	id: int
	case: str
	name: str
	subpages: bool
	content: bool
	nonincludable: bool
	canonical: str | None = field(default = None)
	aliases: set[str] = field(default_factory = set)
	namespaceprotection: str | None = field(default = None)
	defaultcontentmodel: str | None = field(default = None)


@unique
class Namespace(IntEnum):
	MEDIA = -2
	SPECIAL = -1
	MAIN = 0
	TALK = 1
	FILE = 6
	FILE_TALK = 7
