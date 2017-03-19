import re
import pymorphy2
import pylev
import sys
sys.path.append('C:/Users/Ivankov/Documents/GitHub/heritage_morphchecker2.0/spellchecker')
from spell_checker import check_word
from rules import context_rules
from prjscript import morphSplitnCheck, kuznec
from collections import defaultdict, namedtuple

Rule = namedtuple('Rule', ['old', 'new', 'condition', 'gram'])

class Rulebook:

    def __init__(self):

        with open('C:/Users/Ivankov/Documents/GitHub/heritage_morphchecker2.0/resources/ru_RU.dic', 'r',
                  encoding='UTF-8') as lines:
            wordlist = [line.split('/') for line in lines if '/' in line]

        self.codes_for_lemma = defaultdict(list,
                                           {entry[0]: re.findall('[A-Za-z]{2}', entry[1].strip('\n'))
                                            for entry in wordlist}
                                           )

        with open('C:/Users/Ivankov/Documents/GitHub/heritage_morphchecker2.0/resources/ru_RU.aff', 'r',
                  encoding='UTF-8') as raw:
            sfx_rules = [line.split() for line in raw
                         if 'SFX' in line and ' Y ' not in line]

            pfx_rules = [rule.split() for line in raw
                         if 'PFX' in line and ' Y ' not in line]

        morphs_for_tag = defaultdict(set)
        rules_for_code = defaultdict(list)

        for rule in sfx_rules:

            morph = re.sub('[//[a-zA-Z]]*', '', rule[3])  # нужно убрать символы после слэша
            tag = rule[5].strip('()')

            POS = tag[0]
            if POS in ['N', 'A']:
                morphs_for_tag[POS + '.им.п.м.р.'].add(rule[2])
            elif POS == 'V':
                morphs_for_tag[POS + '.инф.'].add(rule[2])

            morphs_for_tag[tag].add(morph)

            rules_for_code[rule[1]].append(Rule(old=rule[2].replace('0', ''),
                                                new=morph.replace('0', ''),
                                                condition=rule[4].replace('0', ''),
                                                gram=tag
                                                )
                                           )

        self.morphs_for_tag = self.heuristics(morphs_for_tag)
        self.rules_for_code = rules_for_code

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
            return self.rules_for_lemma(lemma, grams='all')[0].gram[0]
        except (IndexError, KeyError):
            try:
                al = Allomorphs()
                if al.worddict[lemma]:
                    return al.worddict[lemma]['1']['pos']
            except KeyError:
                print('Лемма отсутствует! Часть речи неизвестна! \n')
                return None

    def apply_rule(self, rule, lemma):
        replaced = re.subn(rule.old + '$', rule.new, lemma)
        if replaced[1]:
            return replaced[0]

    def heuristics(self, grammar):
        no_adj_noun = {'ая', 'яя', 'ее', 'ое', 'и', 'ы', 'ев', 'ей', 'ем',
                       'ом', 'ов', 'ет', 'ли', 'ла', 'ло', 'ной', 'ни'}
        no_verb = {'и'}
        grammar['A.им.п.м.р.'] = grammar['A.им.п.м.р.'].difference(no_adj_noun)
        grammar['N.им.п.м.р.'] = grammar['N.им.п.м.р.'].difference(no_adj_noun)
        grammar['V.инф.'] = grammar['V.инф.'].difference(no_verb)
        grammar['V.н.в.ед.ч.ж.р.'].update(['а']) # делилка не может выделить "ла", "ло", "ли"
        grammar['V.н.в.ед.ч.с.р.'].update(['о'])
        grammar['V.н.в.мн.ч.'].update(['и'])
        grammar['N.ед.ч.т.п.'].update(['ией', 'ием'])  # МОЖЕТ И НЕ ПРИГОДИТЬСЯ
        grammar['N.мн.ч.р.п.'].update(['иев'])  # для случаев типа "загрязненией", "фантазием"
        grammar['A.мн.ч.т.п.'].update(['ами', 'имы'])  # для случаев типа "руссками"
        grammar['A.краткая.форма.ед.ч.м.р.'].update(['ан'])  # для случев типа "разрешан"
        grammar['A.им.п.м.р.'].update({'ай'}) # развиващай
        grammar['V.п.н.ед.ч.'] = grammar['V.п.н.ед.ч.'].difference({'ли'}, {'ки'}, {'ыми'})  # императив "дремли" путается с прош.временем
        grammar['N.мн.ч.и.п.'] = grammar['N.мн.ч.и.п.'].difference({'ли'})

        return grammar



class Allomorphs(kuznec):
    def __init__(self):
        self.allomorphs = defaultdict(str,
                                      {item: (self.worddict[item][place]['allo']
                                              if self.worddict[item][place]['allo'] != ['']
                                              else [self.worddict[item][place]['morph']]
                                              )
                                       for item in self.worddict
                                       for place in self.worddict[item]
                                       if 'status' in self.worddict[item][place]
                                       and self.worddict[item][place]['status'] == 'корень'
                                       }
                                      )

    def vowel_change(self, string):

        vowel_pairs = {'о': '[ао]',
                       'а': '[ао]',
                       'и': '[ие]',
                       'ы': '[ыи]',
                       'е': '[ие]',
                       'я': '[еяи]'}

        return ''.join([letter
                        if letter not in vowel_pairs
                        else vowel_pairs[letter]
                        for letter in string])

    def is_allomorph(self, error_root, lemma):

        choice = '|'.join(self.allomorphs[lemma])

        if choice:
            regexp = '^(' + re.sub('([0-9]|\(j\))', '', self.vowel_change(choice)) + ')'
            print('СПИСОК АЛЛОМОРФОВ: %s' % regexp)
        else:
            try:
                variant_morphs = morphSplitnCheck(lemma)
            except (KeyError, AttributeError, IndexError) as exc:
                print(exc)
                return None

            if hasattr(variant_morphs, 'extraRoot') and variant_morphs.extraRoot:
                variant_root = variant_morphs.extraRoot[0]
            elif variant_morphs.root:
                variant_root = variant_morphs.root[0]
            print('КОРЕНЬ ВАРИАНТА: %s' % variant_root)

            regexp = '^(' + re.sub('([0-9]|\(j\))', '', self.vowel_change(variant_root)) + ')'  # во(j) - в корнях слов военный, воин
            print('СПИСОК АЛЛОМОРФОВ: %s' % regexp)

        if re.search(regexp, error_root) is not None:
            return True
        else:
            return False
        
        

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
            return [mistake
                    for mistake in spellchecked['mistake']
                    if ' ' not in mistake], False

    def get_root_and_tags(self, word):

        morphs = morphSplitnCheck(word)

        if hasattr(morphs, 'extraRoot') and morphs.extraRoot:
            root = morphs.extraRoot[0]
        elif morphs.root:
            root = morphs.root[0]

        if morphs.postfix:
            flexion = morphs.postfix[0]
        else:
            if morphs.suffix:
                flexion = morphs.suffix[0]

        if not flexion:
            flexion = '0'

        tags = self.rb.tags_for_morph(flexion)
        if hasattr(morphs, 'reflexive'):
            tags = {tag for tag in tags if 'V' in tag}

        print('КОРЕНЬ: %s' % root)
        print('ОКОНЧАНИЕ: %s' % flexion)
        print('ПОКАЗАТЕЛИ ОКОНЧАНИЯ: %s' % tags)

        return root, tags

    def pos_check(self, lemma, tags):
        if self.rb.pos_for_lemma(lemma) in {tag[0] for tag in tags}:
            return True
        else:
            return False

    def lemma_merge(self, variants):
        lemmas = set()
        for variant in variants:
            variant = re.sub('[^а-яА-Я]', ' ', variant)
            parsed = self.pm2.parse(variant)[0]
            tag = parsed.tag

            if 'PRTF' in tag or 'PRTS' in tag:
                lemmas.add(parsed.inflect({'sing', 'nomn', 'masc'}).word.replace('ё', 'е'))
            else:
                lemmas.add(parsed.normalized.word.replace('ё', 'е'))

            if 'GRND' in tag:
                if 'pres' in tag:
                    lemmas.add(parsed.inflect({'sing', 'nomn', 'masc', 'pres'}).word.replace('ё', 'е'))
                if 'past' in tag:
                    lemmas.add(parsed.inflect({'sing', 'nomn', 'masc', 'past'}).word.replace('ё', 'е'))

        return list(lemmas)

    def edit_distance(self, word, suggestions):
        scores = [(pylev.levenshtein(word, suggestion), suggestion)
                  for suggestion in suggestions]
        return sorted(scores)

    def locate(self, error, suggestion):
        error_morphs = error.morphList
        suggest_morphs = morphSplitnCheck(suggestion).morphList
        print(error_morphs)
        print(suggest_morphs)
        """
        suggestions = [self.locate(morphs, suggestion[1])
                       for suggestion in suggestions
                       if suggestion[0] == 1]"""

    def mcheck(self, word):
        word = word.replace('ё', 'е')
        print('ПРОВЕРЯЕМ СЛОВО: %s' % word)

        spellchecked, is_correct = self.spellcheck(word)

        if is_correct == True:
            suggestions = spellchecked
        else:
            suggestions = []

            spellchecked = list(set(spellchecked).union(context_rules(word)))
            print('СПЕЛЛЧЕК: %s' % spellchecked + '\n')

            root, tags = self.get_root_and_tags(word)

            for lemma in self.lemma_merge(spellchecked):
                if self.pos_check(lemma, tags):
                    print('АНАЛИЗИРУЕМ ВАРИАНТ: %s' % lemma)
                    if self.al.is_allomorph(root, lemma):
                        print('АЛЛОМОРФ!' + '\n')
                        for rule in self.rb.rules_for_lemma(lemma, grams=tags):
                            corrected = self.rb.apply_rule(rule, lemma)
                            if corrected is not None:
                                suggestions.append(corrected.replace('0', ''))
                    else:
                        print('НЕ АЛЛОМОРФ!' + '\n')
                else:
                    print('У  СЛОВА %s НЕ ТА ЧАСТЬ РЕЧИ ' %lemma)

            """if not suggestions:
                suggestions = spellchecked"""

            suggestions = self.edit_distance(word, suggestions)
            print('ИСПРАВЛЕНИЯ: %s \n' % suggestions)
            if suggestions:
                min_ed = min(suggestions, key=lambda x: x[0])
                suggestions = [suggestion
                               for suggestion in suggestions
                               if suggestion[0] == min_ed[0]]

        return suggestions

    def tokenize(self, text):
        import string
        text = text.lower().split()
        return [token.strip(string.punctuation).replace('ё', 'е')
                for token in text if token not in string.punctuation]

    def text_mcheck(self, text):
        return [(word, self.morphcheck(word)) for word in self.tokenize(text)]

    def file_mcheck(self, filename):
        with open(filename, 'r', encoding='utf-8') as file:
            return self.text_morphcheck(file.read())

    def test(self):

        with open('for tests.txt', 'r', encoding='utf-8') as test:
            all_words = [entry.strip('\n') for entry in test]
            results = {word: self.mcheck(word) for word in all_words}

        with open('test_with_new_delilk.txt', 'w', encoding='utf-8') as output:
            for result in results:
                output.write(result + ' ' + str(results[result]) + '\n')

        print('DONE')

m = Morphchecker()

pass