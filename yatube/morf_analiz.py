# -*- coding: utf-8 -*-

import pymorphy2

# text = ''


def lemmatize(text):
    morph = pymorphy2.MorphAnalyzer()
    text = text.replace(",", " ")
    text = text.replace(".", " ")
    text = text.replace("!", " ")
    text = text.replace("?", " ")
    words = text.split()
    result = []
    for word in words:
        p = morph.parse(word)[0]
        result.append(p.normal_form)

    result1 = []
    for x in result:
        if x not in result1:
            result1.append(x)

    return result1


# print(",".join(lemmatize(text)))
