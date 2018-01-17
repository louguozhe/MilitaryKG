#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
from tools.nerByLTP import Extractor

#LTP 提供的命名实体类型为:人名（Nh）、地名（Ns）、机构名（Ni）。
#LTP 采用 BIESO 标注体系。B 表示实体开始词，I表示实体中间词，E表示实体结束词，S表示单独成实体，O表示不构成命名实体。

def findTriple(extractor,sentence):
    extractor.chunk_str(sentence)
    extractor.resolve_all_conference()
    print("Triple: ")
    print('\n'.join(str(p) for p in extractor.triple_list))

def processSencenceToWords(extractor,sentence):
    words = extractor.segment(sentence)
    return words
def processSencence(extractor,sentence):
    words = processSencenceToWords(extractor,sentence)
    processWords(extractor, words)

def processWords(extractor,words):
    wordstr = ""
    for i in range(0,len(words)):
        wordstr = wordstr + '%s(%d)\t' % (words[i],i)
    print(wordstr)

    postags = extractor.postag(words)
    print("\t".join(postags))

    arcs = extractor.parse(words,postags)
    print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))

    netags = extractor.recognize(words, postags)
    print("\t".join(netags))

    roles = extractor.label(words, postags,netags, arcs)
    print("\t".join("%d:%s" % (arc.head, arc.relation) for arc in arcs))
    for role in roles:
        print(role.index, "\t".join(["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))
        print(words[role.index], "\t".join(["%s:(%s)" % (arg.name, ''.join(words[arg.range.start: arg.range.end+1])) for arg in role.arguments]))

if __name__ == "__main__":
    extractor = Extractor()
    extractor.load()

    sentence = '我和他都是中国人' #是 A0:(我和他)	ADV:(都)	A1:(中国人)
    sentence = '新华社快讯，韩国统一部９日称，韩朝决定从当地时间10日8时起重启黄海朝韩军用通信线路。'
    processSencence(extractor, sentence)
    #words = sentence.split(' ')
    #processWords(extractor, words)
    #findTriple(extractor,sentence)
    #processSencence(extractor, '日媒：中国第3艘航母已开建 不仅是模仿辽宁舰')


    extractor.release()

