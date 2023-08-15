import re
from functools import total_ordering

from ._dcs import Namespace


@total_ordering
class Title:
	
	__slots__ = ('_name', '_namespace', '_parser')
	
	_extension = re.compile(r'(?<=\.)[^.\s]+$')
	
	def __init__(self, name, *, namespace, parser):
		self._name = name
		self._namespace = namespace
		self._parser = parser
	
	def __str__(self):
		return self.full_name
	
	def __repr__(self):
		return f'{self.__class__.__name__}({self.full_name!r})'
	
	def __hash__(self):
		return hash(self.full_name)
	
	def __lt__(self, other):
		if isinstance(other, self.__class__):
			return self.full_name < other.full_name
		
		if isinstance(other, str):
			return self.full_name < other
		
		return NotImplemented
	
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return self.full_name == other.full_name
		
		if isinstance(other, str):
			return self.full_name == other
		
		return NotImplemented
	
	def __truediv__(self, other):
		return self._parser.parse(f'{self.full_name}/{other}')
	
	@property
	def full_name(self):
		if self.namespace != 0:
			return f'{self.namespace_name}:{self._name}'
		
		return self.name
	
	@property
	def namespace(self):
		return self._namespace
	
	@property
	def name(self):
		return self._name
	
	@property
	def namespace_name(self):
		return self.namespace_data.name
	
	@property
	def namespace_data(self):
		return self._parser.namespace_data[str(self.namespace)]
	
	@property
	def canonical_namespace_name(self):
		return self.namespace_data.canonical
	
	@property
	def associated_namespace(self):
		if self.namespace < 0:
			return None
		
		if self.namespace % 2 == 1:
			return self.namespace - 1
		else:
			return self.namespace + 1
	
	@property
	def associated_namespace_name(self):
		namespace_data = self.associated_namespace_data
		
		if namespace_data is None:
			return None
		
		return namespace_data.name
	
	@property
	def associated_namespace_data(self):
		namespace_id = self.associated_namespace
		
		if namespace_id is None:
			return None
		
		return self._parser.namespace_data \
			.get(str(namespace_id))
	
	@property
	def in_content_namespace(self):
		return self.namespace_data.content
	
	@property
	def title_fragments(self):
		if self.namespace_data.subpages:
			return tuple(self.name.split('/'))
		
		return tuple([self.name])
	
	@property
	def root(self):
		return self.__class__(
			self.title_fragments[0],
			namespace = self.namespace,
			parser = self._parser
		)
	
	@property
	def base(self):
		fragments = self.title_fragments
		
		if len(fragments) == 1:
			new_page_name = fragments[0]
		else:
			new_page_name = '/'.join(fragments[:-1])
		
		return self.__class__(
			new_page_name,
			namespace = self.namespace,
			parser = self._parser
		)
	
	@property
	def tail(self):
		# Naming reason: https://superuser.com/q/524724
		return self.title_fragments[-1]
	
	@property
	def is_subpage(self):
		return len(self.title_fragments) > 1
	
	@property
	def extension(self):
		if self.namespace not in (Namespace.FILE, Namespace.FILE_TALK):
			return None
		
		match = self._extension.search(self.name)
		
		if match is None:
			return None
		
		return match.group(0)
	
	@property
	def associated(self):
		associated_namespace = self.associated_namespace
		
		if associated_namespace is None:
			return None
		
		return self.__class__(
			self.name,
			namespace = self.associated_namespace,
			parser = self._parser
		)
	
	@property
	def subject(self):
		if self.namespace < 0 or self.namespace % 2 == 0:
			return self
		
		return self.associated
	
	@property
	def talk(self):
		if self.namespace < 0:
			return None
		
		if self.namespace % 2 == 1:
			return self
		
		return self.associated
