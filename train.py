# coding=UTF-8

import sys
import re

import rnc
import morf

sentences = []
sentences.extend(rnc.Reader().read('res/fiction.xml'))
sentences.extend(rnc.Reader().read('res/science.xml'))
sentences.extend(rnc.Reader().read('res/laws.xml'))
sentences.extend(rnc.Reader().read('res/media1.xml'))
sentences.extend(rnc.Reader().read('res/media2.xml'))
sentences.extend(rnc.Reader().read('res/media3.xml'))

tag_id = {}
tag_inv = {}

posl = ['S', 'A', 'NUM', 'A-NUM', 'V', 'ADV', 'PRAEDIC', 'PARENTH', 
	'S-PRO', 'A-PRO', 'ADV-PRO', 'PRAEDIC-PRO', 'PR', 'CONJ', 
	'PART', 'INTJ', 'INIT', 'NONLEX']

re_pos = re.compile('([\w-]+)(?:[^\w-]|$)'.format('|'.join(posl)))

for i in range(0, len(posl)):
	tag_id[posl[i]] = i + 1
	tag_inv[i + 1] = posl[i]
	
tagger_pos = morf.Tagger(
	posl, tag_id, tag_inv,
	{'suff': 1,
	'pref': 1,
	'body': 1,
	'prev': 1},
	3)

sentence_labels = []
sentence_words = []
for sentence in sentences:
	labels = []
	words = []
	for word in sentence:
		gr = word[1]['gr']
		m = re_pos.match(gr)
		# if not m:
			# print(gr, file = sys.stderr)
			
		pos = m.group(1)
		if pos == 'ANUM':
			pos = 'A-NUM'
			
		label = tagger_pos.get_label_id(pos)
		# if not label:
		# 	print(gr, file = sys.stderr)
			
		labels.append(label)
		
		body = word[0].replace('`', '')
		words.append(body)
		
	sentence_labels.append(labels)
	sentence_words.append(words)
			
tagger_pos.train(sentence_words, sentence_labels, True)
tagger_pos.train(sentence_words, sentence_labels)
tagger_pos.save('tmp/svm-pos.model', 'tmp/ids-pos.pickle')
##############################################################

tag_id = {}
tag_inv = {}

genl = ['m', 'f', 'm-f', 'n']

for i in range(0, len(genl)):
	tag_id[genl[i]] = i + 1
	tag_inv[i + 1] = genl[i]

tagger_gen = morf.Tagger(
	genl, tag_id, tag_inv,
	{'suff': 1,
	'pref': 0,
	'body': 1,
	'prev': 0},
	3)

sentence_labels = []
sentence_words = []
for sentence in sentences:
	labels = []
	words = []
	for word in sentence:
		pos = -100
		
		gr = word[1]['gr']
		lgr = gr.rsplit(',')

		for onegr in lgr:
			if onegr in tagger_gen.tagset:
				pos = onegr
				break
			
		label = tagger_gen.get_label_id(pos)
		if not label:
			continue
			
		labels.append(label)
		
		body = word[0].replace('`', '')
		words.append(body)
		
	sentence_labels.append(labels)
	sentence_words.append(words)
			
tagger_gen.train(sentence_words, sentence_labels, True)
tagger_gen.train(sentence_words, sentence_labels)
tagger_gen.save('tmp/svm-gender.model', 'tmp/ids-gender.pickle')
###############################################################

tag_id = {}
tag_inv = {}

quanl = ['sg', 'pl']

for i in range(0, len(quanl)):
	tag_id[quanl[i]] = i + 1
	tag_inv[i + 1] = quanl[i]

tagger_quan = morf.Tagger(
	quanl, tag_id, tag_inv,
	{'suff': 1,
	'pref': 0,
	'body': 1,
	'prev': 0},
	3)

sentence_labels = []
sentence_words = []
for sentence in sentences:
	labels = []
	words = []
	for word in sentence:
		pos = -100
		
		gr = word[1]['gr']
		lgr = gr.rsplit(',')

		for onegr in lgr:
			if onegr in tagger_quan.tagset:
				pos = onegr
				break
			
		label = tagger_quan.get_label_id(pos)
		if not label:
			continue
			
		labels.append(label)
		
		body = word[0].replace('`', '')
		words.append(body)
		
	sentence_labels.append(labels)
	sentence_words.append(words)
			
tagger_quan.train(sentence_words, sentence_labels, True)
tagger_quan.train(sentence_words, sentence_labels)
tagger_quan.save('tmp/svm-quantity.model', 'tmp/ids-quantity.pickle')
##############################################################

tag_id = {}
tag_inv = {}

casel = ['nom', 'gen', 'dat', 'dat2', 'acc', 'ins', 
	'loc', 'gen2', 'acc2', 'loc2']# , 'voc', 'adnum'

for i in range(0, len(casel)):
	tag_id[casel[i]] = i + 1
	tag_inv[i + 1] = casel[i]

tagger_case = morf.Tagger(
	casel, tag_id, tag_inv,
	{'suff': 1,
	'pref': 1,
	'body': 1,
	'prev': 1},
	3)

sentence_labels = []
sentence_words = []
for sentence in sentences:
	labels = []
	words = []
	for word in sentence:
		pos = -100
		
		gr = word[1]['gr']
		lgr = gr.rsplit(',')

		for onegr in lgr:
			if onegr in tagger_case.tagset:
				pos = onegr
				break
			
		label = tagger_case.get_label_id(pos)
		if not label:
			continue
			
		labels.append(label)
		
		body = word[0].replace('`', '')
		words.append(body)
		
	sentence_labels.append(labels)
	sentence_words.append(words)
			
tagger_case.train(sentence_words, sentence_labels, True)
tagger_case.train(sentence_words, sentence_labels)
tagger_case.save('tmp/svm-case.model', 'tmp/ids-case.pickle')

##############################################################

tag_id = {}
tag_inv = {}

facel = ['1p', '2p', '3p']

for i in range(0, len(facel)):
	tag_id[facel[i]] = i + 1
	tag_inv[i + 1] = facel[i]

tagger_face = morf.Tagger(
	facel, tag_id, tag_inv,
	{'suff': 1,
	'pref': 0,
	'body': 1,
	'prev': 1},
	3)

sentence_labels = []
sentence_words = []
for sentence in sentences:
	labels = []
	words = []
	for word in sentence:
		pos = -100
		
		gr = word[1]['gr']
		lgr = gr.rsplit(',')

		for onegr in lgr:
			if onegr in tagger_face.tagset:
				pos = onegr
				break
			
		label = tagger_face.get_label_id(pos)
		if not label:
			continue
			
		labels.append(label)
		
		body = word[0].replace('`', '')
		words.append(body)
		
	sentence_labels.append(labels)
	sentence_words.append(words)
			
tagger_face.train(sentence_words, sentence_labels, True)
tagger_face.train(sentence_words, sentence_labels)
tagger_face.save('tmp/svm-face.model', 'tmp/ids-face.pickle')
##############################################################

tag_id = {}
tag_inv = {}

tensel = ['praet', 'praes', 'fut']

for i in range(0, len(tensel)):
	tag_id[tensel[i]] = i + 1
	tag_inv[i + 1] = tensel[i]

tagger_tense = morf.Tagger(
	tensel, tag_id, tag_inv,
	{'suff': 1,
	'pref': 0,
	'body': 1,
	'prev': 1},
	3)

sentence_labels = []
sentence_words = []
for sentence in sentences:
	labels = []
	words = []
	for word in sentence:
		pos = -100
		
		gr = word[1]['gr']
		lgr = gr.rsplit(',')

		for onegr in lgr:
			if onegr in tagger_tense.tagset:
				pos = onegr
				break
			
		label = tagger_tense.get_label_id(pos)
		if not label:
			continue
			
		labels.append(label)
		
		body = word[0].replace('`', '')
		words.append(body)
		
	sentence_labels.append(labels)
	sentence_words.append(words)
			
tagger_tense.train(sentence_words, sentence_labels, True)
tagger_tense.train(sentence_words, sentence_labels)
tagger_tense.save('tmp/svm-tense.model', 'tmp/ids-tense.pickle')