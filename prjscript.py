from nltk.stem import snowball as stem

vowels = ['а', 'у', 'о', 'ы', 'и', 'э', 'я', 'ю', 'ё', 'е']
"""
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

mist.close()"""
stmr = stem.RussianStemmer()

# for item in mistakes:
 #   cash = []
 #   for word in item:
 #       cash.append(stmr.stem(word))
#    print(cash)



class kuznec:

    worddict = {}
    rootdict = []
    
    cashline = []
    
    with open('resources/morphodict.csv', 'r', encoding = 'utf-8') as slovar:
        next(slovar)
    
        for line in slovar:
            line = line.split(';')
            if line[0] not in worddict:
                worddict[line[0]] = {}  
    
            worddict[line[0]].update({line[3] : {'morph' : line[1], 'status' : line[2], 'place' : line[3], 'allo' : line[4], 'pos' : line[5].replace('\n','')}})
            if line[2] == 'корень':
                rootdict.append(line[1])
                
    
#        cashline = [line[0]]
#        if tuple(line[2],line[1]) not in cash:
#            cash.append(tuple(line[2],line[1]))
            
kuzdra = kuznec()
rootdict = kuzdra.rootdict



                
            
    
        



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
                # print(' CLASSNAJA Приставка ' + i + ' !!!')
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
                # print(' CLASSNAJA okon4anie ' + i + ' !!!')
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
    
    
    
def recheck(word):
    print('RECHECK WITH PRSYLL IS BEING RUN')
    print(word)
    if word in rootdict:
        print('STRIKE WORD')
        return((word,1))
# A-ROOT STEP -----------------------------------------------------------------
    if word.endswith('а'):
        arootDict = []
        for i in stmr.gtart():
            if word.endswith(i):
                arootDict.append(i)
        if len(arootDict) > 0:
            maxARoot = (max(arootDict, key = len))
            prst = word[:len(word) - len(maxARoot)]
            if prst in stmr.gtprst(): 
                print('STRIKE A-ROOT')
                return([maxARoot, prst, ''],5)

    nopr = prefixwork(word)
    if nopr.ostatok in rootdict:
        print('STRIKE SOLO PR')
        return([nopr.ostatok, nopr.maxprefix, ''],2)
    sfxrtcash = {}
    for i in get_sfx(word, stmr.gtsfx()):
        if strip_end(word, i) in rootdict:
            sfxrtcash.update({strip_end(word, i) : i})
    if len(sfxrtcash) > 0 :
        maxkey = (max(list(sfxrtcash.keys()), key = len))
        return([maxkey, '', sfxrtcash[maxkey]],3)
    if ((len(sfxrtcash) == 0) and (nopr.maxprefix != '')):
        for i in get_sfx(nopr.ostatok, stmr.gtsfx()):
            if strip_end(nopr.ostatok, i) in rootdict:
                sfxrtcash.update({strip_end(nopr.ostatok, i) : i})
    if len(sfxrtcash) > 0:
        print('SUTORAIKU SFX!')    
        maxkey = (max(list(sfxrtcash.keys()), key = len))
        return([maxkey, nopr.maxprefix, sfxrtcash[maxkey]],3)
    
        
          
def hicc():
    print('a')         
  
              
    
def get_root(text):
    global prtr
    word = postfixwork(text)
    prtr = word.maxpostfix
    word = word.ostatok
#    word = stmr.stemmmm(text)[1]
#    prtr = stmr.stemmmm(text)[2][0]
    print(prtr)
    print(word)
    nopr = None
#    print(word)
#    fst = 
#    ffst = strip_end(word, stmr.gtsfx())
#    fnl = strip_start(strip_end(word,stmr.gtsfx())[0],stmr.gtprst())

    
# FIRST STEP ------------------------------------------------------------------    
    if word in rootdict:
        print('STRIKE WORD')
        return((word,1))
# FIRST STEP END --------------------------------------------------------------
# A-ROOT STEP -----------------------------------------------------------------
    if word.endswith('а'):
        arootDict = []
        for i in stmr.gtart():
#            print(i)
            if word.endswith(i):
                arootDict.append(i)
        if len(arootDict) > 0:
            maxARoot = (max(arootDict, key = len))
            prst = word[:len(word) - len(maxARoot)]
            if prst in stmr.gtprst(): 
                print('STRIKE A-ROOT')
                return([maxARoot, prst, ''],5)

# SECOND STEP -----------------------------------------------------------------
    nopr = prefixwork(word)
    if nopr.ostatok in rootdict:
        print('STRIKE SOLO PR')
        return([nopr.ostatok, nopr.maxprefix, ''],2)
# SECOND STEP END -------------------------------------------------------------
# THIRD STEP ------------------------------------------------------------------
    sfxrtcash = {}
    for i in get_sfx(word, stmr.gtsfx()):
        if strip_end(word, i) in rootdict:
            sfxrtcash.update({strip_end(word, i) : i})
    if len(sfxrtcash) > 0 :
        maxkey = (max(list(sfxrtcash.keys()), key = len))
        return([maxkey, '', sfxrtcash[maxkey]],3)
    if ((len(sfxrtcash) == 0) and (nopr.maxprefix != '')):
        for i in get_sfx(nopr.ostatok, stmr.gtsfx()):
            if strip_end(nopr.ostatok, i) in rootdict:
                sfxrtcash.update({strip_end(nopr.ostatok, i) : i})
    if len(sfxrtcash) > 0:
        print('SUTORAIKU SFX!')    
        maxkey = (max(list(sfxrtcash.keys()), key = len))
        return([maxkey, nopr.maxprefix, sfxrtcash[maxkey]],3)
    tweakword = word + get_syll(prtr)
    print('ITO TWEAKWORD - ' + tweakword)
    twres = recheck(tweakword)
    if twres != None:
        return twres
   
    mxsfx =  max(get_sfx(word,stmr.gtsfx()), key = len)
    
#    rezanoe = strip_start(strip_end(word,mxsfx),stmr.gtprst())
    rezanoe = prefixwork(strip_end(word,mxsfx))
    
    fnl = [rezanoe.ostatok, rezanoe.maxprefix, mxsfx]
#    print(fnl)
#    print('asdasdsd')
    
    return(fnl,4)
    
        
#--------------------------------------------------------------------------------------------
# BACKUP
#
#
#def get_root(text):
#    word = stmr.stemmmm(text)[1]
#    print(word)
#    print(word)
#    fst = 
#    ffst = strip_end(word, stmr.gtsfx())
#    fnl = strip_start(strip_end(word,stmr.gtsfx())[0],stmr.gtprst())
#    if word in rootdict:
#        print('STRIKE WORD')
#        return((word,1))
#    nopr = strip_start(word, stmr.gtprst())
#    if nopr[0] in rootdict:
#        print('STRIKE SOLO PR')
#        return([nopr[0],nopr[1],''],2)
#    sfxrtcash = {}
#    for i in get_sfx(word, stmr.gtsfx()):
#        if strip_end(word, i) in rootdict:
#            sfxrtcash.update({strip_end(word, i) : i})
#    if len(sfxrtcash) > 0 :
#        maxkey = (max(list(sfxrtcash.keys()), key = len))
#        return([maxkey, '', sfxrtcash[maxkey]],3)
#    if ((len(sfxrtcash) == 0) and (nopr[1] != '')):
#        for i in get_sfx(nopr[0], stmr.gtsfx()):
#            if strip_end(nopr[0], i) in rootdict:
#                sfxrtcash.update({strip_end(nopr[0], i) : i})
#    if len(sfxrtcash) > 0:
#        print('SUTORAIKU SFX!')    
#        maxkey = (max(list(sfxrtcash.keys()), key = len))
#        return([maxkey, nopr[1], sfxrtcash[maxkey]],3)
#    mxsfx =  max(get_sfx(word,stmr.gtsfx()), key = len)
#    rezanoe = strip_start(strip_end(word,mxsfx),stmr.gtprst())
#    fnl = [rezanoe[0], rezanoe[1], mxsfx]
#    print(fnl)
#    print('asdasdsd')
    
#    return(fnl,4)
    
#-----------------------------------------------------------------------------------------------








       
    
    
    
#         return(([fnl[0],fst[1],ffst[1]],4))
            
#       else: 
#           return(([fnl[0],fst[1],ffst[1]],5))
            
        
class separator:
           

    def raspil(self, word):
        self.reflexiveRemoved = False
        word = word.lower()
        self.originalWord = word
        if (word.endswith('ся') or word.endswith('сь')):
            word = word[:len(word)-2]
            self.reflexiveRemoved = True
        stcash = stmr.stemmmm(word)
        self.stcash = stcash
        
        rslt = get_root(word)
        self.initOutcome = rslt
        if rslt[1] != 1:
            root = rslt[0][0]
            pr = rslt[0][1]
            sfx = rslt[0][2]
            self.root = root
            self.prefix = pr
            self.suffix = sfx
            
            self.morphList = [self.prefix,self.root,self.suffix]
            
            print('MORPHEMES AVAILABLE')
        
            popil = pr + ':' + root + ':' + sfx   
            self.separated = ''
            for i in self.morphList:
                if len(i) > 0:
                    self.separated += i + ':'
            self.separated += ':'.join(stmr.suffixlist)
            if self.separated.endswith(':'):
                self.separated[:-1]
        else:
            popil = rslt[0]
            self.root = popil
            self.morphList = [self.root]
            self.separated = self.root + ':' + ':'.join(stmr.suffixlist)
            if self.separated.endswith(':'):
                self.separated[:-1]
        if self.reflexiveRemoved:
            
            self.separated = self.separated + ':' + self.originalWord[-2:]
        
        self.enumerated = []
        
        for i,m in enumerate(self.morphList):
            self.enumerated.append((m,i))
        
#        print(rslt[0])
    #    print(stcash)
        
        return([rslt,stcash[:3], popil])
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
        self.postfix = prtr
        
    def do_check(self,morph):
        self.notinit(self.root)
        self.checkPos(morph)


def goThroughCorpus(inp, outputPath):
    csvCash = 'Original\tSeparated\n'
    for item in inp:
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
