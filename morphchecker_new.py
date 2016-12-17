import re
import pymorphy2
import nltk
import time
import sys
from collections import defaultdict, namedtuple
from prjscript import morphSplitnCheck, kuznec
sys.path.append('C:/Users/Ivankov/Documents/GitHub/heritage_morphchecker2.0/spellchecker')
from spell_checker import check_word 

class Rulebook:
    
    def __init__(self):
                    
        with open('C:/Users/Ivankov/Documents/GitHub/heritage_morphchecker2.0/resources/ru_RU.dic', 'r', encoding='UTF-8') as lines:
            wordlist = [line.split('/') for line in lines if '/' in line]
        
        self.codes_for_lemma = defaultdict(list,
                                           {entry[0]:re.findall('[A-Za-z]{2}', entry[1].strip('\n'))
                                            for entry in wordlist}
                                           )
            
        with open('C:/Users/Ivankov/Documents/GitHub/heritage_morphchecker2.0/resources/ru_RU.aff', 'r', encoding='UTF-8') as rawRules:
            rules = [rawRule.split() for rawRule in rawRules
                     if 'SFX' in rawRule and ' Y ' not in rawRule]
            
        morphs_for_tag = defaultdict(set)
        rules_for_code = defaultdict(list)
        Rule = namedtuple('Rule', ['old', 'new', 'condition', 'gram'])
        
        for rule in rules:
            
            tag = rule[5].strip('()')
            morph = re.sub('[//[a-zA-Z]]*', '', rule[3]) # нужно убрать символы после слэша
            
            POS = tag[:5]
            if POS in ['NOUN.', 'ADJF.', 'ADJS.']:
                morphs_for_tag[POS + 'им.п.м.р.'].add(rule[2])
            elif POS == 'VERB.':
                morphs_for_tag[POS + 'инф.'].add(rule[2])
            
            morphs_for_tag[tag].add(morph)
                        
            rules_for_code[rule[1]].append(Rule(old=rule[2],
                                                new=morph,
                                                condition=rule[4], 
                                                gram=tag
                                                ))
        self.morphs_for_tag = self.extend(morphs_for_tag)
        self.rules_for_code = rules_for_code

 
    def rules_for_lemma(self, lemma):               
        return [rule
                for code in self.codes_for_lemma[lemma]
                for rule in self.rules_for_code[code]]
    
    def tags_for_morph(self, morph):
        return {tag
                for tag in self.morphs_for_tag
                if morph in self.morphs_for_tag[tag]}

    def pos_for_lemma(self, lemma):
        return self.rules_for_lemma(lemma)[0].gram[:4]            

    def apply_rule(self, rule, lemma, grams=[]):
        if re.search(rule.condition.replace('0', '') + '$', lemma) != None:
            return re.sub(rule.old.replace('0', '') + '$', rule.new, lemma)

    def extend(self, grammar):
        no_adj_noun = {'ая', 'яя', 'ее', 'ое', 'и', 'ы', 'ев', 'ей', 'ем', 'ом', 'ов', 'ет'}
        grammar['ADJF.им.п.м.р.'] = grammar['ADJF.им.п.м.р.'].difference(no_adj_noun)
        grammar['NOUN.им.п.м.р.'] = grammar['NOUN.им.п.м.р.'].difference(no_adj_noun) 
        no_verb = {'и'}
        grammar['VERB.инф.'] = grammar['VERB.инф.'].difference(no_verb)

        # ====================МОЖЕТ И НЕ ПРИГОДИТЬСЯ
        # для случаев типа "загрязненией", "фантазием"
        grammar['NOUN.ед.ч.т.п.'].add('ией')
        grammar['NOUN.ед.ч.т.п.'].add('ием')
        grammar['NOUN.мн.ч.р.п.'].add('иев')
        # для случаев типа "руссками"
        grammar['ADJF.мн.ч.т.п.'].add('ами')
        grammar['ADJF.мн.ч.т.п.'].add('имы')
        return grammar


class Morphchecker():
    
    def __init__(self):
        self.stemmer = nltk.stem.snowball.RussianStemmer(ignore_stopwords=False)
        self.pm2 = pymorphy2.MorphAnalyzer()
        self.al = Allomorphs()
        self.rb = Rulebook()

    def spellcheck(self, word):
        spellchecked = check_word(word, ' ', ' ',
                                  accent_mistakes={}, big_ru={},
                                  multiword=False)
        if spellchecked['correct']:
            return spellchecked['correct']
        else:
            return spellchecked['mistake']
        
    def lemma_merge(self, variants):
        return list({self.pm2.parse(re.sub('[^а-яА-Я]', ' ', variant))[0].normalized.word.replace('ё', 'е')
                    for variant in variants})

    def root_filter(self, variant):
        variant_morphs = morphSplitnCheck(variant)
        variant_root = variant_morphs.root

    def is_allomorph(self):
        # if is_allomorph(lemma, root, variant_root, allomorph_dict[0]) == True:
        pass        

    def morphcheck(self, word):
        ending = morphSplitnCheck(word).postfix
        suggestions = set()
        for lemma in self.lemma_merge(self.spellcheck(word)):
            tags = self.rb.tags_for_morph(ending)
            for rule in self.rb.rules_for_lemma(lemma):
                corrected = self.rb.apply_rule(rule, lemma, grams=tags)
                if corrected is not None:
                    suggestions.add(corrected.replace('0', ''))
        return suggestions
   
    def tokenize(self, text):
        import string
        text = text.lower().split()
        text = [token.strip(string.punctuation).replace('ё', 'е')
                for token in text if token not in string.punctuation]    

    def text_morphcheck(self, text):
        # output = {word:morphcheck(word) for word in text}
        return [(word, self.morphcheck(word)) for word in self.tokenize(text)]


class Allomorphs(kuznec):
   
    def __init__(self):
        self.allomorphs = defaultdict('',
                                      {self.worddict[item]['morph']:self.worddict[item]['allo']
                                       for item in self.worddict
                                       if 'status' in self.worddict[item]
                                       and self.worddict[item]['status'] == 'корень'}
                                      )


    
                           
"""


def load_allomorphs():
    with open('C:/Users/Ivankov/Documents/GitHub/heritage_morphchecker2.0/morphodict.csv', 'r', encoding='utf-8') as morphodict:
        allom_dict = [line.split(';') for line in morphodict]

        allomorphs = {}
        roots = set()
        for part in allom_dict:
            if part[2] == 'корень':
                if part[4] != '':
                    allomorphs[part[0]] = part[4].replace('ё', 'е')
                else:
                    if part[0] not in allomorphs:
                        allomorphs[part[0]] = part[1].replace('ё', 'е')
                roots.add(part[1])
        return allomorphs, roots    


# проверяет, совпадают ли корни или алломорфы


def is_allomorph(lemma, root, variant_root, allomorph_dict):
    if lemma in allomorph_dict:  # если лемма есть в словаре Кузнецовой
        # регулярка - список алломорфов для леммы (вод|важд|вед)
        regexp = '^(' + re.sub('[0-9]', '', allomorph_dict[lemma]) + ')'
        print('Возможные алломорфы корня %s: %s \n' % (root, regexp))

        if re.match(regexp, root) != None and re.match(regexp, variant_root) != None:
            sys.stdout.write('Корень ' + root + ' - алломорф корня ' + variant_root + '\n')
            return True              
        else:
            sys.stdout.write('Не аллломорф' + '\n')
            if root == variant_root:
                sys.stdout.write('Один и тот же корень' + '\n')
                return True
            
            else:
                sys.stdout.write(root + ' не равно ' + variant_root + '\n')
                sys.stdout.write('Корни разные' + '\n')
                return False
    else:
        sys.stdout.write('Леммы нет в словаре Кузнецовой' + '\n')
        if root == variant_root:
            sys.stdout.write('Один и тот же корень' + '\n')
            return True
        else:
            sys.stdout.write(root + ' не равно ' + variant_root + '\n')
            sys.stdout.write('Корни разные' + '\n')
            return False 
"""
