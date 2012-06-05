import liblinearutil as svm
import features
import ml
import re
import string

class Tagger:
	def __init__(self, ts, tid, tinv, fm, len):
		self.tagset = ts
		self.tag_id = tid
		self.tag_inv = tinv
		self.fmask = fm
		self.chain_len = len
		self._features = features.TaggerFeatures()
		pass
	
	def load(self, modelname, featuresname):
		self._svm_model = svm.load_model(modelname)
		self._features.load(open(featuresname, 'rb'))
		
	def save(self, modelname, featuresname):
		svm.save_model(modelname, self._svm_model)
		self._features.save(open(featuresname, 'wb'))
		
	def get_label_id(self, pos):
		return self.tag_id[pos] if pos in self.tag_id else 0
	
	def get_label(self, id):
		return self.tag_inv[id] if id in self.tag_inv else '?'
		
	def train(self, sentences, labels, cross_validation = False):
		x = []
		y = []
		
		for i in range(0, len(sentences)):
			sentence = sentences[i]
			prev = []
			
			j = 0
			for word in sentence:
				body = word.lower()
				
				featurespace = self._construct_featurespace(body, prev)
				
				prev.append((body, labels[i][j]))
				if len(prev) > self.chain_len:
					del(prev[0])
					
				x.append(featurespace.featureset)
				j += 1

			y.extend(labels[i])

		prob = svm.problem(y, x)
		
		if cross_validation:
			param = svm.parameter('-c 1 -v 4 -s 4')
			svm.train(prob, param)
		else:
			param = svm.parameter('-c 1 -s 4')
			self._svm_model = svm.train(prob, param)
	
	def label(self, sentence):
		for c in string.punctuation:
			sentence = sentence.replace(c,"")
		
		labeled = []
		prev = []
		for word in sentence.split(" "):
			body = word.lower()
			featurespace = self._construct_featurespace(body, prev)
			
			p_label, _, _ = svm.predict([0], [featurespace.featureset], self._svm_model, '')
			label = p_label[0]
			
			prev.append((body, label))
			if len(prev) > self.chain_len:
				del(prev[0])
				
			labeled.append((word, label))
			
		return labeled
				
	def _construct_featurespace(self, word, prev):
		featurespace = ml.FeatureSpace()
			
		featurespace.add({1: len(word)}, 10)
		if self.fmask['suff']:
			featurespace.add(self._features.from_suffix(word))
		if self.fmask['pref']:
			featurespace.add(self._features.from_prefix(word))
		if self.fmask['body']:
			featurespace.add(self._features.from_body(word))

		if self.fmask['prev']:
			for item in prev:
				featurespace.add({1: item[1]}, 100)
#				featurespace.add(features.from_suffix(item[0]))
#				featurespace.add(features.from_prefix(item[0]))
#				featurespace.add(features.from_body(item[0]))
	
		return featurespace