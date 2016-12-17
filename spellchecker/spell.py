from pymystem3 import Mystem
import time
import tests
import subprocess
import re
from pprint import pprint
from rules import rules_back, context_rules

mystem = Mystem()




def hunspell(string):
    '''
    *
    # встертелись 0
    & этым 3 0: тым, этом, этим
    + друзь [без аффикса]
    '''
    # print(string)
    # start_time = time.time()
    echo = subprocess.Popen(['echo', string.encode('utf8')], stdout=subprocess.PIPE)
    result = subprocess.Popen(['hunspell', '-aG', '-d', 'ru_RU'], stdin=echo.stdout, stdout=subprocess.PIPE)
    cyr = result.communicate()[0].decode('utf-8')
    # print("---hunspell: %s seconds ---" % (time.time() - start_time))
    # print(cyr[15])
    if cyr[15] == '*':
        # mistake = False
        print('hunspell says OK')
        return False, [string]
    elif cyr[15] == '&':
        suggested = cyr.split(':')[1].split(',')
        suggested = [w.strip() for w in suggested]
        # print('hunspell suggests:', suggested)
        return True, suggested
    else:
        print('hunspell gives nothing')
        # look
        return True, []


def aspell(string):
    '''
    если ok:    False, []
    если ошибка: True, aspell_sug

    '''
    # enchant.set_param("enchant.aspell.dictionary.path", '/Library/Spelling/aspell6-ru-0.99f7-1')
    d = enchant.Dict("ru_RU")
    if d.check(string):      # aspell says OK
        # print('aspell says OK')
        return False, []
    else:
        # print('aspell says mistake and suggests:')
        aspell_sug = d.suggest(string)
        return True, aspell_sug

# print(aspell('птыца'))


def lookup_mystem(string):
    '''
    кашей{каша=S,жен,неод=твор,ед}
    '''
    # with open('myinput.in', 'w') as myinput:
    #     myinput.write(string)
    # inp = open('myinput.in')
    # start_time = time.time()
    # echo = subprocess.Popen(['echo', string.encode('utf8')], stdout=subprocess.PIPE)
    # result = subprocess.Popen(['./mystem', '-gnid', '-e', 'utf-8'], stdin=echo.stdout, stdout=subprocess.PIPE)
    result = subprocess.Popen(['./mystem', '-gnid', '-e', 'utf-8'], stdin=inp, stdout=subprocess.PIPE)

    cyr = result.communicate()[0].decode('utf-8')
    # print("---mystem+file %s seconds ---" % (time.time() - start_time))
    print(cyr)
    if '?' in cyr:
        mistake = True
    else:
        mistake = False
    print('mystem says', mistake)
    return mistake

# for i in ["эти", "эта", "этой", "мной", "други", "этои", "мнои", "времини"]:
#     print(i)
#     h = hunspell(i)
#     m = lookup_mystem(i)
# print(lookup_mystem('катастрофа'))


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
            big_ru[lemma + ',' + pos] = [ipm, r, d]

    print('START:', test)
    print('aspell')
    pprint(aspell(test))

    # проверяем hunspell
    is_wrong, correct = hunspell(test)
    if not is_wrong:
        print('hunspell says OK')
        # говорит, что ошибки нет.
        # проверим на редкость: лемматизируем и найдём в частотнике
        print('check if rare')
        mystemmed = mystem.analyze(test)
        lemma_mystem = mystemmed[0]['analysis'][0]['lex']
        pos_mystem = mystemmed[0]['analysis'][0]['gr'].split('=')[0].split(',')[0].lower()
        try:
            corr_ipm, corr_r, corr_d = big_ru[lemma_mystem + ',' + pos_mystem]
            print(test, corr_ipm)
        except:
            # нет в частотном словаре, наверное, редкое.
            print('not in the freq_dict', test)

    else:
        print('hunspell says mistake')
        # hunspell говорит, что есть ошибка, и даёт варианты
        if len(correct) > 0:
            ans = []
            print('check if rare')
            for corr in correct:
                # проверить редкость предложенных вариантов
                # print('check if rare')
                mystemmed = mystem.analyze(corr)
                lemma_mystem = mystemmed[0]['analysis'][0]['lex']
                pos_mystem = mystemmed[0]['analysis'][0]['gr'].split('=')[0].split(',')[0].lower()
                try:
                    corr_ipm, corr_r, corr_d = big_ru[lemma_mystem + ',' + pos_mystem]
                    # print(corr, corr_ipm, 'ipm')
                    ans.append((corr, float(corr_ipm)))
                except:
                    # print('not in the dictionary', corr)
                    pass
            pprint(sorted(ans, key=lambda x: x[1], reverse=True))

        else:
            print('hunspell gives nothing')
            # hunspell говорит, что есть ошибка, вариантов нет
            # проверить майстемом
            is_wrong_mystem = lookup_pymystem(test)
            if not is_wrong_mystem:
                correct.append(test)
            else:
                # действительно ошибка, предложить варианты
                print('\tno suggestions by mystem')
            print('final corrections')
            pprint(correct)


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
    print('error dict in memory, took %s sec' % (time.time() - start_time))
    with open('test-set.txt') as f_in:
        words = f_in.readlines()
        for w in words:
            print('-'*20)
            w = w.strip()
            print(w)
            w_test = w.strip().lower()
            # process(ws)
            is_mistake, aspell_suggests = aspell(w_test)
            if is_mistake:
                print('ASPELL')
                print('mistake', '\n'.join(aspell_suggests))
                try:
                    print('RULES')
                    print(mistakes[w_test])
                except:
                    print('NOT IN THE DICTIONARY')


def is_english(word):
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
    i=0
    with open('true_mistakes.dic') as m_file:
        lines = m_file.readlines()
        for line in lines:
            # print(i, len(line.split('\t')))
            m, corr = line.split('\t')
            mistakes[m] = corr
            i += 1
    print('error dict in memory, took %s sec' % (time.time() - start_time))
    return mistakes


def check_boundaries(word, prev_w, next_w):
    '''
    слепить с предыдущим, следующим, пред и след и проверить всё аспеллом
    если такое слово есть - выдать его
    '''
    new = []
    boundaries = list()
    boundaries.append(prev_w + word)
    boundaries.append('-'.join((prev_w, word)))
    boundaries.append(word + next_w)
    boundaries.append('-'.join((word, next_w)))
    boundaries.append(prev_w + word + next_w)
    boundaries.append('-'.join((prev_w, word, next_w)))
    for x in boundaries:
        is_mistake, suggestions = aspell(x)
        if not is_mistake:
            new.append(x)
    print('boundaries:', new)
    return new


def check_word(word, prev_w, next_w, accent_mistakes):
    print('check word:', word)
    result_dict = {'correct': [], 'mistake': []}
    low = word.lower()
    is_mistake, aspell_suggests = aspell(low)
    print('aspell:', is_mistake, aspell_suggests)
    if not is_mistake:
        # ok или real word mistake
        result_dict['correct'].append(low)
    else:
        # аспелл говорит, ошибка
        # границы слов, правила, предложения аспелла
        result_dict['mistake'] += aspell_suggests[:2]

        # if len(aspell_suggests) == 0:

        # границы
        result_dict['mistake'] += check_boundaries(word, prev_w, next_w)
        # небольшой контекст
        result_dict['mistake'] += list(context_rules(word))
        try:
            print('accent rules:')
            correction = accent_mistakes[word]
            print(correction)
            result_dict['mistake'].append(correction)
        except:
            print('artificial mistakes failed')

        try:
            bigram_rules = rules_back(word, ())
            for x in bigram_rules:
                is_wrong, asp = aspell(x)
                if not is_wrong:
                    result_dict['mistake'].append(x)
                elif len(asp) >= 2:
                    result_dict['mistake'] += asp[:2]
                print('bigram rules:', x, '-> asp:', asp[:2])
        except:
            print('ALARM maximum recursion depth exceeded')

    for w in result_dict['correct']:
        if word.istitle():
            w.title()
        elif word.isupper():
            w.upper()
    # mistake_set = []
    # for l in result_dict['mistake']:
    #     mistake_set += l
    # result_dict['mistake'] = list(set(mistake_set))

    return result_dict


# result = spellll('jлa')
# print('== RESULT ==')
# pprint(result)


def check_text(text):
        # print(prepare accent_mistakes)
    print('preparing accent mistakes...')
    accent_mistakes = prepare_accent_mistakes()

    checked_text = []
    lat_table = csv2transform('латиница.csv')

    # вставляем пробелы перед знаками пунктуации
    punct = list(',:;!?')
    text_punct = re.sub('\.', ' . ', text)
    text_punct = re.sub(',', ' , ', text_punct)
    text_punct = re.sub('!', ' ! ', text_punct)
    text_punct = re.sub('\?', ' ? ', text_punct)
    # print('pun', text_punct)
    tokens = text_punct.split(' ')
    print('%d words' % len(tokens))
    tokens.insert(0, ' ')
    tokens.insert(len(tokens), ' ')
    for i, token in enumerate(tokens[1:-1]):
        print('\ntoken:', token, i)
        suggestions = {}
        word = token.strip()
        is_en, num_lat = is_english(word)
        print('# lat =', num_lat)
        if num_lat == len(word) or word in punct:
            # английское слово или знак пунктуации, не проверяем
            print(' '*3 + 'not cyr')
            checked_text.append(word)
        elif num_lat == 0:
            # всё слово кириллицей
            print(' '*3 + 'all cyr')
            suggestions = check_word(word, tokens[i-1], tokens[i+1], accent_mistakes)
        else:
            # есть латиница
            print(' '*3 + 'cyr and lat')
            # правим латиницу
            temp_vars = rules_back(word, lat_table)
            cyr_vars = []
            for replaced in temp_vars:
                if not is_english(replaced)[0]:       # только кириллица
                    cyr_vars.append(replaced)
            print('== CYR ==')
            pprint(cyr_vars)
            for cyr_var in cyr_vars:
                suggestions['mistake'] = check_word(cyr_var, tokens[i-1], tokens[i+1], accent_mistakes)
        checked_text.append(suggestions)
    pprint(checked_text)
    return checked_text


xxx = check_text('жызненый')
print(xxx)
# если выводить текст на экран, надо удалить пробелы перед знаками препинания












