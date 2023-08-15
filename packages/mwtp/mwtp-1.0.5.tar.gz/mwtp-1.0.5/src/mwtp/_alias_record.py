class AliasRecord:
	
	def __init__(self, data):
		self._record = {}
		
		for entry in data:
			namespace_id, alias = entry['id'], entry['alias']
			self._record.setdefault(namespace_id, set()).add(alias)
	
	def __getitem__(self, key):
		numeric_key = int(key)
		
		return self._record.get(numeric_key)
	
	def __repr__(self):
		return f'{self.__class__.__name__}{self._record!r}'
