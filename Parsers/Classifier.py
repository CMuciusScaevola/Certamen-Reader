import sys;args=sys.argv[1:] # input is a filename
import re
import os

file = args[0]

p=(os.path.abspath("Classifier.py"))
lvl = args[0].split("_")[0]
if lvl[-2:]=="dE" or lvl[-2:]=="eE":
        lvl=lvl[:-1]
p=p[:-13]
if not "Reading Files" in p: p+="Reading Files/Rounds/"
DCTENG={*open(p[:-7]+"CSW19.txt",encoding='utf-8').read().splitlines()}
questions = open(p+lvl+"/"+args[0]+'_Parsed.txt', encoding='utf-8').read().splitlines()
histquestions = (open(p+"Advanced/"+f"Advanced_History.txt",encoding='utf-8').read()+open(p+"Intermediate/"+f"Intermediate_History.txt",encoding='utf-8').read()).splitlines()
WORDFREQ = set()
words = "".join(histquestions).replace(",","").replace("'s",'').replace(".","").replace("?","").replace("ā",'a').replace("?","").replace("ē",'e').replace('ī','i').replace('ō','o').replace('ū','u').replace('ë','e').replace('ō','o').split(" ")
for word in words:
    if word and word[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and len(word)>3 and not word[1] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and not word.upper() in DCTENG: 
        WORDFREQ.add(word.lower())
WORDFREQMYTH = set()
myths = (open(p+"Advanced/"+f"Advanced_Mythology.txt",encoding='utf-8').read()+open(p+f"Intermediate/Intermediate_Mythology.txt",encoding='utf-8').read()).splitlines()
wordsmyth = "".join(myths[:len(myths)//2]).replace(",","").replace(".","").replace("'s",'').replace("?","").replace("ā",'a').replace("ē",'e').replace('ī','i').replace('ō','o').replace('ū','u').replace('ë','e').replace('ō','o').split(" ")
for word in wordsmyth:
    if word and word[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and len(word)>3 and not word[1] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and not word.upper() in DCTENG: 
        WORDFREQMYTH.add(word.lower())
forbiddenwordshist = {'rome','war','jupiter','juno'}
forbiddenwordsmyth = {'rome','war'}
WORDFREQ-=forbiddenwordshist
WORDFREQMYTH-=forbiddenwordsmyth
WORDFREQLIT = set()
litQs = open(p+"Advanced/"+f"Advanced_Literature.txt",encoding='utf-8').read().splitlines()
wordslit = "".join(litQs[:len(litQs)//2]).replace(",","").replace(".","").replace("'s",'').replace("?","").replace("ā",'a').replace("ē",'e').replace('ī','i').replace('ō','o').replace('ū','u').replace('ë','e').replace('ō','o').split(" ")
for word in wordslit:
    if word and word[0] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and len(word)>3 and not word[1] in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ' and not word.upper() in DCTENG: 
        WORDFREQLIT.add(word.lower())

WORDFREQLITTEMP=set()
for itm in WORDFREQLIT:
    if itm in WORDFREQMYTH or itm in WORDFREQ:
        WORDFREQ-={itm}
        WORDFREQMYTH-={itm}
    else:
        WORDFREQLITTEMP.add(itm)
for itm in WORDFREQMYTH:
    if itm in WORDFREQ:
        WORDFREQ-={itm}

WORDFREQLIT=WORDFREQLITTEMP

historyterms1500 = ['consulship','politician','century','occupation','tarquinius superbus','ferentina','herdonius','jugurtha','marius','sulla','via aemilia','via popilia','via egnatia','via ignatia','via appia','via pompeia','via flaminia','via postumia','via domitia','romans call','axona','sambre','sabis','siligneus','castrensis','corona graminea','graminea','obsidionalis','tullianum','teuta','afranius burrus','burrus','bath','apodyterium','tepidarium','caldarium','frigidarium','governor','body of water','zeno','horologium','ctesiphon','cyzicus','caudine','aquaduct','aqua marcia','aqua tepula','aqua appia','aqua virgo','aqua augusta',' gens','litterator','fabius','rullianus','barbatus','grammaticus','alba longa','profession','augustus','octavian','tiberius','caligula','claudius','nero','galba','otho','vitellius','vespasian','titus','domitian','nerva','trajan','hadrian','antoninus pius','aurelius','verus','commodus','pertinax', 'was known to the romans',
            'didius','julianus','severus','caracalla','geta','macrinus','elagabalus','maximinus','gordian','pupienus','balbinus','philip','decius','valerian','gallienus','aurelian','probus','zenobia','carinus','numerian''festival','secession','plebs','plebeian','consul','aedile',
        'diocletian','maximian','constantius','constantine','maxentius','licinius','constans','valentinian','gratian','arcadius','stilicho','aetius','aëtius','valens','samnites','samnite','gauls','pompey','antony','cleopatra','mithridates','romulus','remus',' numa ','pompilius',
            'tullus hostilius','clodius','lucullus','ancus marcius','tarquin','servius tullius','paludamentum','sagum','lacerna','cucullus',' tyne','solway','suovetaurilia','suovetaurilia','cincinnatus','regillus','regulus','hannibal','ollus quiris','libitinarius', 'vestal','mola salsa']
historyterms500=['turnus','freedman','seneca','surgeon','general','chieftain','battle','circus','gladiator','chariot','arca','atrium','tablinum','tablinum','vestibulum','city','cities','curator annonae','praefectus annonae'
                 'tribune','praetor','scipio','emperor','roman life','libitinarius',' term ','marriage','wedding',' toga ','praetexta','colosseum','manius','gaius','marcus','funeral','clothing','type of slave','perficae','rostra','designator']
historyterms200= [' bc ','b.c.','lex','roman','white']

religionculture = ['colosseum',' mango','chirurgus','argentarius','designator','tonsor','pistor','amanuensis','topiarius','iudex','sutor','atriensis','carnifex','malum punicum','malum persicum','cerasus','glis','libitinarius','conclamatio','mystery cult','mystery religion','roman family','amita','matertera','scorpio','catapulta','statumen','carpentum','dorsum','viminal','capitoline','quirinal','janiculum','palatine','esquiline','caelian','fetiales','salii','rex sacrorum','parentalia','lupercalia','terminalia','regifugium','matronalia','liberalia','tubilustrium','hilaria','megalesia','cerealia','parilia','robigalia',
            'hibernia','britain','gaul','helvetia','defrutum','tyrotarichus','garum','epityrum','mulsum','fritillus','arbiter bibendi','paedagogus','pedisequi',
            'lemuria','bona dea','saturnalia','garumna','sequana','rhodanus','rhenus','danuvius','ister','cathedra','monopodium','sella curulis','mensa delphica','genius']
laws = ['plautia papiria','lex julia','lex iulia','canuleia','lex hortensia','licinia sextia','manilia','gabinia',' titia ','lex oppia','lex publilia','valeria horatia','ogulnia']
authors = ['ausonius',' catullus',' ovid','cn. naevius','cn naevius','gnaeus naevius','ennius','terence','vergil','cicero','seneca','pliny','lucan ','jerome','horace','andronicus','augustine',
              'pacuvius','reatinus','columella','italicus','accius','atax','atacinus','sallust','sisenna','lucretius','sappho','lesbia','persius','martial'
              ,'juvenal','suetonius','tacitus','petronius', ' cato','damasus','laberius','cinna','novius','nonius','josephus','quintus horatius flaccus',
              'varro','boethius','statius','symmachus','macrobius','livy','celsus','quintillian','apuleius','trebellius pollio','cordus','lampridius',
              'spartianus','syrus','claudian','ulpian','vitruvius','ammianus marcellinus','ausonius','didactic','astronomical']
litnothist = ['aulus gellius','varius rufus','plotius tucca','saturnian',' de ','pupil of','rhetorician','lawyer','jurist','elegist','elegy','what speech','dialogue','late latin','late author','de bello gallico','scipionic circle','maecenas','commentarii','livy','pliny','ammianus marcellinus','accius','macrobius',' conte ','archilochus','horace','pro rabirio']

works = {'aeneid', 'georgics', 'eclogues', 'copa', 'ciris', 'moretum', 'catalepton', 'aetna', 'dirae', 'gladiolus','ludius',
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
litTerms600= ['ulpian','labeo','patavenitas','bible','what meter','pimp','domitian']
litTerms200=['author']
litTerms500=['coined','work of','literature','latin literature','glaucoma','hariolus','triphallus','dolus','mastigophorous','pseudolus','aulularia','amphitruo','asinaria','bacchides','captivi','casina','cistellaria','curculio','epidicus','menaechmi','mercator','miles gloriosus','mostellaria','persa','poenulus','pseudolus','rudens','stichus','trinummus','truculentus','vidularia']
litTerms5000 = ['apologist','montanism','de lapsis','what work','plautine play','plautine comedy','142 books','142','what poemp','what epic','what meter','elegaic couplet','dactylic hexameter','sapphic strophe','attellan farce','translated the old testament','translate the old testament','who wrote','what author','what book','what play','what genre','fabula palliata','fabulae palliatae','fabulae praetextae','fabula praetexta','fabula cothurnata','cena trimalchionis','satyricon','apocolocyntosis',
                'what play of plautus','what play of terence','what play by plautus','zmyrna','mime ','mimes','riciniatae','planipedes','tragedian','comedian','playwright','satirist','elegist',
                'archilochus','lock of berenice','callimachus','menippean','sedigitus','periochae','clinamen','alimentus','palaemon']

mythTerms200 = ['princess']
mythTerms15000=['book i of the aeneid','book ii of the aeneid','book iii of the aeneid','book iv of the aeneid','book v of the aeneid',' book vi of the aeneid','book vii of the aeneid','book viii of the aeneid','book ix of the aeneid',' book x of the aeneid','book xi of the aeneid',' book xii of the aeneid'
                'book 1 of the aeneid','book 2 of the aeneid','book 3 of the aeneid','book 4 of the aeneid','book 5 of the aeneid','book 6 of the aeneid','book 7 of the aeneid','book 8 of the aeneid','book 9 of the aeneid','book 10 of the aeneid','book 11 of the aeneid','book 12 of the aeneid','marsyas','according to ovid','boat race','boxing contest','laodamia','protesilaus','sinon','funeral games of anchises','funeral games of achilles',
                'abaris','achelous','acis ','acmon','acoetes','actaeon','adonis','aeacus','aeetes','aegeus','aesacus','aglaulus','alcmene','alcyone','althaea','anaxarete','Andromeda','arachne','arcas','arethusa','argus','atalanta','athamas','athis','aurora','autolycus','bacchus','battus','baucis','bibles','cadmus','caeneus','calchas','calliope','callisto','cassandra','caunus','cecrops','cephalus','ceyx','chariclo','charybdis','chin','chiron','cinyras','clymene','corone','cyane','cygnus','cyllarus','cyparissus','daedalion','daedalus','daphne','deianira','deucalion','dryope','erysichthon','eurydice','eurytus','galanthis','galatea','Ganymede','glaucus','Hecuba','hermaphroditus','herse','Hesperia','hippodame','Hippolytus','hippomenes','hyacinthus','hylonome','Ianthe','icarus','idmon','inches',' ino ','iphigenia',' io ','iphis','ixion','laomedon','latona','latreus','lethaea','leucothea','lichas','macaques','meleager','memnon',' midas ',' minos','minotaur','morpheus','myrrha','myscelus','narcissus','nessus','niobe','nyctimene','ocyrhoe','orithyia','olenus','pegasus','gadfly','peleus','paellas','penthouse','perdix','phaedra','phaethon','philemon','philomela','phones','phocus','pirithous','polydectes','polydorus','polymestor','polyxena','pomona','procne','procris','pygmalion','pyramus','pyrenees','pyrrha','scylla','semele','silenus','syrinx','telamon','tereus','themis','thetis','thisbe','tiresias','tisiphone','triton','velrtumnus','virbius',
                'ajax','antilochus','calchas','diomedes','idomeneus','menelaus','nestor','odysseus','patroclus','teucer','agenor','andromache','antenor','cassandra','glaucus','sarpedon','neoptolemus','astyanax','helen','laodice','priam','lycaon','laothoe','zeleia','pandarus','polydamas','bellerophon','theano','rhesus','penthesilea','penelope','argos','laertes','anticlea','eurycleia','eumaeus','melantho','eurymachus','eurylochus','elpenor','perimedes','alcimus','amphialos','amphidamas','sinon','antilochus','polyphemus','antiphus','polites','amphinomus','antinous','eurymachus','leocritus','aethra','chryseis','chryses','chrysaor','clymene','diomede','hecamede','iphis','phylo',
                'chione','epaphus','coronis','ischys','cithaeronian','erymanthian','orphic','orpheus','eurydice','perseus','theseus','heracles','hippodamia','lapiths','eridanus','cycnus','epithet','colchis','jason','argonautica','hesiod','transform','danaids','nereids','hecatoncheires','odysseus','aeneas','ascanius','philomela',
                'achilles','briseis','agamemnon','menelaus','hector']
mythTerms1500 = ['funeral games','arrow','metamorphoses','mythological','mythology','atlantis','evenor','albula']
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
langTerms50000 = ['quot sunt','differentiate in meaning','differentiate in derivation','translate the word','ipod romana',' ipod ','translate this line','translate this sentence','translate these lines','translate:','from what latin word','translate the following','translate into latin','translate into english','idiom','what is the meaning','netflix','spotificia',"please listen","following passage","listen carefully","question that follows",'say in latin','quid anglice','welcome to the','cinema romana','bibliotecha romana','spotificio',
                  'for the verb','for the phrase','at the root','say in latin','nominative','ablative','genitive','dative','vocative','accusative','locative','imperative','subjunctive','infinitive','interjection',
                  'rhetorical device','literary device','qua latina','as prose','synonym','antonym','shares a meaning','shares its meaning','what case','is not derived','are not derived','is derived','are derived','derives','does not derive','meaning is shared',
                  '1st person','2nd person','3rd person','plural','singular','clama anglice','dic anglice','archaic form','syncopated form','syncopation','when recognized by the spotter','describamus','the following command','perform or describe','following latin sentence','conditional','comparative','superlative',' tense','classical latin']
langTerms10000 = ['abbreviation','abbreviated','the words','following words','motto','what phrase','latin phrase','verb','noun','adjective','adverb','pronoun','derived from','latin word for','blanks']

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
            litWeight+=10000
            histWeight-=10000
            langWeight-=10000
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
            litWeight+=4500
            #print(itm,"AHA")
            histWeight-=2000
            mythWeight-=2000
            langWeight-=1000
        if 'work of' in q and itm in q:
            litWeight+=600
            langWeight-=500
    for itm in works:
        if itm in q or itm in q:
            litWeight+=20000
    for itm in litTerms600:
        if " "+itm in q or "\n"+itm in q:
            litWeight+=1000
            langWeight-=8000
    for itm in litTerms500:
        if " "+itm in q or "\n"+itm in q:
            litWeight+=400
            langWeight-=500
    for i in range(150):
        if f"{i}-book" in q or f"{i} book" in q: litWeight+=500
    for itm in WORDFREQLIT:
        if " "+itm in q or "\n"+itm in q:
            langWeight+=200
            litWeight+=2000
            histWeight-=2000
            mythWeight-=2000
    
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
            langWeight-=4000
            mythWeight-=400
    for term in historyterms1500:
        if term in q:
            histWeight+=2500
            langWeight-=40000
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
            langWeight+=1000
            histWeight+=2000
            litWeight-=2000
            mythWeight-=2000

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
                langWeight-=10000
                mythWeight+=8000
                litWeight-=2000
                histWeight-=2000

    for itm in mythTerms15000:
        if itm in q:
            if not itm in WORDFREQLIT:
                mythWeight+=15000
                litWeight-=2000
                histWeight-=2000
                langWeight-=30000
    #Language
    if 'praenomen' in q:langWeight-=50000
    if 'andronicus' in q:langWeight-=5000
    if not "translated" in q and "translate" in q and ("english" in q or "latin" in q) and not 'andronicus' in q and not 'jerome' in q:  langWeight+=5000 #picks out translation questions
    elif 'translate' in q and not 'andronicus' in q and not 'jerome' in q:langWeight+=4000
    if "latin phrase" in q:
        langWeight+=500*q.count('latin phrase')
        if 'means' in q: langWeight+=5000
    if 'diminutive' in q:langWeight+=2000
    if "meaning" in q or 'means' in q:
        langWeight+=1000
        if 'differentiate' in q: langWeight+=10000
    if "at the root" in q: langWeight+=40000
    if "noun" in q or "verb" in q or "adjective" in q or "adverb" in q or "preposition" in q:langWeight+=5000

    if ("what use of" in q  or 'the use of' in q):langWeight+=50000
    if "in latin" in q:langWeight+=2000

    if "which of the following words" in q: langWeight+=5000
    if "derivative" in q or "derivation" in q:langWeight+=3000
    if "grammatical" in q: langWeight+=5000
    if "abbreviation" in q or 'abbreviated' in q: langWeight+=3000
    if  "motto" in q:langWeight+=3000
    if "latin word" in q:langWeight+=100
    if "legal term" in question:langWeight+=1000
    if 'quotes' in q:langWeight+=2000
    if 'is being described' in q or 'is described' in q:langWeight+=1000
    if 'of the words' in q:
        langWeight+=5000
        histWeight+=500
    if 'analogy' in q: langWeight+=1000
    if 'form of' in q: langWeight+=2000
    if 'latin form' in q:langWeight+=2000
    if ('due to' in q or 'because of' in q) and ('gender' in q or 'case' in q or 'tense' in q or 'grammar' in q or 'grammatical' in q):
        langWeight+=5000
    for term in langTerms50000:
        if term in q: 
            langWeight+=50000
    for term in langTerms10000:
        if term in q:
            langWeight+=10000
    
    category = ""
    if "Intermediate" in file or "Novice" in file:litWeight=-100000
    #Select category
    if langWeight>histWeight and langWeight>mythWeight and langWeight>litWeight:
        category="Language"
        counts['Lang:']=counts['Lang:']+1
    elif histWeight>langWeight and histWeight>mythWeight and histWeight>litWeight:
        category="History"
        counts['Hist:']=counts['Hist:']+1
    elif mythWeight>langWeight and mythWeight>histWeight and mythWeight>litWeight:
        category="Mythology"
        counts['Myth:']=counts['Myth:']+1
    elif litWeight>langWeight and litWeight>histWeight and litWeight>mythWeight:
        category="Literature"
        counts['Lit:']=counts['Lit:']+1
    else:category=("Ambiguous")
    if category=="Ambiguous":
        print(question,"Ambiguous")
    else:
        lvl = file.split("_")[0]+"/"
        lvl1 = lvl[:]
        if lvl[-3:]=="dE/" or lvl[-3:]=="eE/":
            lvl1=lvl[:-2]+"/"
        a={*open (p+lvl1+f"{lvl[:-1]}_{category}.txt",encoding='utf-8').read().splitlines()}
        with open (p+lvl1+f"{lvl[:-1]}_{category}.txt","a",encoding='utf-8') as output:
            if not question in a:output.write(question+"\n")
        #if category=="Mythology":print(question,category)
print(len(questions))
for itm in counts:
    print(itm,counts[itm])