'''Parser for MediaWiki titles'''

from .parser import Parser as TitleParser
from .title import Title


__all__ = [
	'TitleParser',
	'Title'
]