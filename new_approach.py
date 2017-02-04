import re
import pymorphy2
from collections import defaultdict, namedtuple
from prjscript import morphSplitnCheck, kuznec
import sys
sys.path.append('C:/Users/Ivankov/Documents/GitHub/heritage_morphchecker2.0/spellchecker')
from spell_checker import check_word
from rules import context_rules

Rule = namedtuple('Rule', ['old', 'new', 'condition', 'gram'])

class Rulebook:
    
    def __init__(self):
                    
        with open('C:/Users/Ivankov/Documents/GitHub/heritage_morphchecker2.0/resources/ru_RU.dic', 'r', encoding='UTF-8') as lines:
            wordlist = [line.split('/') for line in lines if '/' in line]
        
        self.codes_for_lemma = defaultdict(list,
                                           {entry[0]:re.findall('[A-Za-z]{2}', entry[1].strip('\n'))
                                            for entry in wordlist}
                                           )
            
        with open('C:/Users/Ivankov/Documents/GitHub/heritage_morphchecker2.0/resources/ru_RU.aff', 'r', encoding='UTF-8') as raw:
            sfx_rules = [line.split() for line in raw
                         if 'SFX' in line and ' Y ' not in line]
            
        with open('C:/Users/Ivankov/Documents/GitHub/heritage_morphchecker2.0/resources/ru_RU.aff', 'r', encoding='UTF-8') as raw:
            pfx_rules = [line.split() for line in raw
                         if 'PFX' in line and ' Y ' not in line]            
            
        morphs_for_tag = defaultdict(set)
        rules_for_code = defaultdict(list)
        Rule = namedtuple('Rule', ['old', 'new', 'condition', 'gram'])
        
        for rule in sfx_rules:
                       
            morph = re.sub('[//[a-zA-Z]]*', '', rule[3]) # нужно убрать символы после слэша
            tag = rule[5].strip('()') 

            POS = tag[0]
            if POS in ['N', 'A']:
                morphs_for_tag[POS + '.им.п.м.р.'].add(rule[2])
            elif POS == 'V':
                morphs_for_tag[POS + '.инф.'].add(rule[2])
            
            morphs_for_tag[tag].add(morph)
                        
            rules_for_code[rule[1]].append(Rule(old = rule[2].replace('0', ''),
                                                new = morph.replace('0', ''),
                                                condition = rule[4].replace('0', ''), 
                                                gram = tag
                                                )
                                           )
            
        self.morphs_for_tag = self.extend(morphs_for_tag)
        self.rules_for_code = rules_for_code

        prefixes = defaultdict(set)
        for pfx_rule in pfx_rules:
            prefixes[pfx_rule[1]].add(pfx_rule[3])
            
        self.prefixes = prefixes

 
    def tags_for_morph(self, morph):
        return {tag
                for tag in self.morphs_for_tag
                if morph in self.morphs_for_tag[tag]}

    def rules_for_lemma(self, lemma, grams=[]):
        if grams == 'all':
            rules = [rule
                     for code in self.codes_for_lemma[lemma]
                     for rule in self.rules_for_code[code]
                     if re.search(rule.condition + '$', lemma) != None]
        else:
            rules = [rule
                     for code in self.codes_for_lemma[lemma]
                     for rule in self.rules_for_code[code]
                     if re.search(rule.condition + '$', lemma) != None
                     and rule.gram in grams]

        for init_form in ['V.инф.', 'N.им.п.м.р.', 'A.им.п.м.р.']:
            if init_form in grams and self.pos_for_lemma(lemma) == init_form[0]:
                rules.append(Rule(old='', new='', condition='', gram=init_form))

        return rules
            

    def morphs_for_lemma(self, lemma):
        return {rule.new
                for rule in self.rules_for_lemma(lemma, grams='all')}

    def pos_for_lemma(self, lemma):
        try: 
            return self.rules_for_code[self.codes_for_lemma[lemma][0]][0].gram[0]
        except:
            try:
                al = Allomorphs()
                if al.worddict[lemma]:
                    return al.worddict[lemma]['1']['pos']
            except:
                print('Лемма отсутствует! Часть речи неизвестна! \n')
                return None

    def find_sfx(self, word):
        all_sfxs = {morph
                    for tag in self.morphs_for_tag
                    for morph in self.morphs_for_tag[tag]
                    if re.search(morph+'$', word) is not None}
        sfxs_sorted = list(reversed(sorted(all_sfxs, key=len)))
        return [(sfx, len(sfxs_sorted)-i) for i, sfx in enumerate(sfxs_sorted)]
    
    def try_all(self, possible, lemma):
        corrected = []
        used = set()
        for sfx in possible:
            tags = self.tags_for_morph(sfx[0])
            for rule in self.rules_for_lemma(lemma, grams=tags.difference(used)):
                cor = self.apply_rule(rule, lemma)
                if cor is not None:
                    corrected.append((cor, sfx[1]))
            used = used.union(tags)
        return sorted(corrected, key=lambda x:x[1], reverse=True)

    def apply_rule(self, rule, lemma):
        replaced = re.subn(rule.old + '$', rule.new, lemma)
        if replaced[1]:
            return replaced[0]

    def extend(self, grammar):
        no_adj_noun = {'ая', 'яя', 'ее', 'ое', 'и', 'ы', 'ев', 'ей', 'ем', 'ом', 'ов', 'ет', 'ли', 'ла', 'ло', 'ной', 'ни'}
        no_verb = {'и'}
        grammar['A.им.п.м.р.'] = grammar['A.им.п.м.р.'].difference(no_adj_noun)
        grammar['N.им.п.м.р.'] = grammar['N.им.п.м.р.'].difference(no_adj_noun) 
        grammar['V.инф.'] = grammar['V.инф.'].difference(no_verb)
        grammar['N.ед.ч.т.п.'].update(['ией', 'ием'])        # МОЖЕТ И НЕ ПРИГОДИТЬСЯ
        grammar['N.мн.ч.р.п.'].update(['иев'])               # для случаев типа "загрязненией", "фантазием"
        grammar['A.мн.ч.т.п.'].update(['ами', 'имы'])        # для случаев типа "руссками"
        grammar['V.п.н.ед.ч.'] = grammar['V.п.н.ед.ч.'].difference({'ли'})  # императив "дремли" путается с прош.временем
        return grammar

    
class Allomorphs(kuznec):
   
    def __init__(self):
        self.allomorphs = defaultdict(str,
                                       {item:(self.worddict[item][place]['allo']
                                              if self.worddict[item][place]['allo'] != ['']
                                              else [self.worddict[item][place]['morph']]
                                              )                             
                                        for item in self.worddict
                                        for place in self.worddict[item]
                                        if 'status' in self.worddict[item][place]
                                        and self.worddict[item][place]['status'] == 'корень'
                                        }
                                      )

        self.prefixes = defaultdict(str)
        
        for item in self.worddict:
            for place in self.worddict[item]:
                if 'status' in self.worddict[item][place] \
                and self.worddict[item][place]['status'] == 'префикс' \
                and not self.prefixes[item]:
                    self.prefixes[item] = self.worddict[item][place]['morph']
      
                              
    def is_allomorph_re(self, word, lemma):
        regexp = '^(' + re.sub('[0-9]', '', '|'.join(self.allomorphs[lemma])) + ')'
        print('СПИСОК АЛЛОМОРФОВ: %s' % regexp)
        if regexp != '^()' and re.search(regexp, word) is not None:
            return True
        if regexp == '^()':
            return 'Пусто!'

    def is_allomorph_re2(self, word, lemma):
        regexp = re.sub('[аоуыэяёиюэ]', '[аоуыэяёиюэ]', word[:int(len(word)/2)-1])
        print('БЕЗ ГЛАСНЫХ: %s' % regexp)
        if re.search(regexp, lemma) is not None:
            return True
        

class M:
    
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
            return [mistake
                    for mistake in spellchecked['mistake']
                    if ' ' not in mistake], False
        
    def lemma_merge(self, variants):
        return list({self.pm2.parse(re.sub('[^а-яА-Я]', ' ', variant))[0].normalized.word.replace('ё', 'е')
                    for variant in variants})

    def bare_approach(self, word):
        word = word.lower().replace('ё', 'е')
        spellchecked, is_correct = self.spellcheck(word)
        
        if is_correct == True:
            suggestions = spellchecked
        else:
            suggestions = []
            
            for lemma in self.lemma_merge(list(set(spellchecked).union(context_rules(word)))):
                suggestions += self.rb.try_all(self.rb.find_sfx(word), lemma)           

        print(sorted(suggestions, key=lambda x:x[1], reverse=True))

        return sorted(suggestions, key=lambda x:x[1], reverse=True)

    def approach(self, word):
        word = word.lower().replace('ё', 'е')
        suffix = self.rb.find_sfx(word)
        spellchecked, is_correct = self.spellcheck(word)
        
        if is_correct == True:
            suggestions = spellchecked
        else:
            suggestions = []
            
            for lemma in self.lemma_merge(list(set(spellchecked).union(context_rules(word)))):
                print(lemma)
                prefix = self.al.prefixes[lemma]
                if prefix:
                    for pfx_code in self.rb.prefixes:
                        pfx_to_match = self.rb.prefixes[pfx_code]
                        if prefix in pfx_to_match:
                            print('ПРЕФИКСЫ: %s' % pfx_to_match)
                            pfx_match = re.search('^('+'|'.join(pfx_to_match)+')', word)
                            if pfx_match is not None:
                                print('ПРЕФИКС СОВПАЛ')
                                if self.al.is_allomorph_re2(word.replace(pfx_match.group(0), '', 1), lemma) == True:
                                    print('БЕЗ ГЛАСНЫХ СОВПАЛО')
                                    if self.al.is_allomorph_re(word.replace(pfx_match.group(0),'', 1), lemma) == True:
                                        print('КОРЕНЬ СОВПАЛ')
                                        suggestions += self.rb.try_all(suffix, lemma)
                                        print('ВОТ ЧТО ПОЛУЧИЛОСЬ:' + str(self.rb.try_all(suffix, lemma)))
                                    elif self.al.is_allomorph_re(word.replace(pfx_match.group(0),'', 1), lemma) == 'Пусто!':
                                        print('НЕТ В КУЗНЕЦОВОЙ')
                                        suggestions += self.rb.try_all(suffix, lemma)
                                else:
                                    print('НИГДЕ НЕТ')
                                    suggestions.append((lemma, 0))
                else:
                    if self.al.is_allomorph_re2(word, lemma) == True:
                        print('БЕЗ ГЛАСНЫХ СОВПАЛО')
                        if self.al.is_allomorph_re(word, lemma) == True:
                            print('КОРЕНЬ СОВПАЛ')
                            suggestions += self.rb.try_all(suffix, lemma)
                        elif self.al.is_allomorph_re(word, lemma) == 'Пусто!':
                            print('НЕТ В КУЗНЕЦОВОЙ')
                            suggestions += self.rb.try_all(suffix, lemma)                         
                    else:
                        print('НИГДЕ НЕТ')
                        suggestions.append((lemma, 0))

        print(sorted(suggestions, key=lambda x:x[1], reverse=True))

        return sorted((list(set(suggestions))), key=lambda x:x[1], reverse=True)

    def test(self):
        b,c = [],{}
        with open('for tests.txt', 'r', encoding='utf-8') as test:
            for word in test:
                b.append(word.strip('\n'))
        for w in b:
            print(w)
            c[w] = self.approach(w)

        with open('good_res.txt', 'w', encoding='utf-8') as rrr:
            for wd in c:
                rrr.write(wd+' '+str(c[wd])+'\n')
        print('DONE')
  
    def tokenize(self, text):
        import string
        text = text.lower().split()
        return [token.strip(string.punctuation).replace('ё', 'е')
                for token in text if token not in string.punctuation]    

    def text_morphcheck(self, text):
        return [(word, self.morphcheck(word)) for word in self.tokenize(text)]

    def file_morphcheck(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return self.text_morphcheck(file.read())
