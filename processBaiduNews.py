# -*- coding: utf-8 -*-
import jieba
import os
from tools.mysqlHelper import MySqlHelper
import fool
from Neo4JHelper import Neo4JConnector,KGImporter
from tools.nerByLTP import Extractor

def fenciNewsTitle(mysqlHelper):
    try:
        rows = mysqlHelper.FetchRows('select url,title from newsdetail')
        for row in rows:
            url = row[0]
            title = row[1]
            title_cut = ' '.join(jieba.cut(title))
            updatesql = "update newsdetail set title_cut=%s where url=%s"
            mysqlHelper.ExecuteNonSQL(updatesql,[title_cut,url])
            mysqlHelper.Commit()
    except Exception as e:
        print(e)

def exportNewsTitle(mysqlHelper,filename):
    try:
        rows = mysqlHelper.FetchRows('select title from newsdetail')
        file = open(filename,'w',encoding='utf8')
        for row in rows:
            title = row[0]
            if '|' in title:
                title = title[:title.find('|')]
            if '-' in title:
                title = title[:title.find('-')]
            title = str(title).strip()
            title = title.replace('\n','')
            if len(title)>6:
                file.write(title + '。\n')
        file.close()
    except Exception as e:
        print(e)

def cutNewsTitleByFool(fromfilename,tofilename):
    try:
        ffile = open(fromfilename,'r',encoding='utf8')
        tfile = open(tofilename,'w',encoding='utf8')
        title = ffile.readline()
        while title:
            tfile.write(' '.join(fool.cut(title)))
            title = ffile.readline()
        ffile.close()
        tfile.close()
    except Exception as e:
        print(e)

def cutNewsTitleByJieba(fromfilename,tofilename,dicfilename=None):
    try:
        if dicfilename:
            jieba.load_userdict(dicfilename)
        ffile = open(fromfilename,'r',encoding='utf8')
        tfile = open(tofilename,'w',encoding='utf8')
        title = ffile.readline()
        while title:
            tfile.write(' '.join(jieba.cut(title)))
            title = ffile.readline()
        ffile.close()
        tfile.close()
    except Exception as e:
        print(e)

def exportNewsFromDB(filename):
    mysqlHelper = MySqlHelper()
    mysqlHelper.InitConnectParameter('root','root','baidunews')
    mysqlHelper.Connect()
    exportNewsTitle(mysqlHelper,filename)
    mysqlHelper.Close()

def exportDictFromNeo4j(filename):
    connector = Neo4JConnector()
    connector.connect()
    queryResult = connector.queryCypher("match (n) return n.name as name")
    tfile = open(filename, 'w', encoding='utf8')
    for record in queryResult:
        tfile.write(record['name'] + '\n')
    tfile.close()
    connector.disconnect()

def processSencenceToWords(extractor,sentence):
    words = extractor.segment(sentence)
    return words

def processWords(extractor,words):
    try:
        postags = extractor.postag(words)
        arcs = extractor.parse(words,postags)
        netags = extractor.recognize(words, postags)
        roles = extractor.label(words, postags,netags, arcs)
        lablestr = ''
        for role in roles:
            #print(role.index, "\t".join(["%s:(%d,%d)" % (arg.name, arg.range.start, arg.range.end) for arg in role.arguments]))
            lablestr = lablestr + '%d(%s)' % (role.index,words[role.index]) + "\t".join(["%s:(%s)" % (arg.name, ''.join(words[arg.range.start: arg.range.end+1])) for arg in role.arguments]) + '\t\t'
        return lablestr
    except Exception as e:
        return ' Error:' + ' '.join(words)

def lableNewsTitle(cutfilename,tofilename,cut=True):
    try:
        extractor = Extractor()
        extractor.load()

        cfile = open(cutfilename,'r',encoding='utf8')
        tfile = open(tofilename,'w',encoding='utf8')
        linestr = cfile.readline()
        while linestr:
            if len(linestr)> 1:
                linestr =linestr[:len(linestr)-1]
            linestr= linestr.strip()
            if len(linestr) > 5:
                words = None
                if cut:
                    words = processSencenceToWords(extractor,linestr)
                else:
                    words = linestr.split(' ')
                lablestr = processWords(extractor,words)
                tfile.write(lablestr + '\n')
            linestr = cfile.readline()
        cfile.close()
        tfile.close()
        extractor.release()
    except Exception as e:
        print(e)

def lableText(text,tofilename=None):
    try:
        extractor = Extractor()
        extractor.load()
        sentences = extractor.sentenceSplite(text)
        tfile = None
        if tofilename:
            tfile = open(tofilename,'w',encoding='utf8')
        for sentence in sentences:
            words = processSencenceToWords(extractor, sentence)
            print(' '.join(words))
            lablestr = processWords(extractor, words)
            if tfile:
                tfile.write(lablestr + '\n')
            else:
                print(lablestr)
        if tfile:
            tfile.close()
        extractor.release()
    except Exception as e:
        print(e)

if __name__ =="__main__":
    #exportNewsFromDB('data/milnewstitle.txt')
    #fenciNewsTitle(mysqlHelper)
    #exportDictFromNeo4j('data/userDictForJieba1.txt')
    #cutNewsTitleByJieba('data/milnewstitle.txt','data/milnewstitle_cut.txt','data/userDictForJieba1.txt')

    #lableNewsTitle('data/milnewstitle_cut.txt','data/milnewstitle_lable.txt',cut=False)
    #lableNewsTitle('data/weixinnews.txt','data/milnewstitle_lable1.txt',cut=True)
    lableText(u'今年1月1日，广州动物园驯兽表演场里发生了一起猛虎伤人事故，引起了市民的关注')