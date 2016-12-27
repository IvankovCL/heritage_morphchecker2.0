# -*- coding: utf-8 -*-

from nltk.stem import snowball as stem
import time

vowels = ['а', 'у', 'о', 'ы', 'и', 'э', 'я', 'ю', 'ё', 'е']

mistakes = []
text = open('mistakes.txt', 'r') 
for line in text:
    line = line.split()
    lc = ''
    for i in line:
        
        if i[0] != '(':
            lc = lc + i + ' '
        else:
            break
    mistakes.append(lc.replace(',','').split())
text.close()
    
mistakes2 = []

mist = open('testset.txt','r',encoding = 'utf-8')

for line in mist:
    mistakes2.append(line.replace('\n',''))

mist.close()
stmr = stem.RussianStemmer()

# for item in mistakes:
 #   cash = []
 #   for word in item:
 #       cash.append(stmr.stem(word))
#    print(cash)



class kuznec:

    worddict = {}
    rootdict = []
    interfixlist = []
    
    cashline = []
    
    with open('umorphodict2.csv', 'r', encoding = 'utf-8') as slovar:
        next(slovar)
    
        for line in slovar:
            line = line.split('\t')
            if line[0] not in worddict:
                worddict[line[0]] = {}  
    
            worddict[line[0]].update({line[3] : {'morph' : line[1], 'status' : line[2], 'place' : line[3], 'allo' : line[4].split('|'), 'pos' : line[5].replace('\n','')}})
            if line[2] == 'корень':
                rootdict.append(line[1])
            if line[2] == 'интерфикс':
                interfixlist.append(line[1])
                
    
#        cashline = [line[0]]
#        if tuple(line[2],line[1]) not in cash:
#            cash.append(tuple(line[2],line[1]))
            
kuzdra = kuznec()
rootdict = list(set(kuzdra.rootdict))
interfixlist = list(set(kuzdra.interfixlist))



                
            
    
        



#wcash = []        
#for word in worddict:
#    
#    l = len(worddict[word])
#    for pl in range(1,l):
#        try:
#            if worddict[word][str(pl)]['status'] == 'суффикс':
#                wcash.append(worddict[word][str(pl)]['morph'])
#        except:
#            print('boink!')
#            pass
#    mrph = set(wcash)



# print(stmr.stemmmm('изменяющимися'))


# VSE KAKIE EST SUFFIXI NA KONCE ZAPISIVAET
def get_sfx(text, suffix):
    sfxcash = []
    for i in suffix:
#        print(i)
        if text.endswith(i):
            sfxcash.append(i)
            print('суффикс ' + i + ' !!!')
    return(sfxcash)

def strip_end(text, suffix, scheck = 0):
  
    vowelcount = 0
#    i = max(get_sfx(text, suffix), key = len)
    for s in vowels:
        vowelcount = vowelcount +  text[:len(text)-len(suffix)].count(s)
    
    if scheck == 1:    
        if vowelcount > 0 :
            return(text[:len(text)-len(suffix)])
            
                    
        else:
            print('VOWELCOUNT INSUFFICIENT')
            return([text,''])   
    else:
        return(text[:len(text)-len(suffix)])
        
                
#def get_pr(text,prst):
#    prcash = []
#    for i in prst:
#        if text.startswith(i):
#            print('Приставка ' + i + ' !!!')
#            prcash.append(i)
            
class prefixwork:
    
    
    
    def get_prefix(self, text, prst):
        self.prefixlist = ['']
        
        for i in prst:
            if text.startswith(i):
                print(' CLASSNAJA Приставка ' + i + ' !!!')
                vowelcount = 0
                for s in vowels:
                    
                    vowelcount = vowelcount + text[len(i):].count(s)
                self.vowelcount = vowelcount
                if vowelcount > 0:
#                    ostatok = text[len(i):]
                    self.prefixlist.append(i)
    def strip_start(self):
        if len(self.prefixlist) > 0:
            self.maxprefix = max(self.prefixlist, key = len)
        
    
    def __init__(self, text, prst = stmr.gtprst()):
        self.get_prefix(text, prst)
        self.strip_start()
    
        if len(self.prefixlist) > 0:
            self.ostatok = text[len(self.maxprefix):]
        else:
            self.ostatok = text
            self.maxprefix = ''
        
class postfixwork:
    def get_postfix(self, text, post):
        self.postfixlist = ['']
        
        for i in post:
            if text.endswith(i):
                print(' CLASSNAJA okon4anie ' + i + ' !!!')
                vowelcount = 0
                for s in vowels:
                    
                    vowelcount = vowelcount + text[:len(text)-len(i)].count(s)
                self.vowelcount = vowelcount
                if vowelcount > 0:
#                    ostatok = text[len(i):]
                    self.postfixlist.append(i)
    def strip_end(self):
        if len(self.postfixlist) > 0:
            self.maxpostfix = max(self.postfixlist, key = len)
            
    def __init__(self, text, post = stmr.gtpost()):
        self.get_postfix(text, post)
        self.strip_end()
    
        if len(self.postfixlist) > 0:
            self.ostatok = text[:len(text)-len(self.maxpostfix)]
        else:
            self.ostatok = text
            self.maxpostfix = ''
    
    

                
def get_syll(word):
    vcnt = 0
    for ind, s in enumerate(word):
        if s in vowels:
            vcnt = vcnt + 1
        if vcnt > 1:
            return(word[:ind])
    vcnt = 0
    return(word)
    
    
    
#def recheck(word):
#    print('RECHECK WITH PRSYLL IS BEING RUN')
#    print(word)
#    if word in rootdict:
#        print('STRIKE WORD')
#        return((word,1))
# A-ROOT STEP -----------------------------------------------------------------
#    if word.endswith('а'):
#        arootDict = []
#        for i in stmr.gtart():
#            if word.endswith(i):
#                arootDict.append(i)
#        if len(arootDict) > 0:
#            maxARoot = (max(arootDict, key = len))
#            prst = word[:len(word) - len(maxARoot)]
#            if prst in stmr.gtprst(): 
#                print('STRIKE A-ROOT')
#                return([maxARoot, prst, ''],5)
#
#    nopr = prefixwork(word)
#    if nopr.ostatok in rootdict:
#        print('STRIKE SOLO PR')
#        return([nopr.ostatok, nopr.maxprefix, ''],2)
#    sfxrtcash = {}
#    for i in get_sfx(word, stmr.gtsfx()):
#        if strip_end(word, i) in rootdict:
#            sfxrtcash.update({strip_end(word, i) : i})
#    if len(sfxrtcash) > 0 :
#        maxkey = (max(list(sfxrtcash.keys()), key = len))
#        return([maxkey, '', sfxrtcash[maxkey]],3)
#    if ((len(sfxrtcash) == 0) and (nopr.maxprefix != '')):
#        for i in get_sfx(nopr.ostatok, stmr.gtsfx()):
#            if strip_end(nopr.ostatok, i) in rootdict:
#                sfxrtcash.update({strip_end(nopr.ostatok, i) : i})
#    if len(sfxrtcash) > 0:
#        print('SUTORAIKU SFX!')    
#        maxkey = (max(list(sfxrtcash.keys()), key = len))
#        return([maxkey, nopr.maxprefix, sfxrtcash[maxkey]],3)


class rootworks():
    
    def go_get_it(self,word):
        self.successCode = True
        
# FIRST STEP ------------------------------------------------------------------    
        if word in rootdict:

            print('STRIKE WORD')

            self.root += [word]
            return
# A-ROOT STEP -----------------------------------------------------------------
        if self.word.endswith('а'):
            arootDict = []
            for i in stmr.gtart():
                if word.endswith(i):
                    arootDict.append(i)
            if len(arootDict) > 0:
                maxARoot = (max(arootDict, key = len))
                prst = word[:len(word) - len(maxARoot)]
                if prst in stmr.gtprst(): 
                    print('STRIKE A-ROOT')
                    self.prefix += [prst]
                    self.root += [maxARoot]
                    return
# SECOND STEP -----------------------------------------------------------------
        nopr = prefixwork(word)

        self.nopr = nopr
        if nopr.ostatok in rootdict:
            print('STRIKE SOLO PR')
            self.root += [nopr.ostatok]
            self.prefix += [nopr.maxprefix]
            return
# THIRD STEP ------------------------------------------------------------------
        sfxrtcash = {}
        for i in get_sfx(word, stmr.gtsfx()):
            if strip_end(word, i) in rootdict:
                sfxrtcash.update({strip_end(word, i) : i})
    #root + single suffix
        if len(sfxrtcash) > 0 :
            maxkey = (max(list(sfxrtcash.keys()), key = len))
            self.root += [maxkey]
            self.suffix += [sfxrtcash[maxkey]]
            return
   # root + prefix + suffix
        if ((len(sfxrtcash) == 0) and (nopr.maxprefix != '')):
            for i in get_sfx(nopr.ostatok, stmr.gtsfx()):
                if strip_end(nopr.ostatok, i) in rootdict:
                    sfxrtcash.update({strip_end(nopr.ostatok, i) : i})
        if len(sfxrtcash) > 0:
            print('SUTORAIKU SFX!')    
            maxkey = (max(list(sfxrtcash.keys()), key = len))
            self.root += [maxkey]
            self.prefix += [nopr.maxprefix]
            self.suffix += [sfxrtcash[maxkey]]
            return

        self.successCode = False
        return 
        
    def flush(self):
        self.prefix = []
        self.suffix = []
        self.root = []

        self.interfix = []
    
    def __init__(self, word):
        self.word = postfixwork(word)    
        self.postfix = [self.word.maxpostfix]
        self.prefix = []
        self.suffix = []
        self.root = []
        self.extraRoot = []
        self.interfix = []
        self.word = self.word.ostatok
        word = self.word
# FIRST ITERATION
        self.go_get_it(word)
    

                
# MORE PRISTAVKAS
        if not self.successCode:
            
            self.prefix += [self.nopr.maxprefix]
            word = self.nopr.ostatok
        
            print('MASS PREFIX STAGE')

            print(self.postfix)
            print(word)

            self.go_get_it(word)

# PLAN KAPKAN
        if not self.successCode:
            
            print('PLAN PEREHVAT')
            self.flush()
            rootCash = []
            for i in rootdict:
                if self.word.startswith(i):
                    rootCash.append(i)
            if len(rootCash)>0:
                self.extraRoot += [max(list(rootCash), key = len)]
                word = self.word[len(max(list(rootCash), key = len)):]
                                       
                print(word)
              #  self.go_get_it(word)
              

                self.go_get_it(word)
                root_no_int = ''.join(self.root)
                print('DA ETO ON'+root_no_int)
                
                for i in interfixlist:
                    
                    if word.startswith(i):
                        self.flush()
                        self.interfix += [i]
                        word = word[len(i):]
                        self.go_get_it(word)
                        root_int = ''.join(self.root)
                        print('da eto on '+root_int)
                        if len(root_int) > len(root_no_int):
                            print('subzero wins')
                            pass
                        else:
                            self.root = [root_no_int]
                            self.interfix = []
                
                     
                   
                    
                    

# MORE SUFFIXES
        if not self.successCode:
            self.prefix += [self.nopr.maxprefix]
            word = self.nopr.ostatok
            suffix = ''
            try:
                suffix = max(get_sfx(word,stmr.gtsfx()), key = len)
                self.suffix += [max(get_sfx(word,stmr.gtsfx()), key = len)]
            except:
                pass
            print(word)
            word = word[:len(word)-len(suffix)]
            print('MAX SUFFIX STAGE')
            print(self.suffix)
            print(word)
            
            self.go_get_it(word)


# IF ALL FAILS        
        if not self.successCode:
            print('MISSION FAILED')
            self.flush()
            try:
                suffix = max(get_sfx(self.word,stmr.gtsfx()), key = len)
                self.suffix += [max(get_sfx(self.word,stmr.gtsfx()), key = len)]
            except:
                pass
            prefix = prefixwork(self.word[:len(self.word)-len(suffix)])
            self.root += [prefix.ostatok]
            self.prefix += [prefix.maxprefix]

            
    
#def get_root(text):
#    global prtr
#    word = postfixwork(text)
#    prtr = word.maxpostfix
#    word = word.ostatok
#    word = stmr.stemmmm(text)[1]
#    prtr = stmr.stemmmm(text)[2][0]
#    print(prtr)
#    print(word)
#    nopr = None
#    print(word)
#    fst = 
#    ffst = strip_end(word, stmr.gtsfx())
#    fnl = strip_start(strip_end(word,stmr.gtsfx())[0],stmr.gtprst())

    
# FIRST STEP ------------------------------------------------------------------    
#    if word in rootdict:
#        print('STRIKE WORD')
#        return((word,1))
# FIRST STEP END --------------------------------------------------------------
# A-ROOT STEP -----------------------------------------------------------------
#    if word.endswith('а'):
#        arootDict = []
#        for i in stmr.gtart():
#            print(i)
#            if word.endswith(i):
#                arootDict.append(i)
#        if len(arootDict) > 0:
#            maxARoot = (max(arootDict, key = len))
#            prst = word[:len(word) - len(maxARoot)]
#            if prst in stmr.gtprst(): 
#                print('STRIKE A-ROOT')
#                return([maxARoot, prst, ''],5)

# SECOND STEP -----------------------------------------------------------------
 #   nopr = prefixwork(word)
 #   if nopr.ostatok in rootdict:
 #       print('STRIKE SOLO PR')
 #       return([nopr.ostatok, nopr.maxprefix, ''],2)
# SECOND STEP END -------------------------------------------------------------
# THIRD STEP ------------------------------------------------------------------
#    sfxrtcash = {}
#    for i in get_sfx(word, stmr.gtsfx()):
#        if strip_end(word, i) in rootdict:
#           sfxrtcash.update({strip_end(word, i) : i})
#    if len(sfxrtcash) > 0 :
#        maxkey = (max(list(sfxrtcash.keys()), key = len))
#        return([maxkey, '', sfxrtcash[maxkey]],3)
#    if ((len(sfxrtcash) == 0) and (nopr.maxprefix != '')):
#        for i in get_sfx(nopr.ostatok, stmr.gtsfx()):
#            if strip_end(nopr.ostatok, i) in rootdict:
#                sfxrtcash.update({strip_end(nopr.ostatok, i) : i})
#    if len(sfxrtcash) > 0:
#        print('SUTORAIKU SFX!')    
#        maxkey = (max(list(sfxrtcash.keys()), key = len))
#        return([maxkey, nopr.maxprefix, sfxrtcash[maxkey]],3)
#   tweakword = word + get_syll(prtr)
#    print('ITO TWEAKWORD - ' + tweakword)
#    twres = recheck(tweakword)
#    if twres != None:
#        return twres
#   
#    mxsfx =  max(get_sfx(word,stmr.gtsfx()), key = len)
#    
##    rezanoe = strip_start(strip_end(word,mxsfx),stmr.gtprst())
#    rezanoe = prefixwork(strip_end(word,mxsfx))
    
#    fnl = [rezanoe.ostatok, rezanoe.maxprefix, mxsfx]
#    print(fnl)
#    print('asdasdsd')
    
#    return(fnl,4)
    
class separator:
           

    def raspil(self, word):

        self.reflexiveRemoved = False    # UBIRAEM REFLEXIVE

        word = word.lower()              # lOWERCASE
        self.originalWord = word
        if (word.endswith('ся') or word.endswith('сь')):
            word = word[:len(word)-2]
            self.reflexiveRemoved = True
        rslt = rootworks(word)
        self.root = rslt.root
        self.prefix = rslt.prefix
        self.postfix = rslt.postfix
        self.suffix = rslt.suffix
        self.extraRoot = rslt.extraRoot
        self.interfix = rslt.interfix
        self.morphList = []
        self.morphList += self.prefix + self.extraRoot + self.interfix + self.root + self.suffix + self.postfix
        
        if self.reflexiveRemoved:
            self.reflexive =  self.originalWord[-2:]
            self.morphList += [self.reflexive]
            
        self.separated = ':'.join(self.morphList)
            

    def __init__(self,word):
        self.raspil(word)
    
    
class kuznecFinder(kuznec, separator):
    def notinit(self,root, word = ''):
        if len(word) > 0:
            self.raspil(word)
        self.rootdict = {'суффикс' : [], 'префикс' : [], 'интерфикс' : [], 'флексия' : []}
        self.wordlist = []
        for word in self.worddict:
            rootFound = False
            for pos in self.worddict[word]:
                pos = self.worddict[word][pos]
               # print(pos)
                if (pos['status'] == 'корень' and pos['morph'] == root):
                    rootFound = True
                    print('NAWEL! ' + word)
                    break
            if rootFound:
                self.wordlist.append(word)
                for pos in self.worddict[word]:
                    pos = self.worddict[word][pos]
                    if pos['status'] != 'корень':
                        self.rootdict[pos['status']] += [pos['morph']]
                        
        for morph in self.rootdict:
            self.rootdict[morph] = list(set(self.rootdict[morph]))
        self.root = root
    def matchPos(self, morpheme, elist = None):
        elist = self.enumerated
        for unit in elist:
            if morpheme in unit:
                return(unit)
    def mat(self, morpheme):
        rootNum = self.matchPos(self.root)
        morphNum = self.matchPos(morpheme)
        
        delta = rootNum[1] - morphNum[1]
        return([delta,rootNum,morphNum])
    def checkPos(self, morpheme, bundle = None):
        bundle = self.mat(morpheme)
        for word in self.wordlist:
            mPos = None
            rPos = None
            for pos in self.worddict[word]:
                
                posNum = pos
                pos = self.worddict[word][pos]
                
                if pos['morph'] ==  morpheme :
                    mPos = posNum
                if pos['morph'] == self.root :
                    rPos = posNum
            if (mPos != None and rPos != None):
                empDelta = int(rPos) - int(mPos)
                if empDelta == bundle[0]:
                    print('Yeach that is the word - ' + word)
                    return(True)
                    break
        print('MORPHEME SHALL NOT PASS!')
        return(False)



class morphSplitnCheck(kuznecFinder):
    def __init__(self,word):
        self.raspil(word)

        
    def do_check(self,morph):
        self.notinit(self.root)
        self.checkPos(morph)


def goThroughCorpus(inp, outputPath):
    csvCash = 'Original\tSeparated\n'
    for item in inp:
        item = item.replace('\n','')
        t = morphSplitnCheck(item)
        csvCash += t.originalWord + '\t' + t.separated + '\n'
    dumpling = open(outputPath, 'w', encoding = 'utf-8')
    dumpling.write(csvCash)
    dumpling.close()
        
    



#adict = []    
#for i in kuznec.rootdict:
#    if i.endswith('а'):
#        adict.append(i)
        
#print(set(adict))




#########################
# FUNKTSIA DLYA RAZDELKI NA MORFEMI
# DLYA SAWI
#def get_morphs(wd):
#    wrd = raspil(wd)
#    csh = wrd[2]+':'+':'.join(wrd[1][2])
#    
#    return(list(reversed(csh.split(':'))))

    
#########################

#def finale():
#    dump = open('proverka2.txt','w',encoding = 'utf-8')
#    wcash = ''
#    for i in mistakes:
#        
#        for w in i:
#            try:
#                wrd = raspil(w)
#                wcash = wcash + 'Original : ' + w + '\n' + 'Separated: ' + wrd[2] + '\nSep. full: ' + wrd[2]+':'+':'.join(wrd[1][2]) + '\n\n\n'
#            except:
#                print('4eto powlo ne tak')
#            
#    print(wcash)
 #   dump.write(wcash)
 #   dump.close()
    


#for i in tuple(set(morphdict)):
#    if word.endswith(i):
#        print(strip_end(word,i))