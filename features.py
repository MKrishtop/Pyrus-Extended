import pickle
import ml
class TaggerFeatures:
	def __init__(self):
		self._body_id = {}
		self._suffix_id = {}
		self._prefix_id = {}
		
		self._train = True
		self._featurespace = ml.FeatureSpace()
		
	def load(self, fp):
		(self._body_id, self._suffix_id, self._prefix_id) = pickle.load(fp)
		self._train = False
		
	def save(self, fp):
		pickle.dump((self._body_id, self._suffix_id, self._prefix_id), fp)

	def from_body(self, body):
		featureset = {}
		if self._train:
			if body not in self._body_id:
				self._body_id[body] = len(self._body_id) + 1
					
			featureset[self._body_id[body]] = 1
		else:
			if body in self._body_id:
				featureset[self._body_id[body]] = 1
				
		return featureset
	
	def from_suffix(self, body):
		featureset = {}
		
		suffix2 = body[-2:]
		if suffix2 not in self._suffix_id:
			self._suffix_id[suffix2] = len(self._suffix_id) + 1
		featureset[self._suffix_id[suffix2]] = 1
		
		suffix3 = body[-3:]
		if suffix3 not in self._suffix_id:
			self._suffix_id[suffix3] = len(self._suffix_id) + 1
		featureset[self._suffix_id[suffix3]] = 1
		
		return featureset
	
	def from_prefix(self, body):
		featureset = {}
		
		prefix2 = body[:2]
		if prefix2 not in self._prefix_id:
			self._prefix_id[prefix2] = len(self._prefix_id) + 1
		featureset[self._prefix_id[prefix2]] = 1
		
		prefix3 = body[:3]
		if prefix3 not in self._prefix_id:
			self._prefix_id[prefix3] = len(self._prefix_id) + 1
		featureset[self._prefix_id[prefix3]] = 1
		
		return featureset