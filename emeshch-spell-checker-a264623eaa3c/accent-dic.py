from pprint import pprint
import re
'''
из словаря ударений сделать список искусственных ошибок, которые описываются в generate_mistakes()
'''

def convert_dic():
    f_out = open('accents_expanded.dic', 'w')
    # wordforms = []
    with open('accent.dic', encoding='cp1251') as dictionary:
        for line in dictionary.readlines():
            # paradigm = {}
            left, accent = line.split('\t')
            accent = re.sub('\n', '', accent)
            accent = re.sub('\d`,?', '', accent)
            accent = re.sub('"', '', accent)
            if len(left.split('(')) > 1:
                stem, flex = left.split('(')
                flexes = flex.split('|')
                for f in flexes:
                    if len(f) > 0:
                        ff = re.sub('\)', '', f)
                        word = stem + ff
                        # wordforms.append({stem + ff : accent})
                        f_out.write(word + '\t' + accent + '\n')
    f_out.close()
# pprint(wordforms)


def expand_multiaccents():
    i = 0
    k = 0
    new_dic = open('accents_expanded_final.dic', 'w')
    with open('accents_expanded.dic') as dic:
        for line in dic.readlines():
            i += 1
            if ',' not in line:
                new_dic.write(line)
                k += 1
            else:
                word, acc_pos = line.split('\t')
                for a in acc_pos.split(','):
                    new_dic.write(word + '\t' + a + '\n')
                    k += 1
    # print(i, k)
    new_dic.close()
    new = open('accents_expanded_final.dic').read()
    no_blank_lines = new.replace('\n\n', '\n')
    with open('accents_final.dic', 'w') as out:
        out.write(no_blank_lines)

# expand_multiaccents()


def abs_acc_pos():
    '''
    был номер ударного слога, стала позиция ударной гласной в слове (с нуля!)
    word
    :return:
    '''
    new_dic = open('accents_abs.dic', 'w')
    # k = 0
    with open('accents_final.dic') as dic:
        for wnum, line in enumerate(dic.readlines()):
            # k += 1
            # print(k, line)
            word, acc_pos = line.split('\t')
            acc = acc_pos[:-1]
            # c_index = 0
            vow = 0
            abs_pos = 0
            for cnum, c in enumerate(word):
                # c_index += 1
                if c in 'аеиоуыэюяё':
                    vow += 1
                    if str(vow) == acc:
                        abs_pos = cnum      # с нуля!
            new_dic.write(word + '\t' + str(abs_pos))
            if wnum < 150 and wnum > 140:
                print(wnum, word, acc_pos[:-1], abs_pos)


def generate_mistakes(word, left, abs_pos, right):
    '''
    возвращает список искусственных ошибок для слова; см. в accent-dic.py
    '''
    new = []
    # однобуквенные замены безударных
    replacements = (('о', 'а'), ('я', 'е'), ('я', 'и'), ('е', 'и'), ('а', 'о'), ('и', 'е'))

    for i in left+right:
        for pair in replacements:
            if word[i] == pair[0]:
                new.append(word[:i] + pair[1] + word[1+i:])
    if word[-2:] == 'ии' and abs_pos < len(word)-2:
        new.append(word[:-1] + 'е')

    return set(new)


def artif_mistakes():
    '''
    # это номер слова, слово,
    массивы индексов гласных букв слева от ударной, ударной, справа от неё
    wnum, word, left, abs_pos, right

    '''
    mistakes_dic = open('mistakes.dic', 'w')
    # k = 0
    lengths = []
    with open('accents_final.dic') as dic:
        lines = dic.readlines()
        print('total: %d words in the dictionary' % len(lines))
        for wnum, line in enumerate(lines):

            word, acc_pos = line.split('\t')
            # print(','.join([x for x in acc_pos]))
            try:
                acc = float(acc_pos.replace(r'\n', r''))
            except:
                print('ALARM ALARM')
                print(word, acc_pos, ','.join([x for x in acc_pos]))
            # c_index = 0
            vow = 0
            abs_pos = 0
            left, right = [], []
            for cnum, c in enumerate(word):
                # c_index += 1
                if c in 'аеиоуыэюяё':
                    vow += 1
                    if vow == acc:
                        abs_pos = cnum      # с нуля!
                    elif vow > acc:
                        right.append(cnum)
                    elif vow < acc:
                        left.append(cnum)

            # это массивы индексов гласных букв слева от ударной, ударной, справа от неё
            w_errors = generate_mistakes(word, left, abs_pos, right)

            for we in w_errors:
                mistakes_dic.write(we + '\t' + word + '\n')
            # lengths.append((len(word), len(w_errors)))

    # with open('stat.csv', 'w') as stat:
    #     stat.write('word\terrors\n')
    #     for pair in lengths:
    #         stat.write('\t'.join([str(x) for x in pair]) + '\n')
    # return
# аббревиатуру [0, 4, 6, 7] 9 [11]


# artif_mistakes()


def mistakes_not_ok():
    '''
    write mistakes from 'mistakes.dic' that are not in 'accents_final.dic' to 'true_mistakes.dic'
    '''
    wordlist = []
    mistakes = {}
    true_mistakes = {}
    with open('accents_final.dic') as dictionary:
        lines = dictionary.readlines()
        for line in lines:
            word, accent = line.split('\t')
            wordlist.append(word)
    wordlist = set(wordlist)

    with open('mistakes.dic') as m_file:
        lines = m_file.readlines()
        for l in lines:
            m, corr = l.split('\t')
            mistakes[m] = corr
    # mistakes = set(mistakes)
    print('set mistakes')

    for z in mistakes:
        if z not in wordlist:
            true_mistakes[z] = mistakes[z]

    with open('true_mistakes.dic', 'w') as true_f:
        for x in true_mistakes:
            true_f.write(x + '\t' + true_mistakes[x])

mistakes_not_ok()


