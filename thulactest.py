#coding:utf-8

import thulac

# 词性标记
# n/名词 np/人名 ns/地名 ni/机构名 nz/其它专名
# m/数词 q/量词 mq/数量词 t/时间词 f/方位词 s/处所词
# v/动词 a/形容词 d/副词 h/前接成分 k/后接成分 i/习语
# j/简称 r/代词 c/连词 p/介词 u/助词 y/语气助词
# e/叹词 o/拟声词 g/语素 w/标点 x/其它

if __name__ =="__main__":
    userdict = 'models//userDict.txt'
    thu1 = thulac.thulac(seg_only=False,user_dict=userdict, model_path="models")  # 设置模式为行分词模式
    a = thu1.cut("日媒：中国第3艘航母已开建 不仅是模仿辽宁舰")
    print(a)
    a = thu1.cut("社评：支持解放军改革，期待中国不怒自威")
    print(a)
    a = thu1.cut("冷战时代美苏“星球大战” 前苏联被拖入军备竞赛")
    print(a)
