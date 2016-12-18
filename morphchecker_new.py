import re
import pymorphy2
from collections import defaultdict, namedtuple
from prjscript import morphSplitnCheck, kuznec
import sys
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
                                                )
                                           )
            
        self.morphs_for_tag = self.extend(morphs_for_tag)
        self.rules_for_code = rules_for_code

 
    def rules_for_lemma(self, lemma, grams=[]):               
        return [rule
                for code in self.codes_for_lemma[lemma]
                for rule in self.rules_for_code[code]
                if rule.gram in grams]
    
    def tags_for_morph(self, morph):
        return {tag
                for tag in self.morphs_for_tag
                if morph in self.morphs_for_tag[tag]}

    def pos_for_lemma(self, lemma):
        return self.rules_for_lemma(lemma)[0].gram[:4]            

    def apply_rule(self, rule, lemma):
        if re.search(rule.condition.replace('0', '') + '$', lemma) != None:
            return re.sub(rule.old.replace('0', '') + '$', rule.new, lemma)

    def extend(self, grammar):
        no_adj_noun = {'ая', 'яя', 'ее', 'ое', 'и', 'ы', 'ев', 'ей', 'ем', 'ом', 'ов', 'ет'}
        no_verb = {'и'}
        grammar['ADJF.им.п.м.р.'] = grammar['ADJF.им.п.м.р.'].difference(no_adj_noun)
        grammar['NOUN.им.п.м.р.'] = grammar['NOUN.им.п.м.р.'].difference(no_adj_noun) 
        grammar['VERB.инф.'] = grammar['VERB.инф.'].difference(no_verb)
        grammar['NOUN.ед.ч.т.п.'].update(['ией', 'ием'])        # МОЖЕТ И НЕ ПРИГОДИТЬСЯ
        grammar['NOUN.мн.ч.р.п.'].update(['иев'])               # для случаев типа "загрязненией", "фантазием"
        grammar['ADJF.мн.ч.т.п.'].update(['ами', 'имы'])        # для случаев типа "руссками"
        return grammar

    
class Allomorphs(kuznec):
   
    def __init__(self):
        self.allomorphs = defaultdict(str,
                                       {self.worddict[item][place]['morph']:self.worddict[item][place]['allo']
                                        for item in self.worddict
                                        for place in self.worddict[item]
                                        if 'status' in self.worddict[item][place]
                                        and self.worddict[item][place]['status'] == 'корень'
                                        and self.worddict[item][place]['allo']
                                        }
                                       )
        
    def is_allomorph(self, variant_root, error_root):
        regexp = '^(' + re.sub('[0-9]', '', self.allomorphs[error_root]) + ')'
        if re.match(regexp, variant_root) != None:
            return True


class Morphchecker:
    
    def __init__(self):
        self.pm2 = pymorphy2.MorphAnalyzer()
        self.rb = Rulebook()
        self.al = Allomorphs()

    def spellcheck(self, word):
        spellchecked = check_word(word, ' ', ' ',
                                  accent_mistakes={},
                                  big_ru={},
                                  multiword=False)
        if spellchecked['correct']:
            return spellchecked['correct'], True
        else:
            return spellchecked['mistake'], False
        
    def lemma_merge(self, variants):
        return list({self.pm2.parse(re.sub('[^а-яА-Я]', ' ', variant))[0].normalized.word.replace('ё', 'е')
                    for variant in variants})

    def init_forms(self, tags):
        for init_form in ['NOUN.им.п.м.р.', 'ADJF.им.п.м.р.', 'ADJS.им.п.м.р.', 'VERB.инф.']:
            if init_form in tags:
                return True
            
    def morphcheck(self, word):        
        word = word.replace('ё', 'е')
        morphs = morphSplitnCheck(word)
        tags = self.rb.tags_for_morph(morphs.postfix)
        spellchecked, is_correct = self.spellcheck(word)
        
        if is_correct == True:
            suggestions = spellchecked
        else:
            suggestions = []
            for lemma in self.lemma_merge(spellchecked):
                if self.al.is_allomorph(morphSplitnCheck(lemma).root, morphs.root) == True:
                    for rule in self.rb.rules_for_lemma(lemma, grams=tags):
                        corrected = self.rb.apply_rule(rule, lemma)
                        if corrected is not None:
                            suggestions.append(corrected.replace('0', ''))
                if self.init_forms(tags):
                    suggestions.append(lemma)                    
            
        return suggestions
   
    def tokenize(self, text):
        import string
        text = text.lower().split()
        return [token.strip(string.punctuation).replace('ё', 'е')
                for token in text if token not in string.punctuation]    

    def text_morphcheck(self, text):
        return [(word, self.morphcheck(word)) for word in self.tokenize(text)]

    def file_morphcheck(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return text_morphcheck(file.read())
