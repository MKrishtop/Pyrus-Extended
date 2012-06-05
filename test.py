# coding=UTF-8

import sys
import morf
import codecs

rus = {
	'S': u'сущ.', 
	'A': u'прил.', 
	'NUM': u'числ.', 
	'A-NUM': u'числ.-прил.', 
	'V': u'глаг.', 
	'ADV': u'нареч.', 
	'PRAEDIC': u'предикатив', 
	'PARENTH': u'вводное', 
	'S-PRO': u'местоим.сущ.', 
	'A-PRO': u'местоим.прил.', 
	'ADV-PRO': u'местоим.нареч.', 
	'PRAEDIC-PRO': u'местоим.предик.', 
	'PR': u'предлог', 
	'CONJ': u'союз', 
	'PART': u'частица', 
	'INTJ': u'межд.', 
	'INIT': u'инит', 
	'NONLEX': u'нонлекс',
	'm': u'муж.',
	'f': u'жен.',
	'm-f': u'общ.',
	'n': u'ср.',
	'non': u'нет',
	'sg': u'ед.',
	'pl': u'мн.',
	'nom': u'имен.',
	'gen': u'родит.',
	'dat': u'дат.',
	'dat2': u'дистр.дат.',
	'acc': u'винит.',
	'ins': u'творит.',
	'loc': u'предл.',
	'gen2': u'вт.родит.',
	'acc2': u'вт.винит.',
	'loc2': u'вт.предл.',
	'voc': u'зват.ф.',
	'adnum': u'счетн.ф.',
	'1p': u'перв.л.',
	'2p': u'вт.л.',
	'3p': u'тр.л.',
	'praet': u'прош.вр.',
	'praes': u'наст.вр.',
	'fut': u'буд.вр.'
}

tagged_pos = []
tagged_gen = []
tagged_quan = []
tagged_case = []
tagged_face = []
tagged_tense = []

sentence = (u"Астронавты установили в месте посадки флаг США, разместили комплект научных приборов и собрали 21,55 кг образцов лунного грунта, которые были доставлены на Землю. После полёта члены экипажа и образцы лунной породы прошли строгий карантин, который не выявил никаких опасных для человека лунных микроорганизмов")

def posf():

	tag_id = {}
	tag_inv = {}
	
	posl = ['S', 'A', 'NUM', 'A-NUM', 'V', 'ADV', 'PRAEDIC', 'PARENTH', 
		'S-PRO', 'A-PRO', 'ADV-PRO', 'PRAEDIC-PRO', 'PR', 'CONJ', 
		'PART', 'INTJ', 'INIT', 'NONLEX']

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

	tagger_pos.load('tmp/svm-pos.model', 'tmp/ids-pos.pickle')

	for word, label in tagger_pos.label(sentence):
		tagged_pos.append((word, tagger_pos.get_label(label)))
	
	#print(tagged_pos)
	return
##############################################################

def genf():
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

	tagger_gen.load('tmp/svm-gender.model', 'tmp/ids-gender.pickle')

	has_gender = ['S', 'A', 'S-PRO', 'A-PRO']

	for word, label in tagger_gen.label(sentence): 

		new_label = 'non'

		for n_word, n_label in tagged_pos:
			if ((n_word == word) & (n_label in has_gender)):
				new_label = tagger_gen.get_label(label)
				break

		tagged_gen.append((word, new_label))
	
	#print(tagged_gen)
	return
#############################################################

def quanf():
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

	tagger_quan.load('tmp/svm-quantity.model', 'tmp/ids-quantity.pickle')

	has_quantity = ['S', 'A', 'V', 'S-PRO', 'A-PRO']

	for word, label in tagger_quan.label(sentence): 

		new_label = 'non'

		for n_word, n_label in tagged_pos:
			if ((n_word == word) & (n_label in has_quantity)):
				new_label = tagger_quan.get_label(label)
				break

		tagged_quan.append((word, new_label))
	
	#print(tagged_quan)
	return
#############################################################

def casef():
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

	tagger_case.load('tmp/svm-case.model', 'tmp/ids-case.pickle')

	has_case = ['S', 'S-PRO', 'A', 'A-PRO']#, 'A', 'V', 'A-PRO'

	for word, label in tagger_case.label(sentence): 

		new_label = 'non'

		for n_word, n_label in tagged_pos:
			if ((n_word == word) & (n_label in has_case)):
				new_label = tagger_case.get_label(label)
				break

		tagged_case.append((word, new_label))
	
	#print(tagged_case)
	return
#############################################################

def facef():
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

	tagger_face.load('tmp/svm-face.model', 'tmp/ids-face.pickle')

	has_face = ['S-PRO', 'V']

	for word, label in tagger_face.label(sentence): 

		new_label = 'non'

		for n_word, n_label in tagged_pos:
			if ((n_word == word) & (n_label in has_face)):
				new_label = tagger_face.get_label(label)
				break

		tagged_face.append((word, new_label))
	
	#print(tagged_face)
	return
#############################################################

def tensef():
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

	tagger_tense.load('tmp/svm-tense.model', 'tmp/ids-tense.pickle')

	has_tense = ['V']

	for word, label in tagger_tense.label(sentence): 

		new_label = 'non'

		for n_word, n_label in tagged_pos:
			if ((n_word == word) & (n_label in has_tense)):
				new_label = tagger_tense.get_label(label)
				break

		tagged_tense.append((word, new_label))
	
	#print(tagged_tense)
	return
########################################################################

def output():
	i = 0
	
	sys.stdout.write( codecs.BOM_UTF8 )

	while i<len(tagged_pos):
		sys.stdout.write((tagged_pos[i][0].encode("utf-8")) + ": ")

		sys.stdout.write("<" + rus[tagged_pos[i][1]].encode("utf-8"))
		sys.stdout.write(", " + rus[tagged_gen[i][1]].encode("utf-8"))
		sys.stdout.write(", " + rus[tagged_quan[i][1]].encode("utf-8"))
		sys.stdout.write(", " + rus[tagged_case[i][1]].encode("utf-8"))
		sys.stdout.write(", " + rus[tagged_face[i][1]].encode("utf-8"))
		sys.stdout.write(", " + rus[tagged_tense[i][1]].encode("utf-8") + ">")
		print()
		i = i + 1
	return

########################################################################
posf()
genf()
quanf()
casef()
facef()
tensef()
output()