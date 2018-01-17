from tools.LTP_API import TextAnalysisByLTP
import json
from tools.nerByLTP import Extractor

def processSentence(ltp,sentence):
    # result, code = ltp.get(sentence,'ws') #分词
    # print(result)
    # result, code = ltp.get(sentence,'pos') #词性标注
    # print(result)
    # result, code = ltp.get(sentence,'ner') #命名实体识别
    # print(result)
    # result, code = ltp.get(sentence,'dp') #依存句法分析
    # print(result)
    # result, code = ltp.get(sentence,'sdp') #语义依存树分析
    # print(result)
    # result, code = ltp.get(sentence,'sdb_graph')#语义依存图分析
    # print(result)
    # result, code = ltp.get(sentence,'srl')#语义角色标注
    # print(result)
    result, code = ltp.get(sentence,'all')#全部任务
    print(result)
    # if code == 200:
    #     words = result.split(' ')
    #     for word in words:
    #         print('word: %s' % word)

if __name__ =="__main__":
    ltp = TextAnalysisByLTP('ad','dfas','xml')

    #基于LTP云接口
    processSentence(ltp,'今年1月1日，广州动物园驯兽表演场里发生了一起猛虎伤人事故，引起了市民的关注。')
    #processSentence(ltp,'冷战时代美苏“星球大战” 前苏联被拖入军备竞赛')

    #基于本地模型
    # data = u"今年1月1日，广州动物园驯兽表演场里发生了一起猛虎伤人事故，引起了市民的关注。"
    # extractor = Extractor()
    # extractor.load()
    # extractor.chunk_str(data)
    # extractor.resolve_all_conference()
    # print("Triple: ")
    # print('\n'.join(str(p) for p in extractor.triple_list))
    #
    # extractor.release()



