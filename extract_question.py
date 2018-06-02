# coding=utf-8
from __future__ import division
import pymongo
import re
import pandas as pd
import sys 
import os
import jieba
import jieba.posseg as pseg
import operator


reload(sys) 
sys.setdefaultencoding("utf-8")

# 需要本地词典增加对英文特殊名词的命中率
jieba.load_userdict("userdict.txt")

english_pattern = re.compile(r'\w+')

# from unidecode import unidecode

# def FormatString(s):
# 	if isinstance(s, unicode):
# 		try:
# 			s.encode('ascii')
# 			return s
# 		except:
# 			return unidecode(s)
# 	else:
# 		return s


# chinese = u"([\u4e00-\u9fff]+)"
# pattern = re.compile(chinese)

def cut_centence(sentence):
	seg_list = jieba.cut(sentence, cut_all=False, HMM=True)
	return "/ ".join(seg_list)

# 分词并获取词性
def cut_sentence_using_posseg(sentence):
	result = pseg.cut(sentence)
	word_hub = {}
	for ret in result:
		ret_dict = ret.__dict__

		if ret_dict['flag'] in ['n','v']:
			if word_hub.has_key(ret_dict['word']):
				word_hub[ret_dict['word']]['counter'] += 1
				word_hub[ret_dict['word']]['flag'] = ret_dict['flag']
			else:
				word_hub[ret_dict['word']] = {}
				word_hub[ret_dict['word']]['counter'] = 1
				word_hub[ret_dict['word']]['flag'] = ret_dict['flag']
	return word_hub

def cut_sentence_usring_posseg_and_get_nvlist(sentence):
	result = pseg.cut(sentence)
	nv_dict = {
		'n':[],
		'v':[]
	} 
	for ret in result:
		ret_dict = ret.__dict__
		if ret_dict['word'].lower() in ['linke','mr','ping','inc','log','ip','core']:
			ret_dict['word'] = ret_dict['word'].lower()
			ret_dict['flag'] = 'n'


		if ret_dict['word'].lower() in ['kill']:
			ret_dict['word'] = ret_dict['word'].lower()
			ret_dict['flag'] = 'v'

		if english_pattern.match(ret_dict['word'].strip()) is not None:
			ret_dict['word'] = ret_dict['word'].lower()

		if ret_dict['flag'] in ['n','v']:
			if ret_dict['flag'] == 'n':
				if ret_dict['word'] not in nv_dict['n']:
					nv_dict['n'].append(ret_dict['word'])
			else:
				if ret_dict['flag'] == 'v':
					if ret_dict['word'] not in nv_dict['v']:
						nv_dict['v'].append(ret_dict['word'])
	return nv_dict

def print_noun(word_hub):
	for token in word_hub:
		if word_hub[token]['flag'] == 'n':
			print '名词 [%s] 次数 [%d]' % (token,word_hub[token]['counter'])
		elif word_hub[token]['flag'] == 'v':
			print '动词 [%s] 次数 [%d]' % (token,word_hub[token]['counter'])
		else:
			print '' 

def count_tag(tag,question_total):
	counter_tag = {}
	text_list = []
	for token in tag:
		if counter_tag.has_key(token):
			counter_tag[token] +=1
		else:
			counter_tag[token] = 1
	sorted_x = sorted(counter_tag.items(), key=operator.itemgetter(1), reverse=True)
	for x in sorted_x[:100]:
		partision = str((x[1]/question_total)*100)[:5]+'%'
		text_str = '[%s]:[%d]:[%s]' % (x[0],x[1],partision)
		text_list.append(text_str)
	return '\n'.join(text_list)

def print_nv_dict(nv_dict):
	print '名词 [%s]' % '/'.join(nv_dict['n'])
	print '动词 [%s]' % '/'.join(nv_dict['v'])



# 抽取问答的所有模糊匹配条件
ifcan_pattern = re.compile(u'.*[\u80fd\u6ca1\u53ef\u4f1a].*[\u5417\u4e48].*')
but_pattern = re.compile(u'.*[\u4f46][\u662f].*[\u4e0d\u6ca1\u80fd].*|.*[\u4f46][\u662f].*[\u5931][\u8d25].*')
fail_pattern = re.compile(u'.*[\u6ca1].*[\u6210]')
what_pattern = re.compile(u'.*[\u662f].*[\u4e48\u5417].*')
request_pattern = re.compile(u'.*[\u5e2e].*[\u770b\u5904\u7406].*')
why_list = map(lambda i:i.decode('utf-8'),['为什么','为啥','啥问题'])
question_list = map(lambda i:i.decode('utf-8'),['请教','请问','问一下','咨询下','的问题'])
ifcan_list = map(lambda i:i.decode('utf-8'),['行吗','能否','是否','行么'])
fail_list = map(lambda i:i.decode('utf-8'),['报错','有问题','失败','走不下去','找不到','不一致','一直没有','没资源','没机器','无变更','挂了','访问不了'])
request_list = map(lambda i:i.decode('utf-8'),['麻烦看'])
how_list = map(lambda i:i.decode('utf-8'),['怎么','如何'])
where_list = map(lambda i:i.decode('utf-8'),['在哪','哪里'])
what_list = map(lambda i:i.decode('utf-8'),['是什么','是不是'])


# 判断是否符合问题模版
def if_question(sentence):

	# ret = {
	# 	'sentence':'',
	# 	'questionClass':''
	# }

	try:
		sen = sentence.decode('utf-8')
	except UnicodeEncodeError:
		sen = sentence

	for why in why_list:
		if why in sen:
			return {
				'sentence'     : sen,
				'questionClass': 'why',
				'questionKey'  : why
			}

	for ifcan in ifcan_list:
		if ifcan in sen:
			return {
				'sentence'     : sen,
				'questionClass': 'ifcan',
				'questionKey'  : ifcan
			}

	for fail in fail_list:
		if fail in sen:
			return {
				'sentence'     : sen,
				'questionClass': 'fail',
				'questionKey'  : fail
			}

	for request in request_list:
		if request in sen:
			return {
				'sentence'     : sen,
				'questionClass': 'request',
				'questionKey'  : request
			}

	for how in how_list:
		if how in sen:
			return {
				'sentence'     : sen,
				'questionClass': 'how',
				'questionKey'  : how
			}

	for where in where_list:
		if where in sen:
			return {
				'sentence'     : sen,
				'questionClass': 'where',
				'questionKey'  : where
			}

	for what in what_list:
		if what in sen:
			return {
				'sentence'     : sen,
				'questionClass': 'what',
				'questionKey'  : what
			}

	if if_exsit(ifcan_pattern.findall(sen)):
			return {
				'sentence'     : sen,
				'questionClass': 'ifcan'
			}

	if if_exsit(but_pattern.findall(sen)):
			return {
				'sentence'     : sen,
				'questionClass': 'but'
			}

	if if_exsit(fail_pattern.findall(sen)):
			return {
				'sentence'     : sen,
				'questionClass': 'fail'
			}

	if if_exsit(what_pattern.findall(sen)):
			return {
				'sentence'     : sen,
				'questionClass': 'what'
			}

	if if_exsit(request_pattern.findall(sen)):
			return {
				'sentence'     : sen,
				'questionClass': 'request'
			}

	for question in question_list:
		if question in sen:
			return {
				'sentence'     : sen,
				'questionClass': 'question',
				'questionKey'  : question
			}

def if_exsit(i):
	if i is not None:
		if len(i) > 0:
			return i



def get_collection():
	client = pymongo.MongoClient('???')
	db = client.linksAggregation
	collection = db.aggregation
	return collection


collection = get_collection()

# result = collection.find({},{'messagesText':1,'_id':0}).limit(10).skip(5)

field_list = ['发布','机器','基础运维','平台故障','平台问题','应用','DRM','中间件',
				'Scheduler','研发容器','迭代','需求','故障标签','消息投递','用户自主解决','其他',
					'sofarouter','沙箱','金融云','分库分表','推送']
					
for field in field_list:

	result = collection.find({'tagLevel1':field},{'tagLevel1':1,'messagesText':1,'linksUrl':1,'_id':0})

	counter = 0
	totallen = 0
	dataTable = []
	tag = []

	for item in result:
		data = {}
		nvlist = []
		totallen +=1
		text = item['messagesText']
		linksUrl = item['linksUrl']
		data['summary'] = '\n'.join(text.split('\n')[:5])
		data['linksUrl'] = linksUrl
		q = []
		for t in text.split('\n')[:5]:
			print t
			if if_question(t) is not None:
				q.append(if_question(t))
		if len(q) > 0:
			counter =counter+1
		
		print '~~~~~~~~~~~~~~~~ CONVERSATION CLOSED ~~~~~~~~~~~~~~~~'
		print '~~~~~~~~~~~~~~~~ QUESTION ~~~~~~~~~~~~~~~~'
		if len(q) > 0:

			data['question'] = q[0]['sentence']
			print 'Question:'
			print q[0]['sentence']
			print cut_centence(q[0]['sentence'])
			nvlist = cut_sentence_usring_posseg_and_get_nvlist(q[0]['sentence'])
			data['noun_tag'] = ','.join(nvlist['n'])
			print_nv_dict(nvlist)
			tag = tag + nvlist['n']

			data['questionClass'] = q[0]['questionClass']
			print 'Question Class [%s]' % q[0]['questionClass']
			if q[0].has_key('questionKey'):
				data['questionKey'] = q[0]['questionKey']
				print 'QuestionKey [%s]' % q[0]['questionKey']
			else:
				data['questionKey'] = ''

		else:
			data['question'] = ''
			data['questionClass'] = ''
			data['questionKey'] = ''
			print '404 NOT FOUND'
		print '~~~~~~~~~~~~~~~~ QUESTION ~~~~~~~~~~~~~~~~'
		print '\n\n'
		dataTable.append(data.copy())
	with open('%s.txt'%field,'w') as f:
		f.write('total Question: %d\n' % counter)
		f.write('total 会话: %d\n' % totallen)
		counter_text = count_tag(tag,counter)
		f.write(counter_text)


	df = pd.DataFrame(dataTable)
	# # df = df.applymap(lambda x: x.encode('unicode_escape').decode('utf-8') if isinstance(x, str) else x)
	df.to_csv('output-%s.csv'%field)

	cmd = "iconv -f UTF8 -t GB18030 output-{}.csv >output-{}-GBK.csv".format(field,field)
	os.system(cmd)

# dialogSummary = []
# for dialog in dataTable:
# 	dialogSummary.append(dialog['summary'])

# dialogText = '\n'.join(dialogSummary)

# with open('dialogText.txt','w') as f:
# 	f.write(dialogText)


