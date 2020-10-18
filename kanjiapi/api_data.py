import ujson
from collections import defaultdict, OrderedDict
from lxml import etree
import csv
from .entry_data import word_dict


NANORI = etree.XPath('./reading_meaning//nanori')
ON_READINGS = etree.XPath('./reading_meaning//reading[@r_type="ja_on"]')
KUN_READINGS = etree.XPath('./reading_meaning//reading[@r_type="ja_kun"]')
MEANINGS = etree.XPath('./reading_meaning//meaning[not(@m_lang)]')
GRADE = etree.XPath('./misc/grade')
STROKE_COUNT = etree.XPath('./misc/stroke_count')
CODEPOINT = etree.XPath('.//cp_value[@cp_type="ucs"]')
JLPT = etree.XPath('./misc/jlpt')
LITERAL = etree.XPath('literal')


def nanori(character):
    readings = NANORI(character)
    return [reading.text for reading in readings]


def on_readings(character):
    readings = ON_READINGS(character)
    return [reading.text for reading in readings]


def kun_readings(character):
    readings = KUN_READINGS(character)
    return [reading.text for reading in readings]


def meanings(character):
    meanings = MEANINGS(character)
    return [meaning.text for meaning in meanings]


def grade(character):
    try:
        return int(GRADE(character)[0].text)
    except (AttributeError, IndexError):
        return None


def stroke_count(character):
    return int(STROKE_COUNT(character)[0].text)


def unicode_codepoint(character):
    return CODEPOINT(character)[0].text


heisig_keywords = None

def heisig_keyword(character_literal):
    global heisig_keywords

    if not heisig_keywords:
        with open('heisig.tsv', 'r', encoding='utf8') as f:
            heisig_keywords = { character: keyword
                              for character, keyword
                              in csv.reader(f, delimiter='\t') }

    return heisig_keywords.get(character_literal)


def jlpt(character):
    try:
        return int(JLPT(character)[0].text)
    except (AttributeError, IndexError):
        return None


def literal(character):
    return LITERAL(character)[0].text


def kanji_data(character):
    character_literal = literal(character)

    return OrderedDict([
        ('kanji', character_literal),
        ('kun_readings', kun_readings(character)),
        ('on_readings', on_readings(character)),
        ('name_readings', nanori(character)),
        ('jlpt', jlpt(character)),
        ('unicode', unicode_codepoint(character)),
        ('heisig_en', heisig_keyword(character_literal)),
        ])


def reading_data(kanjis):
    readings = defaultdict(lambda: {'regular': [], 'name': []})

    for kanji in kanjis:
        literal = kanji['kanji']
        for reading in kanji['kun_readings'] + kanji['on_readings']:
            readings[reading]['regular'].append(literal)
        for reading in kanji['name_readings']:
            readings[reading]['name'].append(literal)

    return [OrderedDict([
        ('reading', reading),
        ('main_kanji', data['regular']),
        ('name_kanji', data['name']),
        ]) for reading, data in readings.items()]


def CJK_compatibility(character):
    return u'\uF900' <= literal(character) <= u'\uFAFF'


def dump_json(filename, obj):
    with open(filename, 'w', encoding='utf8') as f:
        # f.write(str(obj)) # Works - writes Python OrderedDict to file
        # f.write(ujson.dumps(obj, ensure_ascii=False))
        ujson.dump(obj, f, ensure_ascii=False)


def main():
    VERSION_PATH = 'v1'
    KANJI_DIR = 'out/' + VERSION_PATH + '/kanji/'
    WORD_DIR = 'out/' + VERSION_PATH + '/words/'
    READING_DIR = 'out/' + VERSION_PATH + '/reading/'
    JOUYOU_GRADES = [1, 2, 3, 4, 5, 6, 8]
    JINMEIYOU_GRADES = [9, 10]

    kanjidic_root = etree.parse('kanjidic2.xml')
    characters = kanjidic_root.xpath('./character')

    kanjis = [
            kanji_data(character)
            for character in characters
            if not CJK_compatibility(character)
            ]

    # readings = reading_data(kanjis)

    all_kanji = [kanji['kanji'] for kanji in kanjis]

    # for kanji in kanjis:
        # print('Kanji ' + str(kanji['unicode']))
        # dump_json(KANJI_DIR + kanji['kanji'], kanji)

    dump_json(KANJI_DIR + 'main.json', kanjis)
    #dump_json(KANJI_DIR + 'all', all_kanji)

