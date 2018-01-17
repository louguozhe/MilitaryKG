import fool

def processSentence(sentence):
    #print(fool.cut(sentence))
    #print(fool.pos_cut(sentence))
    try:
        print(fool.cut(sentence))
        print(fool.pos_cut(sentence))
        words, ners = fool.analysis(sentence)
        print(words,ners)
    except:
        pass

if __name__ =="__main__":
    try:
        fool.load_userdict('data/userDictForFool.txt')
        pass
    except:
        pass
    #processSentence("一个傻子在北京")
    processSentence("日媒：中国第3艘航母已开建 不仅是模仿辽宁舰")
    processSentence("新华社：冷战时代美苏“星球大战” 前苏联被拖入军备竞赛")
