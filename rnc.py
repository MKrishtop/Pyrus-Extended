# coding=UTF-8

import xml.parsers.expat
import codecs

class Reader:
	def __init__(self):
		self._parser = xml.parsers.expat.ParserCreate()
		self._parser.StartElementHandler = self.start_element
		self._parser.EndElementHandler = self.end_element
		self._parser.CharacterDataHandler = self.char_data		
	
	def start_element(self, name, attr):
		if name == 'ana':
			self._info = attr
	
	def end_element(self, name):
		if name == 'se':
			self._sentences.append(self._sentence)
			self._sentence = []
		elif name == 'w':
			self._sentence.append((self._cdata, self._info))
		elif name == 'ana':
			self._cdata = ''
	
	def char_data(self, content):
		self._cdata += content
		
	def read(self, filename):
		f = codecs.open(filename, "r", "UTF-8")
		content = f.read()
		f.close()
		
		self._sentences = []
		self._sentence = []
		self._cdata = ''
		self._info = ''
		
		self._parser.Parse(content.encode("UTF-8"))		
		
		return self._sentences