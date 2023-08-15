import re


class TitleLike:
	
	_whitespace_char_codes = (
		0x0020, 0x005F, 0x00A0, 0x1680, 0x180E,
		*range(0x2000, 0x200A + 1),
		0x2028, 0x2029, 0x202F, 0x205F, 0x3000
	)
	_unicode_bidi_char_codes = (
		0x200E, 0x200F, 0x202A, 0x202E
	)
	
	_whitespace_series = re.compile(
		f'[{"".join(map(chr, _whitespace_char_codes))}]+'
	)
	_unicode_bidi_marks = re.compile(
		f'[{"".join(map(chr, _unicode_bidi_char_codes))}]+'
	)
	
	_first_colon = re.compile(f' *: *')
	_url_encoded_char = re.compile(r'%[\dA-Fa-f]{2}')
	_html_entity_like = re.compile(r'&[\dA-Za-z\u0080-\uFFFF]+;')
	
	_disallowed_leading_components = ('./', '../')
	_disallowed_trailing_components = ('/.', '/..')
	_disallowed_components = ('/./', '/../')
	
	def __init__(self, string):
		self._string = string
	
	def __contains__(self, item):
		return item in self._string
	
	def __eq__(self, other):
		if isinstance(other, self.__class__):
			return str(self) == str(other)
		
		if isinstance(other, str):
			return str(self) == other
		
		return NotImplemented
	
	def __getitem__(self, item):
		return self._string[item]
	
	def __len__(self):
		surrogate_pair_converted = self._string \
			.encode('utf-16-be', 'surrogatepass') \
			.decode('utf-16-be')
		
		return len(surrogate_pair_converted.encode('utf-8'))
	
	def __repr__(self):
		return f'{self.__class__.__name__}({self._string!r})'
	
	def __str__(self):
		return self._string
	
	def set(self, new_value):
		self._string = new_value
	
	def starts_with(self, substring):
		return self._string.startswith(substring)
	
	def ends_with(self, substring):
		return self._string.endswith(substring)
	
	def extract(self, start, end = None):
		self._string = self._string[start:end]
	
	def find_index(self, substring):
		index = self._string.find(substring)
		
		return index if index != -1 else None
	
	def remove_unicode_bidirectional_marks(self):
		self._string = self._unicode_bidi_marks.sub('', self._string)
	
	def collapse_whitespaces_series(self):
		self._string = self._whitespace_series.sub(' ', self._string)
	
	def strip_surrounding_spaces(self):
		self._string = self._string.strip(' ')
	
	def sanitize(self):
		self.remove_unicode_bidirectional_marks()
		self.collapse_whitespaces_series()
		self.strip_surrounding_spaces()
	
	def split_by_first_colon(self):
		splitted = self._first_colon.split(self._string, maxsplit = 1)
		
		if len(splitted) == 2:
			return tuple(splitted)
		
		return None, splitted[0]
	
	def contains_url_encoded_character(self):
		match = self._url_encoded_char.search(self._string)
		
		return match is not None
	
	def contains_html_entity_like(self):
		match = self._html_entity_like.search(self._string)
		
		return match is not None
	
	def has_relative_path_component(self):
		if '.' not in self._string:
			return False
		
		looks_like_relative_path = (
				self._is_relative_path_component() or
				self._starts_with_disallowed_component() or
				self._contains_disallowed_component() or
				self._ends_with_disallowed_component()
		)
		
		return looks_like_relative_path
	
	def _is_relative_path_component(self):
		return self._string == '.' or self._string == '..'
	
	def _starts_with_disallowed_component(self):
		return any(
			self.starts_with(component)
			for component in self._disallowed_leading_components
		)
	
	def _ends_with_disallowed_component(self):
		return any(
			self.ends_with(component)
			for component in self._disallowed_trailing_components
		)
	
	def _contains_disallowed_component(self):
		return any(
			component in self
			for component in self._disallowed_components
		)
	
	def contains_signature_component(self):
		return '~~~' in self._string
	
	def remove_fragment_if_any(self):
		fragment_index = self.find_index('#')
		
		if fragment_index is not None:
			self.extract(0, fragment_index)
		
		self.strip_surrounding_spaces()
