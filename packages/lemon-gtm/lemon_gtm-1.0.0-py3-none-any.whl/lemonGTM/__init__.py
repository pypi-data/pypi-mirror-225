import jieba
import pickle

class core:
    def __init__(self, fileName):
        self.datas = []
        with open(fileName, 'r', encoding = 'utf-8') as f:
            self.datas = f.readlines()
            
    def analysis(self, word):
        result = []
        for keywordForWord in list(jieba.cut_for_search(word)):
            for data in self.datas:
                for keywordForData in list(jieba.cut_for_search(data)):
                    if keywordForWord == keywordForData:
                        flag = False
                        for keyword in result:
                           if keyword['result'] == data:
                            flag = True
                            keyword['priority'] += 1
                        if flag == False:
                            result.append({'result': data, 'priority': 1})
        result.sort(key = lambda x: x['priority'], reverse = True)
        return result