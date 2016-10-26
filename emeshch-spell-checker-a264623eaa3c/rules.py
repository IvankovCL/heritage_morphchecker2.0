import re
from tests import aspell
# from itertools import combinations
# from pprint import pprint


def context_rules(word):
    '''
    выдать список уникальных исправлений слова согласно правилам, которые
     формулируются на небольшом контексте
    '''

    new = []
    # начало слова, пара (верно, ошибка)
    begin = (('е', 'э'), ('э', 'е'), ('c', 'з'), ('чт', 'ш'))
    for pair in begin:
        if word.startswith(pair[1]):
            new.append(pair[0] + word[1:])
    # конец слова, пара (верно, ошибка)
    final = (('к', 'г'), ('й', 'и'), ('з', 'с'),
             ('й', 'ы'), ('аю', 'у'), ('ие', 'и'), ('ся', 'а'))
    minus3 = (('его', 'ево'), ('ого', 'ово'), ('ние', 'нье'),
              ('жом', 'жем'), ('цом', 'цем'), ('чом', 'чем'))
    tsya = ('ца', 'ця', 'ться', 'тса', 'стя', 'ста')

    for pair in final:
        if word.endswith(pair[1]):
            new.append(word[:-1] + pair[0])
    try:
        for pair in minus3:
            if word.endswith(pair[1]):
                new.append(word[:-3] + pair[0])
    except:
        pass
    for x in tsya:
        if word.endswith(x):
            new.append(re.sub(x, 'тся', word))
            new.append(re.sub(x, 'ться', word))
    try:
        if word.startswith('по') and word[2] != '-':
            for x in 'ому ему цки ски ьи'.split(' '):
                if word.endswith(x):
                    new.append('по-'+word[2:])
    except:
        pass
    try:
        if word.startswith('кое') and word[3] != '-':
            new.append('кое-'+word[3:])
    except:
        pass
    try:
        if word.endswith('нибудь') and word[-7] != '-':
            new.append(word[:-6]+'-нибудь')
    except:
        pass
    new = set(new)
    suggest = []
    for x in new:
        is_wrong, asp = aspell(x)
        if not is_wrong:
            suggest.append(x)
        elif len(asp) >= 2:
            suggest += asp[:2]
    print('context rules:', set(suggest))
    return set(suggest)


def recursive_repl(i1, repl, new, wrongs, depth, done):
    '''
    рекурсивно исправляем ошибки
    '''
    for w in i1:        # для каждой строки
        # print(depth, w, '--->')
        # wr_done = []
        # for wr in wrongs:
        #     if wr in w:         # если есть ещё что исправлять
        #         if wr in wr_done:
        # if w not in new:
        # if depth <= len(w):
        for correct2, wrong2 in repl:
            # if wrong2 in wr_done:
            #     print('nooooooooooooooooo')
            # else:
            # wr_done.append(wrong2)
            i2 = []
            for match in re.finditer(wrong2, w):
                # print('match', wrong2, w)
                # print('depth:', depth)
                b, e = match.span()
                if b not in done:
                    # print(b, 'not in', done)
                    for x in range(b, e):
                        done.append(x)
                    # print('and now done=', done)
                    i2.append(w[:b] + correct2 + w[e:])
                    # print('i2', i2)
                new += i2
                depth += 1
                # print('depth', depth)
                new = recursive_repl(i2, repl, new, wrongs, depth, done)
        done = []
        # print('--')

    return new


def rules_back(word, repl):
    '''
    repl = (исправление, ошибка)
    находим координаты ошибочного сочетания,
    добавляем вариант с исправлением в список вариантов
    '''
    # print('BIGRAMM RULES')
    new = []
    # id_correct_wrong = {}
    # перед д, м, а, и, у...
    if repl == ():
        repl = (("ща", "ша"), ("ще", "ше"), ("ше", "ще"), ("щи", "ши"), ("ши", "щи"),
                ("ск", "зк"), ("зк", "ск"), ("жк", "шк"), ("сп", "зп"), ("фс", "вс"), ("йт", "ит"),
                ("сх", "зх"), ("сч", "зч"), ("сш", "зш"),
                #после
                ("бы", "би"), ("гы", "ги"), ("жи", "жы"), ("зы", "зи"), ("ки", "кы"), ("лы", "ли"),
                ("мы", "ми"), ("ны", "ни"), ("ни", "ны"), ("оэ", "ое"), ("ой", "ои"), ("ое", "оэ"),
                ("ры", "ри"), ("ру", "ри"), ("сы", "си"), ("ты", "ти"), ("ти", "ты"), ("ци", "цы"),
                ("це", "цо"), ("че", "чо"), ("чу", "чю"), ("ча", "чя"), ("ше", "шо"), ("ши", "шы"),
                ("шу", "шю"), ("щу", "щю"), ("ща", "щя"),
                ('ть', 'ьт'), ('зг', 'сг')
                )
    # по одной букве
    # one_letter = (
    #         ("д", "б"), ("б", "в"), ("ж", "г"), ("з", "г"), ("д", "г"), ("ж", "д"), ("о", "е"),
    #         ("у", "и"), ("и", "у"),
    #         ('и', 'й')
    #         )
    # по одному

    # simple = []
    # for correct, wrong in one_letter:
    #     if wrong in word:
    #         simple.append(word.replace(wrong, correct))
    # for correct, wrong in repl:
    #     if wrong in word:
    #         simple.append(word.replace(wrong, correct))
    # # все вместе
    # modified = word
    # for correct, wrong in one_letter:
    #     if wrong in word:
    #         modified = modified.replace(wrong, correct)
    # for correct, wrong in repl:
    #     if wrong in word:
    #         modified = modified.replace(wrong, correct)
    # print('all', modified)

    wrongs = [w for c, w in repl]
    # wrongs_one = [w for c, w in one_letter]

    done = []
    depth = 0
    i1 = [word]
    # try:
    new = recursive_repl(i1, repl, new, wrongs, depth, done)
    # except:
    #     pass

    # print('---------')
    # print('combinations', len(set(new)), set(new))
    # print('simple', simple)
    # print(len(set(new)), '\n'.join(set(new))
    return set(new)

# with open('what aspell cant.txt') as t:
#     for line in t.readlines():
#         rules_back(line)
# rules_back('жы-щя')

# for x in rules_back():
#     if aspell(x)[0]


'''
repl = (("ща", "ша"), ("ще", "ше"), ("ше", "ще"), ("щи", "ши"), ("ши", "щи"),
            ("ск", "зк"), ("зк", "ск"), ("жк", "шк"), ("сп", "зп"), ("фс", "вс"), ("йт", "ит"),
            ("сх", "зх"), ("сч", "зч"), ("сш", "зш"),
            #после
            ("бы", "би"), ("гы", "ги"), ("жи", "жы"), ("зы", "зи"), ("ки", "кы"), ("лы", "ли"),
            ("мы", "ми"), ("ны", "ни"), ("ни", "ны"), ("оэ", "ое"), ("ой", "ои"), ("ое", "оэ"),
            ("ры", "ри"), ("ру", "ри"), ("сы", "си"), ("ты", "ти"), ("ти", "ты"), ("ци", "цы"),
            ("це", "цо"), ("че", "чо"), ("чу", "чю"), ("ча", "чя"), ("ше", "шо"), ("ши", "шы"),
            ("шу", "шю"), ("щу", "щю"), ("ща", "щя"),
            ('ть', 'ьт'), ('зг', 'сг')
            )
'''
# rules_back('жы-жы', repl)
