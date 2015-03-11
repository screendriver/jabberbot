import os
import random as rndm


def random():
    """Random language code and country"""
    dirpath = os.path.dirname(os.path.realpath(__file__))
    filepath = os.path.join(dirpath, 'lang_codes.txt')
    with open(filepath) as f:
        lines = [tuple(line.strip().split(';')) for line in f]
        langs = dict(lines)
    lang_code = rndm.choice(list(langs))
    country = langs[lang_code]
    return lang_code, country
