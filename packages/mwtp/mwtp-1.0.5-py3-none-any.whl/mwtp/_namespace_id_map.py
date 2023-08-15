class NamespaceIDMap:
	
	def __init__(self):
		self._map = {}
	
	def __repr__(self):
		return f'{self.__class__.__name__}({self._map!r})'
	
	def __contains__(self, key):
		return self[key] is not None
	
	def __getitem__(self, key):
		if not isinstance(key, str):
			return None
		
		normalized_key = key.lower()
		
		return self._map.get(normalized_key)
	
	def __setitem__(self, key, value):
		if not isinstance(key, str):
			raise TypeError('Key must be a string')
		
		if not isinstance(value, int):
			raise TypeError('Value must be an integer')
		
		normalized_key = key.lower()
		
		self._map[normalized_key] = value
	
	def __delitem__(self, key):
		raise TypeError('Keys cannot be deleted')
	
	def __len__(self):
		return len(self._map)
	
	def __iter__(self):
		return iter(self._map)
