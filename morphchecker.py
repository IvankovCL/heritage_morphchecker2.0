import re
import pymorphy2
import pylev
import sys
import difflib
import os
sys.path.append('./spellchecker')
from spell_checker import check_word
from rules import context_rules
from prjscript import morphSplitnCheck, kuznec
from collections import defaultdict, namedtuple

Rule = namedtuple('Rule', ['old', 'new', 'condition', 'gram'])

class Rulebook:
    """Модуль для работы со словарями Hunspell

    Файл ru_RU.dic содержит список лемм, каждой из которых приписано множество двухбуквенных кодов,
    каждый код указывает на множество правил постановки леммы во все возможные морфологические формы.

    Формат правила: СУФФИКС/ПРЕФИКС код заменяемая_часть_леммы окончание_нужной_формы условие граммема_окончания.

    Например:
    бороться/BBLLNN                             = на правила для спряжения глагола "бороться" указывают коды BB, LL, NN
    SFX NN оться ются оться (V.н.в.мн.ч.т.л.)   = форма V.н.в.мн.ч.т.л. образуется заменой окончания "оться" на "ются"
                                                  при условии, что глагол заканчивается на "оться"
    """

    def __init__(self):
        """Чтение файлов"""
        with open('./resources/ru_RU.dic', 'r', encoding='UTF-8') as lines:
            wordlist = [line.split('/') for line in lines if '/' in line]

        self.codes_for_lemma = defaultdict(list,
                                           {entry[0]: re.findall('[A-Za-z]{2}', entry[1].strip('\n'))
                                            for entry in wordlist}
                                           )

        with open('./resources/ru_RU.aff', 'r', encoding='UTF-8') as raw:
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

        self.morphs_for_tag = self.heuristics(morphs_for_tag) # словарь {граммема:[морфемы]}
        self.rules_for_code = rules_for_code  # словарь {код: [правила]}

    def tags_for_morph(self, morph):
        """Определение множества граммем для морфемы"""
        return {tag
                for tag in self.morphs_for_tag
                if morph in self.morphs_for_tag[tag]}

    def rules_for_lemma(self, lemma, grams=[]):
        """Определение для леммы правил изменения с учётом граммем"""
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
        """Определение множества морфем, доступных для леммы"""
        return {rule.new
                for rule in self.rules_for_lemma(lemma, grams='all')}

    def pos_for_lemma(self, lemma):
        """Определение части речи леммы по словарю"""
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
        """Постановка леммы в некоторую форму согласно правилу"""
        replaced = re.subn(rule.old + '$', rule.new, lemma)
        if replaced[1]:
            return replaced[0]

    def heuristics(self, grammar):
        """Внесение изменений в словарь {граммема:[морфемы]}"""
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
    """Модуль для работы с алломорфами по словарю Кузнецовой"""
    def __init__(self):
        """Собирает словарь {лемма:[алломорфы корня]}"""
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
        """Изменяет список алломорфов для учёта фонологии"""
        vowel_pairs = {'о': '[ао]', 'а': '[ао]',
                       'и': '[ие]', 'ы': '[ыи]',
                       'е': '[ие]', 'я': '[еяи]'}

        return ''.join([letter
                        if letter not in vowel_pairs
                        else vowel_pairs[letter]
                        for letter in string])

    def is_allomorph(self, error_roots, lemma):
        """Извлекает корень леммы и сравнивает его со списком алломорфов корня ошибочного слова"""

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

        return any([re.search(regexp, error_root)
                   for error_root in error_roots])

        

class Morphchecker:
    """Коррекция морфологических ошибок"""

    def __init__(self):

        self.pm2 = pymorphy2.MorphAnalyzer()
        self.rb = Rulebook()
        self.al = Allomorphs()

    def spellcheck(self, word):
        """Возвращает кортеж:
        ([исправления], False) для слова с ошибкой
        ([само слово], True) для слова без ошибки"""
        spellchecked = check_word(word, ' ', ' ',
                                  accent_mistakes={},
                                  big_ru={},
                                  multiword=False)

        if spellchecked['correct']:
            print("СПЕЛЛЧЕК: %s" % spellchecked['correct'])
            return spellchecked['correct'], True
        else:
            print("СПЕЛЛЧЕК: %s" % spellchecked['mistake'])
            without_context_rules = [mistake
                                    for mistake in spellchecked['mistake']
                                    if ' ' not in mistake]
            with_context_rules = list(set(without_context_rules).union(context_rules(word)))
            return with_context_rules, False

    def get_root_and_tags(self, word):
        """Слово делится на морфемы. Извлекается корень и окончание.
        Определяются возможные граммемы для окончания"""
        morphs = morphSplitnCheck(word)

        flexion = ''
        roots = []
        if hasattr(morphs, 'extraRoot') and morphs.extraRoot:
            roots.append(morphs.extraRoot[0])
        if morphs.root:
            roots.append(morphs.root[0])

        if morphs.postfix and morphs.postfix[0]:
            flexion = morphs.postfix[0]
        else:
            if morphs.suffix:
                flexion = morphs.suffix[0]

        if not flexion:
            flexion = '0'

        tags = self.rb.tags_for_morph(flexion)
        if hasattr(morphs, 'reflexive'):
            tags = {tag for tag in tags if 'V' in tag} # оставляем только граммемы для глаголов, если есть постфикс

        print('ВОЗМОЖНЫЕ КОРНИ: %s' % str(roots))
        print('ОКОНЧАНИЕ: %s' % flexion)
        print('ПОКАЗАТЕЛИ ОКОНЧАНИЯ: %s' % tags)

        return roots, tags

    def pos_check(self, lemma, tags):
        """Сравнивает часть речи исправления с граммемами окончания"""
        if self.rb.pos_for_lemma(lemma) in {tag[0] for tag in tags}:
            return True
        else:
            return False

    def lemma_merge(self, variants):
        """Лемматизирует выдачу спеллчекера. Объединяет одинаковые леммы"""
        lemmas = set()
        for variant in variants:
            variant = re.sub('[^а-яА-Я]', ' ', variant)
            parsed = self.pm2.parse(variant)[0]
            tag = parsed.tag

            if 'PRTF' in tag or 'PRTS' in tag: # причастия и деепричастия лемматизируются в форму причастия м.р. ед.ч. и.п.
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
        """Вычисляет расстояние Левенштейна между каждыи исправлением и ошибочным словом
        Сортирует по возрастанию"""
        return sorted([(pylev.levenshtein(word, suggestion), suggestion)
                       for suggestion in suggestions])

    def locate(self, suggestion, error):
        """Сравнивает исправление с ошибочным словом. Находит лишние, недостающие или изменённые морфемы."""

        suggest_morphs = morphSplitnCheck(suggest).morphList
        error_morphs = morphSplitnCheck(error).morphList
        print(suggest_morphs)
        print(error_morphs)

        difference = ''.join(difflib.ndiff(suggest_morphs, error_morphs))
        print(difference)
        altered = re.findall("[+-] ([^+-]*)\?", difference)
        removed = re.findall("[\-] ([^?+\- ]*)", difference)
        added = re.findall("[+] ([^?+\- ]*)", difference)

        Location = namedtuple('Location', ['suggest', 'altered', 'added', 'removed'])
        return Location(suggest=suggest, altered=altered, added=added, removed=removed)

    def mcheck(self, word):
        """Основной алгоритм"""

        word = word.replace('ё', 'е')
        print('ПРОВЕРЯЕМ СЛОВО: %s' % word)

        spellchecked, is_correct = self.spellcheck(word)

        if is_correct == True:
            suggestions = [(0, spellchecked[0])]
        else:
            suggestions = []

            roots, tags = self.get_root_and_tags(word)

            for lemma in self.lemma_merge(spellchecked):
                if self.pos_check(lemma, tags):
                    print('АНАЛИЗИРУЕМ ВАРИАНТ: %s' % lemma)
                    if self.al.is_allomorph(roots, lemma):
                        print('АЛЛОМОРФ!' + '\n')
                        for rule in self.rb.rules_for_lemma(lemma, grams=tags):
                            corrected = self.rb.apply_rule(rule, lemma)
                            if corrected is not None:
                                suggestions.append(corrected.replace('0', ''))
                    else:
                        print('НЕ АЛЛОМОРФ!' + '\n')
                else:
                    print('У  СЛОВА %s НЕ ТА ЧАСТЬ РЕЧИ ' %lemma)

            if not suggestions:
                suggestions = spellchecked

            suggestions = self.edit_distance(word, suggestions)
            sys.stdout.write('ИСПРАВЛЕНИЯ: %s \n' % suggestions)
            if suggestions:
                min_ed = min(suggestions, key=lambda x: x[0])
                suggestions = [suggestion
                               for suggestion in suggestions
                               if suggestion[0] == min_ed[0]]

        return suggestions

    def analyse(self, suggestions):
        """Локализация ошибки в ошибочном слове на основе исправления"""
        error_morphs = morphSplitnCheck(word).morphList
        location = [self.locate(suggestion[1], error_morphs)
                    for suggestion in suggestions
                    if suggestion[0] != 0]
        message = "Если {0} - правильное исправление, " \
                  "то морфема {1} употреблена вместо морфемы {2}".format(location.suggest, location.added, location.removed)
        print(message)

    def tokenize(self, text):
        """Токенизация перед обработкой текста"""
        import string
        text = text.lower().split()
        return [token.strip(string.punctuation).replace('ё', 'е')
                for token in text if token not in string.punctuation]

    def text_mcheck(self, text):
        return [(word, self.mcheck(word)) for word in self.tokenize(text)]

    def file_mcheck(self, filename1, filename2):
        import io
        with open(filename1, 'r', encoding='utf-8') as f1:
            mchecked = self.text_mcheck(f1.read())
            
        f2 = open(filename2, 'w', encoding='utf-8')
        for m in mchecked:
            f2.write(str(m)+'\n')
        f2.close()

    def test(self):

        with open('ttrue_examples.txt', 'r', encoding='utf-8') as test:
            all_words = [entry.strip('\n') for entry in test]
            results = {word: self.mcheck(word) for word in all_words}

        with open('test_with_new_delilk.txt', 'w', encoding='utf-8') as output:
            for result in results:
                output.write(result + ' ' + str(results[result]) + '\n')

        print('DONE')

pass

def options(argv):
    """
    USAGE
    
    python morphchecker.py [option1] [string] [option2]
    or
    python morphchecker.py input.txt output.txt [option2]

    options 1:
    -m [word]   word morphcheck
    -s [word]   word spellcheck
    -t [text]   text morphcheck

    option 2:
    --log       enable logs
    """



    if len(argv) > 2:
        m = Morphchecker()
        if argv[1] == '-m':
            m.mcheck(argv[2])
        elif argv[1] == '-s':
            m.spellcheck(argv[2])
        elif argv[1] == '-t':
            m.text_mcheck(argv[2])
        if argv[1].endswith('.txt') and argv[2].endswith('.txt'):
            m.file_mcheck(argv[1], argv[2])
    else:
        sys.stdout.write(options.__doc__)

if __name__ == '__main__':
    if '--log' not in sys.argv:
        def print(*args):
            pass
    options(sys.argv)

