import re, sys, os
# from itertools import product
from tests import hunspell, aspell, csv2transform, lookup_pymystem
from pymystem3 import Mystem
from pprint import pprint
import enchant
import time
from rules import rules_back, context_rules
import numpy as np
from collections import Counter
from nltk.metrics import edit_distance
from shutil import copyfile

# import matplotlib.pyplot as plt

def disable_print(*args):
    pass

def disable_pprint(*args):
    pass

mystem = Mystem()
enchant.set_param("enchant.aspell.dictionary.path", "./aspell6-ru-0.99f7-1")
if not enchant.dict_exists('ru_RU'):
    copyfile('./resources/aspell/ru_RU.dic', os.path.dirname(enchant.__file__).replace('\\', '/') + '/share/enchant/myspell/ru_RU.dic')
    copyfile('./resources/aspell/ru_RU.aff', os.path.dirname(enchant.__file__).replace('\\', '/') + '/share/enchant/myspell/ru_RU.aff')
#     res = list(''.join(o) for o in product(*d))
#     res.remove(low)



def old_process(test):
    '''
    в этой версии есть проверка частотности, aspell, hunspell, mystem
    '''
    # загружаем частотник
    big_ru = {}
    with open('./Freq2011/freqrnc2011.csv') as rus:
        ru = rus.readlines()[1:]
        for line in ru:
            lemma, pos, ipm, r, d, doc = line.split('\t')
            big_ru[lemma + ',' + pos] = ipm

    disable_print('START:', test)
    disable_print('aspell')
    disable_pprint(aspell(test))

    # проверяем hunspell
    is_wrong, correct = hunspell(test)
    if not is_wrong:
        disable_print('hunspell says OK')
        # говорит, что ошибки нет.
        # проверим на редкость: лемматизируем и найдём в частотнике
        disable_print('check if rare')
        mystemmed = mystem.analyze(test)
        lemma_mystem = mystemmed[0]['analysis'][0]['lex']
        pos_mystem = mystemmed[0]['analysis'][0]['gr'].split('=')[0].split(',')[0].lower()
        try:
            corr_ipm = big_ru[lemma_mystem + ',' + pos_mystem]
            print(test, corr_ipm)
        except:
            # нет в частотном словаре, наверное, редкое.
            disable_print('not in the freq_dict', test)

    else:
        disable_print('hunspell says mistake')
        # hunspell говорит, что есть ошибка, и даёт варианты
        if len(correct) > 0:
            ans = []
            disable_print('check if rare')
            for corr in correct:
                # проверить редкость предложенных вариантов
                # disable_print('check if rare')
                mystemmed = mystem.analyze(corr)
                lemma_mystem = mystemmed[0]['analysis'][0]['lex']
                pos_mystem = mystemmed[0]['analysis'][0]['gr'].split('=')[0].split(',')[0].lower()
                try:
                    corr_ipm = big_ru[lemma_mystem + ',' + pos_mystem]
                    # print(corr, corr_ipm, 'ipm')
                    ans.append((corr, float(corr_ipm)))
                except:
                    # disable_print('not in the dictionary', corr)
                    pass
            disable_pprint(sorted(ans, key=lambda x: x[1], reverse=True))

        else:
            disable_print('hunspell gives nothing')
            # hunspell говорит, что есть ошибка, вариантов нет
            # проверить майстемом
            is_wrong_mystem = lookup_pymystem(test)
            if not is_wrong_mystem:
                correct.append(test)
            else:
                # действительно ошибка, предложить варианты
                disable_print('\tno suggestions by mystem')
            disable_print('final corrections')
            disable_pprint(correct)


def olga_test():
    '''
    проверка по искусственным ошибкам
    '''
    mistakes = {}
    start_time = time.time()
    with open('true_mistakes.dic') as m_file:
        lines = m_file.readlines()
        for line in lines:
            m, corr = line.split('\t')
            mistakes[m] = corr
    disable_print('error dict in memory, took %s sec' % (time.time() - start_time))
    with open('test-set.txt') as f_in:
        words = f_in.readlines()
        for w in words:
            disable_print('-'*20)
            w = w.strip()
            print(w)
            w_test = w.strip().lower()
            # process(ws)
            is_mistake, aspell_suggests = aspell(w_test)
            if is_mistake:
                disable_print('ASPELL')
                disable_print('mistake', '\n'.join(aspell_suggests))
                try:
                    disable_print('RULES')
                    print(mistakes[w_test])
                except:
                    disable_print('NOT IN THE DICTIONARY')


def is_english(word):
    '''
    считаем количество букв английского алфавита в слове
    :param word: строковая переменная - слово для проверки
    :return: (True, 3) True если в слове есть английские буквы, False, если только кириллица; количество англ букв
    '''
    english = "abcdefghijklmnopqrstuvwxyz"
    en = 0
    for x in word:
        if x in english:
            en += 1
    if en == 0:
        return False, 0
    else:
        return True, en


def prepare_accent_mistakes():
    mistakes = {}
    start_time = time.time()
    i = 0
    with open('true_mistakes.dic') as m_file:
        lines = m_file.readlines()
        for line in lines:
            # print(i, len(line.split('\t')))
            m, corr = line.split('\t')
            mistakes[m] = corr
            i += 1
    disable_print('error dict in memory, took %s sec' % (time.time() - start_time))
    return mistakes


def check_boundaries(word, prev_w, next_w):
    '''
    слепить с предыдущим, следующим, пред и след и проверить всё аспеллом
    если такое слово есть - выдать его, если нет — первые два предложения аспелла
    '''
    disable_print('CHECK BOUNDARIES: prev word next:', [prev_w, word, next_w])
    new = []
    boundaries = list()
    boundaries.append(prev_w + word)
    boundaries.append('-'.join((prev_w, word)))
    boundaries.append(word + next_w)
    boundaries.append('-'.join((word, next_w)))
    boundaries.append(prev_w + word + next_w)
    boundaries.append('-'.join((prev_w, word, next_w)))
    disable_print('bound vars:', boundaries)
    for x in boundaries:
        is_mistake, suggestions = aspell(x)
        # disable_print('boundaries::', x, is_mistake, suggestions)
        if not is_mistake:
            new.append(x)
        else:
            new += suggestions[:2]
            # print(x, '->aspell', suggestions)

    for p in 'что или ли же бы'.split(' '):
        if word.endswith(p) and len(p) > 0:
            x = word.replace(p, '')
            new.append(x+' '+p)
    disable_print('boundaries:', new)
    return list(set(new))


def heritage_rules(word, prev_w, next_w, accent_mistakes, multiword=True):
    '''
    все наши правила вызываются здесь

    '''
    # границы
    mistake = []
    if multiword:
        mistake += check_boundaries(word, prev_w, next_w)
    # disable_print('1', mistake)
    # небольшой контекст
    mistake += context_rules(word)
    # disable_print('2', mistake)
    try:
        correction = accent_mistakes[word]
        disable_print('accent rules:', correction)
        mistake.append(correction)
    except KeyError:
        disable_print('not in the dict of artificial mistakes')
    # try:
    # disable_print('3', mistake)
    bigram_rules = rules_back(word, ())  #bigram_rules = rules_back(word, (), all_combinations=True)
    for x in bigram_rules:
        is_wrong, asp = aspell(x)
        if not is_wrong:
            mistake.append(x)
        elif len(asp) >= 2:
            mistake += asp[:2]
        disable_print('bigram rules:', x, '-> asp (is_mistake, vars):', is_wrong, asp[:2])
    # except:
    #     disable_print('ALARM', sys.exc_info()[0], 'word:', word)
    # disable_print('4', mistake)

    return mistake


def freq_filter(string, big_ru):
    '''
    if rare return False, else True
    '''
    # disable_print('check if rare:', string)
    # mystemmed = mystem.analyze(string)
    # print(mystemmed)
    try:
        lemma_mystem = mystemmed[0]['analysis'][0]['lex']
        pos_mystem = mystemmed[0]['analysis'][0]['gr'].split('=')[0].split(',')[0].lower()
        ipm = big_ru[lemma_mystem + ',' + pos_mystem]
        #print(string, lemma_mystem + ',' + pos_mystem, ipm)
        if float(ipm) >= 15:
            return [string, True, ipm]
        else:
            return [string, False, ipm]
    except:
        # нет в частотном словаре, наверное, редкое.
        # disable_print('not in the freq_dict', string)
        return [string, False, -1]


def sort_heritage_suggestions(mistake, big_ru):
    '''
    mistake - список наших предложений, big_ru - частотный словарь
    '''

    counted = Counter(mistake)
    more_than_once, only_once = [], []
    for k in counted:
        if counted[k] > 1:
            more_than_once.append(k)
        else:
            only_once.append(k)

    freq_more_than_once = [freq_filter(s, big_ru) for s in more_than_once]
    # print(freq_more_than_once)
    sorted_more_than_once = [x[0] for x in sorted(freq_more_than_once, key=lambda x: float(x[2]), reverse=True)]
    # disable_print('more than once:', sorted_more_than_once)

    freq_only_once = [freq_filter(s, big_ru) for s in only_once]
    freq_from_once = [w for w in filter(lambda x: x[1], freq_only_once)]
    sorted_only_once = [x[0] for x in sorted(freq_from_once, key=lambda x: float(x[2]), reverse=True)]

    # sorted(student_tuples, key=lambda student: student[2])
    disable_print('freq_from_once', freq_only_once)
    if len(sorted_only_once) > 5:
        sorted_only_once = sorted_only_once[:5]

    disable_print('more than once:', sorted_more_than_once)
    disable_print('sorted_only_once', sorted_only_once)
    return sorted_more_than_once + sorted_only_once


def check_word(word, prev_w, next_w, accent_mistakes, big_ru, multiword):
    '''
    проверка и исправление кирилического слова

    :param word: слово, которое сейчас проверяем
    :param prev_w: предыдущий токен; для нулевого токена ' ';
    :param next_w: следующий токен; для последнего токена ' ';
    :param accent_mistakes: то же, что и в check_text
    :param big_ru: то же, что и в check_text
    :return: словарь {'correct': [...], 'mistake': [...], 'aspell': [...]} — см. check_text
    '''
    disable_print('check word (prev - word - next):', [prev_w, word, next_w])
    mistake = []
    result_dict = {'correct': [], 'mistake': [], 'aspell': []}
    # проверяем аспеллом
    is_mistake, aspell_suggests = aspell(word)
    if not is_mistake:
        # ok или real word mistake
        disable_print('aspell: OK')
        result_dict['correct'].append(word)
        print(freq_filter(word, big_ru))
        if freq_filter(word, big_ru)[1]:
            pass
        else:   # редкое correct => даём свои варианты
            mistake = heritage_rules(word, prev_w, next_w, accent_mistakes, multiword)
            result_dict['mistake'] = sort_heritage_suggestions(mistake, big_ru)

    else:
        # аспелл говорит, что есть ошибка
        # result_dict['correct'] = []
        disable_print('aspell: is mistake;', aspell_suggests)

        # предложения аспелла
        result_dict['aspell'] = aspell_suggests
        freq_asp = [freq_filter(s, big_ru) for s in aspell_suggests[2:]]
        # freq_asp = []
        # for s in aspell_suggests:
        #     print(s)
        #     freq_asp.append(freq_filter(s, big_ru))
        disable_print('freq asp:', freq_asp)
        # freq_from_aspell = [w[0] for w in filter(lambda x: x[1], freq_asp)]
        asp_sorted = [x[0] for x in sorted(freq_asp, key=lambda x: float(x[2]), reverse=True)]
        disable_print('ASPELL sorted', asp_sorted)
        if len(asp_sorted) > 5:
            asp_sorted = asp_sorted[:5]

        # asp_to_mistake - это то, что будем объединять с нашими предложениями и писать в ответ
        asp_to_mistake = aspell_suggests[:2] + asp_sorted
        disable_print('asp_to_mistake', asp_to_mistake)
        # теперь наши дополнения
        mistake = []
        mistake += heritage_rules(word, prev_w, next_w, accent_mistakes, multiword)
        disable_print('heritage_rules', mistake)
        # сортируем наши исправления
        disable_print('sort_heritage_suggestions(mistake, big_ru)', sort_heritage_suggestions(mistake, big_ru))
        # ответ
        result_dict['mistake'] = sort_heritage_suggestions(mistake, big_ru) + asp_to_mistake

    return result_dict

#check_word('рисски')

# result = spellll('jлa')
# disable_print('== RESULT ==')
# disable_pprint(result)


def check_text(in_arg, out_arg='fout.txt', accent_mistakes={}, big_ru={},  multiword=False):
    '''
    проверка файла или строковой переменной

    :param in_arg: имя файла (.txt, utf-8),
    :param out_arg: имя файла (.txt, utf-8), куда будем писать результаты
    :param accent_mistakes: словарь искусственных ошибок на безударные
    :param big_ru: частотный словарь русского языка (леммы)
    :param multiword: режим проверки одного слова (используется в evaluation)
    :return: список словарей, соответствующих токенам текста. ключи словаря: 'correct' – если слово написано верно,
                'aspell' – исправления аспелла, 'mistake' – исправления нашей системы
    '''
    # читаем текст и удаляем в конце пробелы, таблуляцию, переносы строк
    if in_arg.endswith('.txt'):
        with open(in_arg, encoding='utf-8') as f_in:
            text = f_in.read().strip()
    else:
        text = in_arg.strip()

    disable_print('='*30+'\n'+'START:')
    checked_text = []       # здесь будет скапливаться ответ -- список словарей (по словарю на слово)

    # загружаем частотник
    '''if big_ru == {}:
        disable_print('preparing freq dict...')
        big_ru = {}
        with open('freqrnc2011.csv') as rus:
            ru = rus.readlines()[1:]
            for line in ru:
                lemma, pos, ipm, r, d, doc = line.split('\t')
                big_ru[lemma + ',' + pos] = ipm     # слово идентифицируется по лемме и части речи, потому что бывают омонимы
    # загружаем словарь искусственных ошибок
    if accent_mistakes == {}:
        disable_print('preparing accent mistakes...')
        accent_mistakes = prepare_accent_mistakes()'''

    # загружаем правила перевода латиницы в кириллицу
    lat_table = csv2transform('латиница.csv')

    if not multiword:
        tokens = [text]     # в режиме multiword=False список токенов состоит только из одного слова

    # вставляем пробелы перед знаками пунктуации, чтобы после разбиения по пробелам не потерять знаки препинания
    punct = list('.,:;!?')      # в дальнейшем нужен список знаков препинания
    text = re.sub('\n', ' ', text)
    text_punct = re.sub('\.', ' . ', text)
    text_punct = re.sub(',', ' , ', text_punct)
    text_punct = re.sub('!', ' ! ', text_punct)
    text_punct = re.sub('\?', ' ? ', text_punct)

    # токенизируем
    tokens = text_punct.split(' ')
    disable_print('%d word(s)' % len(tokens))

    # для нулевого токена предыдущий - пробел, для последнего следующий - пробел
    tokens.insert(0, ' ')
    tokens.insert(len(tokens), ' ')

    # disable_print('TOKENS:', tokens[1:-1])
    for i, token in enumerate(tokens[1:-1]):    # не анализируем пробелы, которые вставили только что
        k = i+1         # настоящие индексы массива tokens
        disable_print('\ntoken:', k, token)
        suggestions = {'correct': [], 'mistake': [], 'aspell': []}  # результаты для этого токена
        word = token.strip().lower()            # к нижнему регистру
        word = re.sub('ё', 'е', word)           # замена ё на е
        if len(word) > 0:                       # если не пустая строка
            is_en, num_lat = is_english(word)   # есть ли в слове латиница?
            # disable_print('# lat =', num_lat)
            if num_lat == len(word) or word in punct:
                # английское слово или знак пунктуации, не проверяем
                disable_print('english or punct')
                checked_text.append({'correct': [], 'aspell': [], 'mistake': []})
            elif num_lat == 0:
                # всё слово кириллицей
                disable_print('all cyr')
                disable_print('prev-w-next:', [tokens[k-1], tokens[k], tokens[k+1]])
                suggestions = check_word(word, tokens[k-1], tokens[k+1], accent_mistakes, big_ru, multiword)
            else:
                # есть латиница
                disable_print('cyr and lat')
                suggestions['aspell'] = aspell(word)[1]
                # правим латиницу
                temp_vars = rules_back(word, lat_table, all_combinations=False)
                disable_print('temp_cyr', temp_vars)
                cyr_vars = []
                for replaced in temp_vars:
                    if not is_english(replaced)[0]:       # только кириллица
                        cyr_vars.append(replaced)
                # disable_print('== CYR ==')
                disable_print('cyr', cyr_vars)
                correct_vars, mistake_vars = [], []
                # обработка каждого из кириллических вариантов
                for cyr_var in cyr_vars:
                    result = check_word(cyr_var, tokens[k-1], tokens[k+1], accent_mistakes, big_ru, multiword)
                    mistake_vars += result['mistake']
                    # suggestions['aspell'] += result['aspell']
                    correct_vars += result['correct']
                    # disable_print('cyr_k suggestions:', suggestions)
                # только уникальные
                mistake_vars = list(set(mistake_vars))
                correct_vars = list(set(correct_vars))
                # находим ipm для исправлений
                freq_mistake_vars = [freq_filter(s, big_ru) for s in mistake_vars]
                # сортируем по частотности
                suggestions['mistake'] = [x[0] for x in sorted(freq_mistake_vars, key=lambda x: float(x[2]), reverse=True)]
                # «правильные» слова сортируем по расстоянию Левенштейна до исходного (ещё с латиницей)
                suggestions['correct'] = sorted(correct_vars, key=lambda x: edit_distance(x, word))

            checked_text.append(suggestions)
    disable_print('===RESULTS===')
    # пишем результаты в файл
    '''if '.txt' not in out_arg:
        out_arg = 'fout.txt'
    with open(out_arg, 'w') as f_out:
        f_out.write('token\taspell_correct\tfull_aspell\ther')'''
    for t, r in zip(tokens[1:-1], checked_text):
            r['mistake'] = list(set(r['mistake']))
        # disable_pdisable_print('\t'.join([t, ','.join(r['correct']), ','.join(r['mistake'])]))
            f_out.write('\n' + t + '\t' + ','.join(r['correct']) + '\t' + ','.join(r['aspell']) + '\t' + ','.join(r['mistake']))
    disable_pprint(checked_text)
    disable_print('='*30)
    if not multiword:
        return checked_text[0]
    else:
        return checked_text


# xxx = check_text('text_1.txt', out_arg='fout.txt', accent_mistakes={}, big_ru={}, multiword=True)
# print(xxx)


def evaluate(in_arg, out_arg):
    '''
    оценка работы системы
    входной файл
    word \t human_correct
    '''
    disable_print('preparing freq dict...')
    big_ru = {}
    with open('freqrnc2011.csv') as rus:
        ru = rus.readlines()[1:]
        for line in ru:
            lemma, pos, ipm, r, d, doc = line.split('\t')
            big_ru[lemma + ',' + pos] = ipm
    disable_print('preparing accent mistakes...')
    accent_mistakes = prepare_accent_mistakes()
    # accent_mistakes = {}
    with open(in_arg) as test_f:
        her = 0
        her_len = 0
        asp = 0
        asp_len = 0
        asp_short = 0
        asp_ok_true = 0
        total = 0
        total_mistakes = 0
        asp_where = []
        asp_len_list = []
        her_len_list = []
        for line in test_f.readlines():
            # print(line.split('\t'))
            # try:
            # token, aspell_corr, full_aspell, her_corr, golden = line.split('\t')
            word, golden = line.replace('\n', '').split('\t')
            # golden = golden_[:-1]
            result = {'correct': [], 'aspell': [], 'mistake': []}
            print([word, golden])
            if word.strip() == golden.strip():
                if golden.strip() in result['correct']:
                    # aspell верно определил корректное слово
                    asp_ok_true += 1
            else:
                total_mistakes += 1
                result = check_text(word, big_ru=big_ru, accent_mistakes=accent_mistakes, multiword=False)
                if golden.strip() in result['mistake']:
                    her += 1
                    her_len += len(result['mistake'])
                    her_len_list.append(len(result['mistake']))
                if golden.strip() in result['aspell']:
                    asp += 1
                    asp_len += len(result['aspell'])
                    asp_len_list.append(len(result['aspell']))
                    asp_where.append(result['aspell'].index(golden.strip()))
                if golden.strip() in result['aspell'][:1]:
                    asp_short += 1
            total += 1
            # except:
            #     pass
        asp_numpy = np.array(asp_where)
        # print(total, her, her_len, asp, asp_short, asp_len, asp_ok_true)
        disable_print('='*50)
        disable_print('heritage/total', round(her/total_mistakes, 4))
        disable_print('aspell/total', round(asp/total_mistakes, 4))
        disable_print('aspell_short(first two)/total', round(asp_short/total_mistakes, 4))
        disable_print('heritage/aspell', round(her/asp, 7))
        disable_print('heritage_length/total', round(her_len/total_mistakes, 4))
        disable_print('aspell_length/total', round(asp_len/total_mistakes, 4))
        disable_print('aspell percentiles', np.percentile(asp_numpy, 25), np.percentile(asp_numpy, 50), np.percentile(asp_numpy, 75))
        disable_print('aspell_index_of_correct(0123..)', asp_where)
        disable_print('aspell_length', asp_len_list)
        disable_print('heritage_length_list', her_len_list)
        if total - total_mistakes > 0:
            disable_print('asp_ok_true/total_mistakes', round(asp_ok_true/(total-total_mistakes), 4))
        if '.txt' in out_arg:
            f_out = open(out_arg, 'w')
        else:
            f_out = open('eval.txt', 'w')
            f_out.write('='*50)
            f_out.write('heritage/total', round(her/total_mistakes, 4))
            f_out.write('aspell/total', round(asp/total_mistakes, 4))
            f_out.write('aspell_short(first two)/total', round(asp_short/total_mistakes, 4))
            f_out.write('heritage/aspell', round(her/asp, 7))
            f_out.write('heritage_length/total', round(her_len/total_mistakes, 4))
            f_out.write('aspell_length/total', round(asp_len/total_mistakes, 4))
            f_out.write('aspell percentiles', np.percentile(asp_numpy, 25), np.percentile(asp_numpy, 50), np.percentile(asp_numpy, 75))
            f_out.write('aspell_index_of_correct(0123..)', asp_where)
            f_out.write('aspell_length', asp_len_list)
            f_out.write('heritage_length_list', her_len_list)
            if total - total_mistakes > 0:
                f_out.write('asp_ok_true/total_mistakes', round(asp_ok_true/(total-total_mistakes), 4))
            f_out.close()

# evaluate('banana.csv')

# test = 'далёкего заморожанние обхидомого серёзьно принокрылась близначки кажетсячто тыжелего расгавариваю двенадьсять растрайевает'

# check_text(test)

if __name__ == "__main__":
    args = []
    for arg in sys.argv[1:]:
        args.append(arg)
    if len(sys.argv) == 4:
        if sys.argv[1] == '-text':
            in_file = sys.argv[2]
            out_file = sys.argv[3]
            check_text(in_file, out_arg=out_file)
        elif sys.argv[1] == '-word':
            in_word = sys.argv[2]
            out_file = sys.argv[3]
            check_text(in_word, out_arg=out_file, multiword=False)
        elif sys.argv[1] == 'evaluate':
            evaluate(sys.argv[2], sys.argv[3])

    else:
        disable_print('WRONG ARGUMENTS!\nto check a utf-8 text file:\npython3 spell_checker.py -text input_file.txt output_file.txt\n'
              'to check a word:\npython3 spell_checker.py -word серёзьно output_file.txt\n'
              'to evaluate results given the gold standard:\npython3 spell_checker.py -evaluate golden.txt output_file.txt\n')
