# -*- coding: utf-8 -*-

import pymorphy2

morph = pymorphy2.MorphAnalyzer()

text = 'сборы'


def lemmatize(text):
    words = text.split(',')
    result = []
    for word in words:
        p = morph.parse(word)[0]
        result.append(p.normal_form)

    result1 = []
    for x in result:
        if x not in result1:
            result1.append(x)

    return result1


print(','.join(lemmatize(text)))
