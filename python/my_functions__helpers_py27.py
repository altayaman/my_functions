'''
import sys
sys.path.insert(0, './my_functions')
from my_functions__helpers_py27 import transliterate_rus2latin
'''


# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def transliterate_rus2latin(rus_str):
    a = {}

    a["а"]="a"
    a["б"]="b"
    a["в"]="v"
    a["г"]="g"
    a["д"]="d"
    a["е"]="e"
    a["ё"]="yo"
    a["ж"]="zh"
    a["з"]="z"
    a["и"]="i"
    a["й"]="i"
    a["к"]="k"
    a["л"]="l"
    a["м"]="m"
    a["н"]="n"
    a["о"]="o"
    a["п"]="p"
    a["р"]="r"
    a["с"]="s"
    a["т"]="t"
    a["у"]="u"
    a["ф"]="f"
    a["х"]="h"
    a["ц"]="ts"
    a["ч"]="ch"
    a["ш"]="sh"
    a["щ"]="sch"
    a["ъ"]="'"
    a["ы"]="i"
    a["ь"]="'"
    a["э"]="e"
    a["ю"]="yu"
    a["я"]="ya"

    a["А"]="a"
    a["Б"]="B"
    a["В"]="V"
    a["Г"]="G"
    a["Д"]="D"
    a["Е"]="E"
    a["Ё"]="YO"
    a["Ж"]="ZH"
    a["З"]="Z"
    a["И"]="I"
    a["Й"]="I"
    a["К"]="K"
    a["Л"]="L"
    a["М"]="M"
    a["Н"]="N"
    a["О"]="O"
    a["П"]="P"
    a["Р"]="R"
    a["С"]="S"
    a["Т"]="T"
    a["У"]="U"
    a["Ф"]="F"
    a["Х"]="H"
    a["Ц"]="TS"
    a["Ч"]="CH"
    a["Ш"]="SH"
    a["Щ"]="SCH"
    a["Ъ"]="'"
    a["Ы"]="I"
    a["Ь"]="'"
    a["Э"]="E"
    a["Ю"]="YU"
    a["Я"]="Ya"

    trans_str = ''

    for c in rus_str:
        if(c in a.keys()):
            trans_str = trans_str + '_' + a[c.encode('utf-8')]

    return trans_str[1:]



