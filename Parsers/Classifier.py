import sys;args=sys.argv[1:] # input is a filename
import re
import os


p=(os.path.abspath("Classifier.py"))

p=p[:-13]
if not "Reading Files" in p: p+="Reading Files/Rounds/"
DCTENG={*open(p[:-7]+"CSW19.txt",encoding='utf-8').read().splitlines()}
questions = open(p+args[0]+'.txt', encoding='utf-8').read().splitlines()
histquestions = open(p+f"Advanced_History.txt",encoding='utf-8').read().splitlines()
WORDFREQ = set()
words = "".join(histquestions).replace(",","").replace("'s",'').replace(".","").replace("?","").replace("ā",'a').replace("ē",'e').replace('ī','i').replace('ō','o').replace('ū','u').replace('ë','e').replace('ō','o').split(" ")
for word in words:
    if word and word[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and len(word)>3 and not word[1] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and not word.upper() in DCTENG: 
        WORDFREQ.add(word.lower())
WORDFREQMYTH = set()
myths = open(p+f"Advanced_Mythology.txt",encoding='utf-8').read().splitlines()
wordsmyth = "".join(myths[:len(myths)//2]).replace(",","").replace(".","").replace("'s",'').replace("ā",'a').replace("ē",'e').replace('ī','i').replace('ō','o').replace('ū','u').replace('ë','e').replace('ō','o').split(" ")
for word in wordsmyth:
    if word and word[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and len(word)>3 and not word[1] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and not word.upper() in DCTENG: 
        WORDFREQMYTH.add(word.lower())
forbiddenwordshist = {'rome','war','jupiter','juno'}
forbiddenwordsmyth = {'rome','war'}
WORDFREQ-=forbiddenwordshist
WORDFREQMYTH-=forbiddenwordsmyth
WORDFREQLIT = set()
litQs = open(p+f"Advanced_Literature.txt",encoding='utf-8').read().splitlines()
wordslit = "".join(litQs[:len(litQs)//2]).replace(",","").replace(".","").replace("'s",'').replace("ā",'a').replace("ē",'e').replace('ī','i').replace('ō','o').replace('ū','u').replace('ë','e').replace('ō','o').split(" ")
for word in wordslit:
    if word and word[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and len(word)>3 and not word[1] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and not word.upper() in DCTENG: 
        WORDFREQLIT.add(word.lower())

WORDFREQLITTEMP=set()
for itm in WORDFREQLIT:
    if itm in WORDFREQMYTH or itm in WORDFREQ:
        print(itm)
        WORDFREQ-={itm}
        WORDFREQMYTH-={itm}
    else:
        WORDFREQLITTEMP.add(itm)
WORDFREQLIT=WORDFREQLITTEMP

historyterms1500 = ['occupation','tarquinius superbus','ferentina','herdonius','jugurtha','marius','sulla','via aemilia','via popilia','via egnatia','via ignatia','via appia','via pompeia','via flaminia','via postumia','via domitia','romans call','axona','sambre','sabis','siligneus','castrensis','corona graminea','graminea','obsidionalis','tullianum','teuta','afranius burrus','burrus','bath','apodyterium','tepidarium','caldarium','frigidarium','governor','body of water','zeno','horologium','ctesiphon','cyzicus','caudine','aquaduct','aqua marcia','aqua tepula','aqua appia','aqua virgo','aqua augusta',' gens','litterator','fabius','rullianus','barbatus','grammaticus','alba longa','profession','augustus','octavian','tiberius','caligula','claudius','nero','galba','otho','vitellius','vespasian','titus','domitian','nerva','trajan','hadrian','antoninus pius','aurelius','verus','commodus','pertinax', 'was known to the romans',
            'didius','julianus','severus','caracalla','geta','macrinus','elagabalus','maximinus','gordian','pupienus','balbinus','philip','decius','valerian','gallienus','aurelian','probus','zenobia','carinus','numerian''festival','secession','plebs','plebeian','consul','aedile',
        'diocletian','maximian','constantius','constantine','maxentius','licinius','constans','valentinian','gratian','arcadius','stilicho','aetius','aëtius','valens','samnites','samnite','gauls','pompey','antony','cleopatra','mithridates','romulus','remus',' numa ','pompilius',
            'tullus hostilius','clodius','lucullus','ancus marcius','tarquin','servius tullius','paludamentum','sagum','lacerna','cucullus',' tyne','solway','suovetaurilia','suovetaurilia','cincinnatus','regillus','regulus','hannibal','ollus quiris','libitinarius', 'vestal','mola salsa']
historyterms500=['turnus','freedman','seneca','surgeon','general','chieftain','battle','circus','gladiator','chariot','arca','atrium','tablinum','tablinum','vestibulum','city','cities','curator annonae','praefectus annonae'
                 'tribune','praetor','scipio','emperor','roman life','designator','libitinarius',' term ','marriage','wedding',' toga ','praetexta','colosseum','manius','gaius','marcus','funeral','clothing','type of slave','perficae','rostra','designator']
historyterms200= [' bc ','b.c.','lex','roman','white']

religionculture = ['mystery cult','mystery religion','roman family','amita','matertera','scorpio','catapulta','statumen','carpentum','dorsum','viminal','capitoline','quirinal','janiculum','palatine','esquiline','caelian','fetiales','salii','rex sacrorum','parentalia','lupercalia','terminalia','regifugium','matronalia','liberalia','tubilustrium','hilaria','megalesia','cerealia','parilia','robigalia',
            'hibernia','britain','gaul','helvetia','defrutum','tyrotarichus','garum','epityrum','mulsum','fritillus','arbiter bibendi','paedagogus','pedisequi',
            'lemuria','bona dea','saturnalia','garumna','sequana','rhodanus','rhenus','danuvius','ister','cathedra','monopodium','sella curulis','mensa delphica','genius']
laws = ['plautia papiria','lex julia','lex iulia','canuleia','lex hortensia','licinia sextia','manilia','gabinia','titia','lex oppia','lex publilia','valeria horatia','ogulnia']
authors = ['ausonius',' catullus',' ovid','cn. naevius','cn naevius','gnaeus naevius','ennius','terence','vergil','cicero','seneca','pliny','lucan ','jerome','horace','andronicus','augustine',
              'pacuvius','reatinus','columella','italicus','accius','atax','atacinus','sallust','sisenna','lucretius','sappho','lesbia','persius','martial'
              ,'juvenal','suetonius','tacitus','petronius', ' cato','damasus','laberius','cinna','novius','nonius','josephus','quintus horatius flaccus',
              'varro','boethius','statius','symmachus','macrobius','livy','celsus','quintillian','apuleius','trebellius pollio','cordus','lampridius',
              'spartianus','syrus','claudian','ulpian','vitruvius','ammianus marcellinus']
litnothist = ['livy','pliny','ammianus marcellinus','accius','macrobius',' conte ','archilochus','horace','pro rabirio']

works = {'aeneid', 'georgics', 'eclogues', 'copa', 'ciris', 'moretum', 'catalepton', 'aetna', 'dirae',
        'metamorphoses', 'ars amatoria', 'remedia amoris', 'amores', 'heroides', 'fasti', 'tristia', 'epistulae ex ponto', 'medea', 'ibis',
        'pharsalia', 'bellum civile',
        'thebaid', 'achilleid', 'silvae',
        'argonautica',
        'punica',
        'de rerum natura',
        'odes', 'epodes', 'satires', 'epistles', 'ars poetica', 'carmen saeculare', 'epistulae ad pisones', 'epodes', 'satirae',
        'epigrams','elegies','miles gloriosus', 'the braggart soldier', 'aulularia', 'the pot of gold', 'asinaria', "the donkey's story", 'amphitryon', 'captivi', 'the captives', 'truculentus', 'the hard-hearted',
        'andria', 'the woman from Andros', 'heauton timorumenos', 'the self-tormentor', 'eunuchus', 'the eunuch', 'phormio', 'adelfae', 
         'de clementia', 'on clemency', 'de ira', 'on anger', 'de brevitate vitae', 'on the shortness of life', 'de vita beata', 'on the happy life', 'naturales quaestiones',
        'hedyphagetica','argonautica','ab urbe condita','de oratore','de vita','de analogia','ibis','haleutica','ars amatoria','remedia amoris','naturalis historia','origines','de inventione','partitiones',
         'de verborum significatu','golden ass','asinus aureus','achilleid','de medicina','de re coquinaria','institutio oratoria','ars amatoria','remedia amoris','metamorphoses','amores','heroides','fasti','tristia','epistulae ex ponto','medea','ibis',
'aeneid','georgics','eclogues','copa','ciris','culex','moretum','catalepton','aetna','dirae',
'carmina','epodes','odes','satires','ars poetica','carmen saeculare','epistles','epistula ad pisones','odes liber iv','sermones',
'annales','historiae','germania','agricola','dialogus de oratoribus','vita agricolae','de origine et situ germanorum','annales liber i','historiae liber iv','agricola vita',
'commentarii de bello gallico','commentarii de bello civili','de bello africano','de bello hispaniensi','de bello alexandrino','bellum gallicum liber i','bellum civile liber i','bellum gallicum liber vii','bellum civile liber iii','bellum gallicum liber vi',
'de rerum natura','hymnus ad venerem','de rerum natura liber i','de rerum natura liber ii','de rerum natura liber iii','de rerum natura liber iv','de rerum natura liber v','de rerum natura liber vi','epicurea','natura rerum',
'catilina','bellum catilinae','bellum iugurthinum','historiae fragmenta','epistulae ad caesarem','oratio macri','epistulae ad senatum','invectiva in ciceronem','historiae liber i','bellum iugurthinum liber',
'epistulae','epistulae morales','de brevitate vitae','de ira','de clementia','de providentia','apocolocyntosis','thyestes','phaedra',
'ab urbe condita','ab urbe condita liber i','ab urbe condita liber v','ab urbe condita liber x','ab urbe condita liber xxi','ab urbe condita liber xxx','ab urbe condita liber xxxiv','ab urbe condita liber xl','ab urbe condita liber xlv','periochae',
'carmina','catulli carmina','epithalamium','attidis','epyllion','poema 64','poema 5','poema 43','poema 85','poema 101',
'pharsalia','bellum civile','pharsalia liber i','pharsalia liber ii','pharsalia liber vii','pharsalia liber ix','pharsalia liber x','bellum civile liber iv','bellum civile liber vi','bellum civile liber viii',
'in catilinam','pro caelio','pro archia','pro milone','de amicitia','de senectute','de officiis','de republica','de legibus',
'in verrem','philippicae','brutus','orator','de oratore','partitiones oratoriae','topica','academica','tusculanae disputationes','somnium scipionis',
'fabulae','phaedri fabulae','fabulae aesopiae','fabula lupus et agnus','fabula canis et umbra','fabula vulpes et uva','fabula ranae','fabula lupus et grus','fabula canis et lupus','fabula asinus et leo',
'satyricon','cena trimalchionis','bellum civile petronii','epigrammata','poemata','fabulae milesiae','fragmenta petronii','epigramma','novellae','prosimetrum',
'epigrammata','liber epigrammaton','xenia','apophoreta','epigrammata liber i','epigrammata liber iv','epigrammata liber x','epigrammata liber xii','epigrammata liber xiv','epigrammata liber xv'
 ,'cynegetica'       
        }
works={*works}
litTerms600= ['patavenitas','bible','what meter','pimp','rhetorician','lawyer','jurist','domitian']
litTerms200=['author']
litTerms500=['coined','work of','literature','latin literature','glaucoma','hariolus','triphallus','dolus','mastigophorous','pseudolus','aulularia','amphitruo','asinaria','bacchides','captivi','casina','cistellaria','curculio','epidicus','menaechmi','mercator','miles gloriosus','mostellaria','persa','poenulus','pseudolus','rudens','stichus','trinummus','truculentus','vidularia']
litTerms5000 = ['apologist','montanism','de lapsis','what work','plautine play','plautine comedy','142 books','142','what poemp','what epic','what meter','elegaic couplet','dactylic hexameter','sapphic strophe','attellan farce','translated the old testament','translate the old testament','who wrote','what author','what book','what play','what genre','fabula palliata','fabulae palliatae','fabulae praetextae','fabula praetexta','fabula cothurnata','cena trimalchionis','satyricon','apocolocyntosis',
                'what play of plautus','what play of terence','what play by plautus','zmyrna','mime ','mimes','riciniatae','planipedes','tragedian','comedian','playwright','satirist','elegist',
                'archilochus','lock of berenice','callimachus','menippean','sedigitus','periochae','clinamen','alimentus','palaemon']

mythTerms200 = ['princess']
mythTerms1500 = ['mythological','mythology','atlantis','evenor','albula']
mythNotLit = {'trophonius','agamedes','prometheus','moirai','aphrodite','demeter','hestia','hecate','aesacus','cebren','hesperia','laocoon','daedalus', 'icarus',  'daphne', 'jupiter', 'juno', 'narcissus', 'echo', 'hermes', 'persephone', 'orphus', 'europa', 'pheaton', 'baucis', 'philemon', 'alcyone', 'clymene', 'pyrrha', 'deucalion', 'niobe', 'arachne', 
            'ares', 'minerva', 'lycaon', 'callisto', 'actaeon', 'tantalus', 'alpheus', 'arethusa', 'latona', 'vulcan', 'venus', 'adonis', 'pyramus', 'thisbe', 'hercules', 'meleager', 'atalanta', 'pelops', 'hippodamia', 'midas', 'midus', 
            'bellerophon', 'chimera', 'pegasus', 'phaethon', 'cassandra', 'tithonus', 'perseus', 'andromeda', 'medusa', 'midas', 'glaucus', 'scylla', 'charybdis', 'clytemnestra', 'aegeus', 'theseus', 'ariadne', 'minotaur', 'zeus', 'lycaon', 
            'neptune', 'ceres', 'proserpina', 'dionysus', 'nymphs', 'satyrs', ' pan ', 'alcyone', 'pyramus', 'thisbe', 'daedalus', 'nymphs', 'syrinx',  'alpheus', 'arethusa', 'dryope', 'lotis', 'cinyras', 'myrrha', 'adonis', 'venus', 
            'persephone', 'zephyrus', 'flora', 'meleager', 'heracles', 'tantalus', 'orion', 'scylla', 'glaucus', 'circe', 'medea', 'teiresias', 'juno', 'pluto', 'cerberus','persephone', 'zeus', 'athena', 'selene', 'ares', 'hermes',  
            'sisyphus', 'creon', 'leucothea', 'phrixus', 'hellen', 'arion', 'midas', 'adrasteia', 'typhon', 'chaos',  'rhea', 'hebe', 'pallus', 'luna', 'pyramus', 'thisbe', 'alcyone', 'halcyon', 'juno', 'charon', 'pluto', 'semele', 'bacchus', 
            'cerberus', 'talus', 'circe', 'medusa', 'heracles', 'nymphs', 'ecbatus', 'tithonus', 'nymphs', 'clymene', 'boreas', 'hylas', 'phyllis', 'proserpina', 'hephaestus', 'tantalus', 'daphne', 'alpheus', 'arethusa', 'cicones', 'leda', 'morpheus', 
            'endor', 'genus', 'andromeda', 'pegasus', 'oceanus', 'tethys', 'calypso', 'ceres', 'mimnermus', 'anaxarete', 'cassandra', ' iris ', 'niobe', 'clytemnestra', 'romulus', 'remus', 'ganymede', 'althea' , 'nymphs', 'arcas', 'arisbe', 'hippomenes', 
            'atalanta', 'hippopotamus', 'adrasteia', 'aeneas', 'aegeus', 'phalantes', 'teiresias', 'oeneus', 'hypsipyle', 'hermes', 'autolycus', 'cephissus', 'echo', 'zeus', 'juno',  'heracles', 'cerberus', 'nymphs',
            'eneas', 'dido', 'anchises', 'ascanius', 'venus', 'jupiter', 'juno', 'mercury', 'neptune', 'mars', 'turnus', 'latinus', 'lavinia', 'king mezentius', 'camilla', 'pallas', 'evander', 'ulixes', 'aeneas', 'diomedes', 'belinus', 'sabinus', 'tarchon',  'camilla', 'sybilla', 'achates', 'aesacus', 'hibernia', 'misenus', 'samo', 'caeneas', 'ulixes', 'clytemnestra', 'cerberus', 'deiphobus', 'anchemolus', 'sarpedon', 'glaucus', 'aeolus', 'scyllae', 'charybdis', 'turnus', 'sylvan', 'laocoon', 'acestes', 'neptune', 'creusa', 'hector', 'pallas', 'minerva', 'bittius', 'turii', 'sibylla', 'alcides', 'cacus', 'nymphs', 'eurus', 'pleurathus', 'clymene', 'metabus', 'saticula', 'pyrrhus', 'laomedon', 'lycius', 'aeetes', 'saturnia', 'latium', 'diones', 'pallas', 'anteius', 'polyxena', 'pallas', 'tiryns', 'centaur', 'camilla'}
count = 0
counts={"Myth:":0,"Hist:":0,"Lang:":0,"Lit:":0}

for question in questions:
    q=question.lower()
    q=q.replace("ā",'a').replace("ē",'e').replace('ī','i').replace('ō','o').replace('ū','u').replace('ë','e').replace('ō','o')
    mythWeight = 0
    histWeight = 0
    langWeight = 0
    litWeight = 0

    #Literature
    for itm in litnothist:
        if itm in q:
            litWeight+=1000
            histWeight-=10000
    for itm in litTerms200:
        if " "+itm+" " in q or "\n"+itm in q and not 'authority' in q:
            litWeight+=200
            histWeight-=100
    for itm in litTerms5000:
        if " "+itm in q or "\n"+itm in q: 
            litWeight+=5000
            #print(itm,"AHA")
            langWeight-=1000
    for itm in authors:
        foundlangstuff=False
        if itm in q and not 'saturninus' in q and not 'macro' in q:            
            litWeight+=3500
            #print(itm,"AHA")
            histWeight-=2000
            mythWeight-=2000
        if 'work of' in q and itm in q:
            litWeight+=600
            langWeight-=500
    for itm in works:
        if itm in q or itm in q:
            litWeight+=5000
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
    for itm in WORDFREQLIT:
        if " "+itm in q or "\n"+itm in q:
            litWeight+=1000
    
    #History
    if 'praenomen' in q and 'abbreviated' in q:histWeight+=5000
    if 'of the following cities' in q or 'of the following provinces' in q:histWeight+=5000
    if 'province' in q:histWeight+=2000
    if 'according to'  in q and ('livy' in q or 'tacitus' in q): 
        litWeight-=1000
        histWeight+=2000
    if'described by' in q and ('livy' in q or 'tacitus' in q):
        litWeight-=1000
        histWeight+=2000
    for law in laws:
        if law in q:
            langWeight-=5000
            litWeight-=5000
            histWeight+=5000
    for thing in religionculture:
        if thing in q:
            histWeight+=5000
            litWeight-=1000
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
    for term in historyterms200:
        if term in q:
            histWeight+=200
            langWeight-=25
    for itm in WORDFREQ:
        if itm in q:
            histWeight+=2000

    #Myth:
    for itm in WORDFREQMYTH:
        if " "+itm in q or "\n"+itm in q:
            mythWeight+=1000
    for itm in mythNotLit:
        if itm in q:
            mythWeight+=3000
            if not ('vergil' in q and 'aeneid' in q):
                litWeight-=3000
    if 'who speaks the following' in q:
        mythWeight+=7000
    if 'according to' in q and 'ovid' in q:
        mythWeight+=2000
        litWeight-=2000
    for itm in mythTerms1500:
        if itm in q:
            if not itm in WORDFREQLIT:
                mythWeight+=1500
    #Language
    if 'andronicus' in q:langWeight-=5000
    if "please listen" in q or "following passage" in q or "listen carefully" in q or "question that follows" in q:langWeight+=5000 #picks out passage questions
    if not "translated" in q and "translate" in q and ("english" in q or "latin" in q) and not 'andronicus' in q and not 'jerome' in q:  langWeight+=5000 #picks out translation questions
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
    if "say in Latin" in q: langWeight+=5000
    for a in ['ablative','dative','accusative','nominative','vocative','genitive','locative']:
        if a in q:langWeight+=100
        if ("what use" in q  or 'the use' in q) and a in q:langWeight+=500
    if 'what case' in q: langWeight+=6000
    for a in ['subjunctive','imperative','indicative','infinitive']:
        if a in q:
            langWeight+=200*q.count(a)
            if "what use" in q or 'the use' in q:langWeight+=5000
    if 'interjection' in q: langWeight+=300
    if 'qua latina' in q:langWeight+=5000
    if "as prose" in q:langWeight+=5000
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
    #if category=="":
        #print(q,histWeight,litWeight,mythWeight,langWeight)
print(len(questions))
for itm in counts:
    print(itm,counts[itm])