class SizeLimitedDictionary:
	"""A dictionary class that has a maximum capcaity.  It is guarenteed to
	   always have the most recent capacity number of items present.  Older
	   items may be eliminated.  It will never use more that (approximately) 
	   twice the storage of a regular dictionary.  All operations take at 
	   most (approximately) twice the time of regular dictionary."""
	   
	def __init__(self, capacity):
		"""Create a new dictionary with the specified capacity."""
		self._capacity = capacity
		self._recent = {}
		self._old = {}
		
	def has_key(self, key):
		"""Test whether the given item is stored in the dictionary."""
		return self._recent.has_key(key) or self._old.has_key(key)
		
	def __getitem__(self, key):
		"""Return the value for the specified key.  If it is not present
		throw a KeyError."""
		try:
			return self._recent[key]
		except KeyError:
			pass
			
		try:
			value = self._old[key]
			self._recent[key] = value
			if len(self._recent) > self._capacity:
				self._old = self._recent
				self._recent = {}
			return value
		except KeyError:
			raise KeyError('Unable to find key')
		
	def __setitem__(self, key, value):
		"""Store the value using the specified key."""
		self._recent[key] = value
		if len(self._recent) > self._capacity:
			self._old = self._recent
			self._recent = {}		
