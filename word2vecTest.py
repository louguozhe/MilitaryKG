#encoding=utf-8
from gensim.models import word2vec
import codecs
import os

def train(textfilename,modelfilename,modelfilename2):
    sentences=word2vec.Text8Corpus(textfilename)
    model=word2vec.Word2Vec(sentences, size=50)
    model.save(modelfilename)
    model.wv.save_word2vec_format(modelfilename2, binary=False)

def test(modelfilename):
    model = word2vec.Word2Vec.load(modelfilename)
    y2=model.similarity(u"领导", u"干部")
    print('领导：',model[u"领导"])
    print(y2)

    for i in model.most_similar(u"新华社"):
        print(i[0],i[1])
    #model.most_similar(positive=['新华社', '北京'], negative=['上海'])
    print('余弦相似度：',model.similarity(u'新华社', u'北京'))
    #可计算两个集合之间的相似度
    # list1 = [u'今天', u'我', u'很', u'开心']
    # list2 = [u'空气', u'清新', u'善良', u'开心']
    # list_sim1 = model.n_similarity(list1, list2)
    # print(list_sim1)

    #选出不同类的词语
    # list = [u'纽约', u'北京', u'上海', u'西安']
    # print(model.doesnt_match(list))

def processModelFile(filename1,vecfilename,vocabfilename):
    try:
        sfile = codecs.open(filename1, 'r', encoding='utf-8')
        vecfile = codecs.open(vecfilename, 'w', encoding='utf-8')
        vocabfile = codecs.open(vocabfilename, 'w', encoding='utf-8')
        line = sfile.readline() #跳过第一行
        line = sfile.readline()
        while(line):
            vecfile.write(line)
            vocabfile.write(line.split()[0] + '\n')
            line = sfile.readline()
        sfile.close()
        vecfile.close()
        vocabfile.close()
    except Exception as E:
        pass


if __name__ == "__main__":
    textfilename = u'data/分词后的语料.txt'
    modelfilename = 'data/word2vec_model'
    modelfilename2 = 'data/word2vec_model2'
    vecfilename = 'data/wiki.zh.vec'
    vocabfilename = 'data/source_vocab.txt'
    #train(textfilename,modelfilename,modelfilename2)
    #test(modelfilename)
    processModelFile(modelfilename2,vecfilename,vocabfilename)