# -*- coding: utf-8 -*-

import pymorphy2

# text = 'сегодня,завтра,вчера,неделя,год,месяц,я,работа,учёба,рутина,обычно,обед,завтрак,ужин,занятый,стандартно,распорядок,обязанность,устать,план,школа,семья,ребёнок,родитель,позвонить,дело,друг,коллега,привычка,еда,расписание,спорт,отдых,режим,магазин,вечер,телевизор,пиво,футбол,компьютер,развлечение,игра,туалет,стресс,хобби,литература,книга,время,час,часы,новость,сеть,лента,транспорт,метро,автобус,здоровье,больница,поликлиника,питание,приём,интернет,wi-fi,сон,кровать,постель,проблема,эмоция,задача,саморазвитие,жизнь,стремление,'

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
