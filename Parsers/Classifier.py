import sys;args=sys.argv[1:] # input is a filename
import re
import os


p=(os.path.abspath("Classifier.py"))

p=p[:-13]
if not "Reading Files" in p: p+="Reading Files/Rounds/"
DCTENG={*open(p[:-7]+"CSW19.txt",encoding='utf-8').read().splitlines()}
questions = open(p+f"Advanced_History.txt",encoding='utf-8').read().splitlines()

WORDFREQ = set()
words = "".join(questions).split(" ")
for word in words:
    if word and word[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and len(word)>3 and not word[1] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and not word.upper() in DCTENG: 
        WORDFREQ.add(word)
WORDFREQMYTH = set()
myths = open(p+f"Advanced_Mythology.txt",encoding='utf-8').read().splitlines()
wordsmyth = "".join(myths).split(" ")
for word in wordsmyth:
    if word and word[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and len(word)>3 and not word[1] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and not word.upper() in DCTENG: 
        WORDFREQMYTH.add(word)
forbiddenwordshist = {'rome','war','jupiter','juno'}
forbiddenwordsmyth = {'rome','war'}
WORDFREQ-=forbiddenwordshist
WORDFREQMYTH-=forbiddenwordsmyth

historyterms1500 = ['bath','apodyterium','tepidarium','caldarium','frigidarium','governor','body of water','zeno','horologium','ctesiphon','cyzicus','caudine','aquaduct','aqua marcia','aqua tepula','aqua appia','aqua virgo','aqua augusta',' gens','litterator','fabius','rullianus','barbatus','grammaticus','alba longa','profession','augustus','octavian','tiberius','caligula','claudius','nero','galba','otho','vitellius','vespasian','titus','domitian','nerva','trajan','hadrian','antoninus pius','aurelius','verus','commodus','pertinax', 'was known to the romans',
            'didius','julianus','severus','caracalla','geta','macrinus','elagabalus','maximinus','gordian','pupienus','balbinus','philip','decius','valerian','gallienus','aurelian','probus','zenobia','carinus','numerian'
            ,'diocletian','maximian','constantius','constantine','maxentius','licinius','constans','valentinian','gratian','arcadius','stilicho','aetius','aëtius','valens','samnites','samnite','gauls','pompey','antony','cleopatra','mithridates','romulus','remus',' numa ','pompilius',
            'tullus hostilius','clodius','lucullus','ancus marcius','tarquin','servius tullius','paludamentum','sagum','lacerna','cucullus',' tyne','solway','suovetaurilia','suovetaurilia','cincinnatus','regillus','regulus','hannibal','ollus quiris','libitinarius', 'vestal','mola salsa']
historyterms500=['occupation','surgeon','general','chieftain','battle','circus','gladiator','chariot','arca','atrium','tablinum','tablinum','vestibulum','city','cities','festival','secession','plebs','plebeian','consul','aedile','curator annonae','praefectus annonae'
                 'tribune','praetor','scipio','emperor','roman life','designator','libitinarius',' term ','marriage','wedding',' toga ','praetexta','colosseum','manius','gaius','marcus','funeral','clothing','type of slave','perficae','rostra','designator']
historyterms50= [' bc ','b.c.','lex']

religion = ['fetiales','salii','rex sacrorum','parentalia','lupercalia','terminalia','regifugium','matronalia','liberalia','tubilustrium','hilaria','megalesia','cerealia','parilia','robigalia',
            'lemuria','bona dea','saturnalia']
laws = ['plautia papiria','lex julia','lex iulia','canuleia','lex hortensia','licinia sextia','manilia','gabinia','titia','lex oppia','lex publilia','valeria horatia','ogulnia']
authors = [' catullus',' ovid','cn. naevius','cn naevius','gnaeus naevius','ennius','terence','vergil','cicero','seneca','pliny','lucan ','jerome','horace','andronicus','augustine',
              'pacuvius','reatinus','columella','italicus','accius','atax','atacinus','sallust','sisenna','lucretius','sappho','lesbia','persius','martial'
              ,'juvenal','suetonius','tacitus','petronius', ' cato','damasus','laberius','cinna','novius','nonius','josephus','quintus horatius flaccus',
              'varro','boethius','statius','symmachus','macrobius','livy','celsus','quintillian','apuleius','trebellius pollio','cordus','lampridius',
              'spartianus','syrus','claudian','ulpian']
works = ['de oratore','de vita','de analogia','ibis','haleutica','ars amatoria','remedia amoris','naturalis historia','origines','de inventione','partitiones',
         'de verborum significatu','golden ass','asinus aureus','achilleid','de medicina','de re coquinaria','institutio oratoria']
litTerms600= ['bible','what meter','pimp','rhetorician','lawyer','jurist']
litTerms200=['author']
litTerms500=['coined','work of','literature','latin literature','glaucoma','hariolus','triphallus','dolus','mastigophorous','pseudolus','aulularia','amphitruo','asinaria','bacchides','captivi','casina','cistellaria','curculio','epidicus','menaechmi','mercator','miles gloriosus','mostellaria','persa','poenulus','pseudolus','rudens','stichus','trinummus','truculentus','vidularia']
litTerms5000 = ['attellan farce','translated the old testament','translate the old testament','who wrote','what author','what book','what play','what genre','fabula palliata','fabula praetexta','fabula cothurnata','cena trimalchionis','satyricon','apocolocyntosis',
                'what play of plautus','what play of terence','what play by plautus','zmyrna','mime ','mimes','riciniatae','planipedes','tragedian','comedian','playwright','satirist','elegist',
                'archilochus','lock of berenice','callimachus','menippean','sedigitus','periochae','clinamen','alimentus','palaemon']
mythTerms200 = ['princess']

count = 0
counts={"Myth:":0,"Hist:":0,"Lang:":0,"Lit:":0}

for question in questions:
    q=question.lower()
    q=q.replace("ā",'a').replace("ē",'e').replace('ī','i').replace('ō','o').replace('ū','u')
    mythWeight = 0
    histWeight = 0
    langWeight = 0
    litWeight = 0

    #Literature
    
    for itm in litTerms200:
        if " "+itm+" " in q or "\n"+itm in q and not 'authority' in q:
            
            litWeight+=200
            histWeight-=100
    for itm in litTerms5000:
        if " "+itm in q or "\n"+itm in q: 
            litWeight+=5000
            langWeight-=1000
    for itm in authors:
        

        foundlangstuff=False
        if " "+itm+" " in q or "\n"+itm in q and not 'saturninus' in q and not 'macro' in q:
            print(itm,q)
            
            litWeight+=1000
            histWeight+=500
            if 'word' in q and not foundlangstuff:
                foundlangstuff=True
                litWeight-=200
            if 'phrase' in q and not foundlangstuff:
                litWeight-=200
                foundlangstuff=True
            langWeight+=200
        if 'work of' in q and itm in q:

            litWeight+=600
            langWeight-=500
    for itm in works:
        if " "+itm in q or "\n"+itm in q:

            litWeight+=1000
    for itm in litTerms600:
        if " "+itm in q or "\n"+itm in q:

            litWeight+=600
            langWeight-=8000
    for itm in litTerms500:
        if " "+itm in q or "\n"+itm in q:

            litWeight+=400
            langWeight-=500
    for i in range(150):
        if f"{i}-book" in q or f"{i} book" in q: litWeight+=500

    #History
    if 'praenomen' in q and 'abbreviated' in q:histWeight+=5000
    if 'of the following cities' in q or 'of the following provinces' in q:histWeight+=5000
    if 'province' in q:histWeight+=1500
    if 'food' in q or 'house' in q:litWeight-=1000
    for law in laws:
        if law in q:
            litWeight-=500
            langWeight-=500
            histWeight+=500
    for thing in religion:
        if thing in q:
            histWeight+=700
            litWeight-=100
            langWeight-=400
            mythWeight-=400
    for term in historyterms1500:
        if term in q:
            histWeight+=1500
            langWeight-=100
            litWeight-=500
    for term in historyterms500:
        if term in q:
            histWeight+=500
            langWeight-=50
    for term in historyterms50:
        if term in q:
            histWeight+=50
            langWeight-=25
    for itm in WORDFREQ:
        if itm in q:
            histWeight+=200

    #Myth:
    for itm in WORDFREQMYTH:
        if " "+itm in q or "\n"+itm in q:
            mythWeight+=400
    
    #Language
    if 'andronicus' in q:langWeight-=5000
    if "please listen" in q or "following passage" in q or "listen carefully" in q or "question that follows" in q:langWeight+=1500 #picks out passage questions
    if not "translated" in q and "translate" in q and ("english" in q or "latin" in q) and not 'andronicus' in q and not 'jerome' in q:  langWeight+=1000 #picks out translation questions
    elif 'translate' in q and not 'andronicus' in q and not 'jerome' in q:langWeight+=400
    if 'say in latin' in q: langWeight+=1000
    if "quid anglice" in q or "quid anglice" in q: langWeight+=500 #picks out vocab
    if "welcome to the" in q or "cinema romana" in q or "bibliotecha romana" in q or 'spotificio' in q or 'spotificio' in q or "romana" in q:
        langWeight+=500 #cinema Romana, etc
    if "for the verb" in q or "for the phrase" in q: langWeight+=500 
    if "latin phrase" in q:
        langWeight+=200*q.count('latin phrase')
        if 'means' in q: langWeight+=500
    if 'diminutive' in q:langWeight+=200
    if "meaning" in q or 'means' in q:langWeight+=100
    if "at the root" in q: langWeight+=400
    if "noun" in q or "verb" in q or "adjective" in q or "adverb" in q or "preposition" in q:langWeight+=500
    if "say in Latin" in q: langWeight+=500
    for a in ['ablative','dative','accusative','nominative','vocative','genitive','locative']:
        if a in q:langWeight+=100
        if ("what use" in q  or 'the use' in q) and a in q:langWeight+=500
    if 'what case' in q: langWeight+=600
    for a in ['subjunctive','imperative','indicative','infinitive']:
        if a in q:
            langWeight+=200*q.count(a)
            if "what use" in q or 'the use' in q:langWeight+=500
    if 'interjection' in q: langWeight+=300
    if 'qua latina' in q:langWeight+=500
    if "as prose" in q:langWeight+=500
    if 'synonym' in q or 'antonym' in q or ('shares' in q and 'meaning' in q):langWeight+=200
    if "in latin" in q:langWeight+=200
    if "rhetorical device" in q or 'literary device' in q:
        litWeight-=3000
        langWeight+=5000
    if "which of the following words" in q: langWeight+=500
    if "is not derived" in q or "are not derived" in q:langWeight+=500
    if "is derived" in q or "are derived" in q or "derives" in q or "does not derive" in q:langWeight+=500
    if "derivative" in q or "derivation" in q:langWeight+=300
    if "grammatical" in q: langWeight+=100
    if "abbreviation" in q or 'abbreviated' in q: langWeight+=300
    if  "motto" in q:langWeight+=1000
    if "latin word" in q:langWeight+=100
    if "1st person" in q or "2nd person" in q or "3rd person" in q:langWeight+=200
    if "legal term" in question:langWeight+=100
    if 'quotes' in q:langWeight+=400
    if 'is being described' in q or 'is described' in q:langWeight+=1000
    if 'of the words' in q:
        langWeight+=500
        histWeight+=50
    if 'analogy' in q: langWeight+=500
    if 'form of' in q: langWeight+=500
    if 'latin form' in q:langWeight+=200
    if 'clama anglice' in q or 'dic anglice' in q or 'responde latine' in q or 'responde anglice' in q: langWeight+=300
    if 'describamus' in q:langWeight+=1000
    if 'following command' in q or 'perform or describe' in q: langWeight+=700
    if 'following sentence' in q or 'following latin sentence' in q: langWeight+=800
    if 'conditional' in q:langWeight+=700
    if 'comparative' in q or'superlative' in q or 'positive' in q:
        langWeight+=100
        if 'form' in q:langWeight+=500
    if ('due to' in q or 'because of' in q) and ('gender' in q or 'case' in q or 'tense' in q or 'grammar' in q or 'grammatical' in q):
        langWeight+=500
    if 'classical latin' in q:langWeight+=600

    category = ""
    #Select category
    if langWeight>histWeight and langWeight>mythWeight and langWeight>litWeight:
        category="Language"
        counts['Lang:']=counts['Lang:']+1
    elif histWeight>mythWeight and histWeight>litWeight:
        category="History"
        counts['Hist:']=counts['Hist:']+1
    elif mythWeight>litWeight:
        category="Mythology"
        counts['Myth:']=counts['Myth:']+1
    else:
        category="Literature"
        counts['Lit:']=counts['Lit:']+1
    #if category!='History' and category=='Literature':
        #print(question,category)
print(count,len(questions))
for itm in counts:
    print(itm,counts[itm])