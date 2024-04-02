# -*- coding: utf-8 -*-
import urllib.request
import urllib.parse
import json
import jieba
import numpy as np
import re


class Translation:
    @staticmethod
    def translate(text):
        if not text:
            return 'None'
        url = "https://fanyi.youdao.com/translate"
        params = {
            'i': text,
            'doctype': 'json',
            'from': 'AUTO',
            'to': 'AUTO'
        }
        data = urllib.parse.urlencode(params).encode('utf-8')
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        req = urllib.request.Request(url=url, data=data, headers=headers)
        response = urllib.request.urlopen(req)
        content = json.loads(response.read().decode('utf-8'))
        if content['errorCode'] == 0:
            result_tup = (item['tgt'] for item in content['translateResult'][0])
            result = ''.join(result_tup)
        else:
            result = 'Error'
        return result


class Judge:
    @staticmethod
    def get_word_vector(s1, s2):
        """
        :param s1: 句子1
        :param s2: 句子2
        :return: 返回句子的余弦相似度
        """
        # 分词
        cut1 = jieba.cut(s1)
        cut2 = jieba.cut(s2)
        list_word1 = (','.join(cut1)).split(',')
        list_word2 = (','.join(cut2)).split(',')

        # 列出所有的词,取并集
        key_word = list(set(list_word1 + list_word2))
        # 给定形状和类型的用0填充的矩阵存储向量
        word_vector1 = np.zeros(len(key_word))
        word_vector2 = np.zeros(len(key_word))

        # 计算词频
        # 依次确定向量的每个位置的值
        for i in range(len(key_word)):
            # 遍历key_word中每个词在句子中的出现次数
            for j in range(len(list_word1)):
                if key_word[i] == list_word1[j]:
                    word_vector1[i] += 1
            for k in range(len(list_word2)):
                if key_word[i] == list_word2[k]:
                    word_vector2[i] += 1

        # 输出向量
        # print(word_vector1)
        # print(word_vector2)
        return float(np.dot(word_vector1,word_vector2)/(np.linalg.norm(word_vector1)*np.linalg.norm(word_vector2)))

    @staticmethod
    def cos_dist(vec1,vec2):
        """
        :param vec1: 向量1
        :param vec2: 向量2
        :return: 返回两个向量的余弦相似度
        """

        return

    @staticmethod
    def filter_html(html):
        """
        :param html: html
        :return: 返回去掉html的纯净文本
        """
        dr = re.compile(r'<[^>]+>',re.S)
        dd = dr.sub('', html).strip()
        return dd


if __name__ == "__main__":
    while True:
        text = input('翻译内容：')
        result = Translation.translate(text)
        test = Translation.translate(result)
        print("翻译结果：%s" % test)
        judge = Judge
        print(judge.get_word_vector(text, test))

