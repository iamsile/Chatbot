# coding=utf-8

import json
import logging
import os

from .match import *
from .responsesEvaluate import Evaluator

class Answerer(object):

    def __init__(self):

        self.general_questions = []
        self.path = os.path.dirname(__file__)

        self.matcher = getMatcher(matcherType="Fuzzy")
        self.evaluator = Evaluator()
        self.moduleTest()

    def moduleTest(self):
        logging.info("測試問答與斷詞模塊中...")
        try:
            self.matcher.wordSegmentation("測試一下斷詞")
            logging.info("測試成功")
        except Exception as e:
            logging.info(repr(e))
            logging.info("模塊載入失敗，請確認data與字典齊全")

    def getResponse(self, sentence, api_key=None):

        if api_key is None:
            response = self.getGeneralQA(sentence)
        else:
            response = self.getCustomQA(sentence,api_key)
        return response

    def getGeneralQA(self,query,threshold=0):

        title,index = self.matcher.match(query)
        sim = self.matcher.getSimilarity()
        if sim < threshold:
            return None,0
        else:
            res = json.load(open(os.path.join(self.path+"/data/processed/reply/",str(int(index/1000))+'.json'),
                            'r',encoding='utf-8'))
            targetId = index % 1000
            candiates = self.evaluator.getBestResponse(res[targetId],topk=3)
            reply = self.randomPick(candiates)
            return reply,sim

    def randomPick(self, answers):
        try:
            answer = answers[random.randrange(0,len(answers))][0]
        except:
            answer = None
        return answer

    def getCustomQA(self, sentence, api_key, threshold=50):

        #TODO GET USER'S QA BY api_key
        #FIXME REPLACE TESTING DATA TO FORMAL ONE(GET BY DATABASE).
        #i.e IMPLEMENT getUserQA(api_key)
        #customqa_list = json.loads(getUserQA(api_key))

        data = '[{"Question":"你媽長得像魚人","Answers":["你媽也長得像魚人","你比痲瘋地精還臭"]}]'
        customqa_list = json.load(data)

        return None,0
