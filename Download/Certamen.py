import sys; args = sys.argv[1:]
import math, re, time, random,os
from threading import Thread
import tkinter as tk
from tkinter import *
from tkinter import ttk
from Flashcards import flashCardWindow,reviewCardWindow
from Search_Questions import searchForQWindow

ROUNDNAMES=["Harvard","Yale","Princeton","VAFinals","Keartamen","VAKickoff","NJCL","Longhorn"]
LEVELS=["Novice","Intermediate","Advanced"]
CATEGORIES=["History","Literature","Language","Mythology"]
DCTYEARS={}

SELECTEDLEVELRDOPTION=[0] #Novice, Intermediate, or Advanced
HASSKIPPED=[False,0]
LASTSKIPP=[time.time()] #To ensure repeated skips don't come too often
RD2PLAY=[""]
ALLQUESTIONS=set()

p=(os.path.abspath("Certamen.py"))
print(p)

p=p[:-11]
if not "Download" in p: p+="Download/"
print(p)
rnds = os.listdir(p+"Rounds")
for rnd in rnds:
    if not "Language.txt" in rnd and not "History.txt" in rnd and not "Literature.txt" in rnd and not "Mythology.txt" in rnd:
        qs=open(p+"Rounds/"+rnd,encoding='utf-8').read()
        rnd=rnd.replace("_"," ")
        while "  " in qs:
            qs=qs.replace("  "," ")
        qs=qs.splitlines()
        newQs=[]
        for itm in qs:newQs+=itm.split("BONUS:")
        for itm in newQs:ALLQUESTIONS.add(itm+f" (from {rnd[:-11]})")

DCTENG={*open(p+"CSW19.txt",encoding='utf-8').read().splitlines()} #to make reading speed better
SORTING=[True] #If true allows sorting of questions into new categories
SHOWINGCATS=[False] #Controls whether the option buttens for sorting are visible

QUESTIONS=[] #Will be populated with questions from the selected round
QUESTION,ANSWER,BONUS1,BONUS1ANS,BONUS2,BONUS2ANS=[""],[""],[""],[""],[""],[""] #For reading the question
LASTEXTRACTED=[0] #For saving, reporting faulty, etc
CURPOINT=["Tossup"] #To progress through tossup bonus bonus sequence correctly
EXPANS=[0] #The expected answer to the current question
CURQ=[] #The current question
CURQLABEL=[] #The words from the current question that are currently being displayed as it is read
BUZZ=[False]
CURSCREEN=['Homescreen']
READSPEED=[1]
#Functions

def updateReadSpeed(*args):
    READSPEED[0]=1.0-readingSpeedSld.get()
    print(READSPEED[0])

def checkKeyBindings():
    while CURSCREEN[0]=="Answered":
        time.sleep(0.1)
        if root.focus_get()==factSaveFrame:
            root.unbind("<space>") #space
            root.unbind("<Return>") #Return
            root.unbind("n")
            root.unbind("f")
            root.unbind("s")
            root.bind("<Return>",saveFact) #Return
        elif root.focus_get()==ansEntry:
            root.unbind("<space>") #space
            root.unbind("<Return>") #Return
            root.unbind("n")
            root.unbind("f")
            root.unbind("s")
            root.bind("<Return>",displayAns) #Return



def saveToHist(*args):
    a={*open(p+'Rounds/Advanced_History.txt',encoding='utf-8').read().splitlines()} #to ensure duplicate questions don't end up here
    with open(p+"Rounds/Advanced_History.txt","a",encoding='utf-8') as output:
        q2write=LASTEXTRACTED[0]
        if not q2write[:-1] in a:
            output.write(q2write)
        else:print("Question already there...")
    saved.grid()
    root.unbind("h")
    root.unbind("l")
    root.unbind("i")
    root.unbind("m")
    SHOWINGCATS[0]=False
def saveToLit(*args):
    a={*open(p+'Rounds/Advanced_Literature.txt',encoding='utf-8').read().splitlines()}
    with open(p+"Rounds/Advanced_Literature.txt","a",encoding='utf-8') as output:
        q2write=LASTEXTRACTED[0]
        if not q2write[:-1] in a:
            output.write(q2write)
        else:print("Question already there...")
    saved.grid()
    root.unbind("h")
    root.unbind("l")
    root.unbind("i")
    root.unbind("m")
    SHOWINGCATS[0]=False
def saveToLang(*args):
    a={*open(p+'Rounds/Advanced_Language.txt',encoding='utf-8').read().splitlines()}
    with open(p+"Rounds/Advanced_Language.txt","a",encoding='utf-8') as output:
        q2write=LASTEXTRACTED[0]
        if not q2write[:-1] in a:
            output.write(q2write)
        else:print("Question already there...")
    saved.grid()
    root.unbind("h")
    root.unbind("l")
    root.unbind("i")
    root.unbind("m")
    SHOWINGCATS[0]=False
def saveToMyth(*args):
    a={*open(p+'Rounds/Advanced_Mythology.txt',encoding='utf-8').read().splitlines()}
    with open(p+"Rounds/Advanced_Mythology.txt","a",encoding='utf-8') as output:
        q2write=LASTEXTRACTED[0]
        if not q2write[:-1] in a:
            output.write(q2write)
        else:print("Question already there...")
    saved.grid()
    root.unbind("h")
    root.unbind("l")
    root.unbind("i")
    root.unbind("m")
    SHOWINGCATS[0]=False

def showCatsForSaving(*args):
    saveHistBtn.grid()
    savelitBtn.grid()
    savelangBtn.grid()
    saveMythBtn.grid()
    root.unbind("s")
    root.bind("h",saveToHist)
    root.bind("l",saveToLang)
    root.bind("i",saveToLit)
    root.bind("m",saveToMyth)
    SHOWINGCATS[0]=True


def questionScreen():
    questionFrame.grid()
    topFrm.grid()
    readNext.grid()
    q.configure(text="")
    returnHomeBtn.grid()
    readingSpeedFrm.grid()
    welcomeText.grid_remove()
    confirmFrm.grid_remove()
    root.bind("n",reset)
    root.bind("s",showCatsForSaving)
    CURSCREEN[0]='Reading'

def selectSaveFact(*args):
    factSave.focus()
    root.bind("<Return>",saveFact) #Return
    root.unbind("n")
    root.unbind("s")
    root.unbind("f")
    #temp=CardMaker(root)

def homeScreen(*args):
    RD2PLAY[0]=""
    while QUESTIONS:QUESTIONS.remove(QUESTIONS[0])
    welcomeText.grid()
    difficultyOptions.grid()
    playFavoritesBtn.grid()
    flashCardsFrame.grid()
    CURSCREEN[0]='Homescreen'
    for itm in questionReadingItms: itm.grid_remove()

def saveFact(*args):
    entry = factSavetxt.get()
    factSave.delete(0,'end')
    if entry:
        with open(p+"Fact.txt","a",encoding='utf-8') as output:
            output.write(entry+"\n")
    root.unbind("<>") #Return
    root.bind("s",showCatsForSaving)
    root.bind("n",reset)
    root.bind("f",selectSaveFact)
    mainframe.focus()
    
def favoriteQuestion(*args):
    a={*open(p+'Rounds/Favorites.txt',encoding='utf-8').read().splitlines()} #to ensure duplicate questions don't end up here
    with open(p+"Rounds/Favorites.txt","a",encoding='utf-8') as output:
        q2write=LASTEXTRACTED[0]
        if not q2write[:-1] in a:
            output.write(q2write)
        else:print("Question already there...")
def skipQuestion(*args):
    if time.time()-LASTSKIPP[0]>0.75:
        SHOWINGCATS[0]=False
        CURPOINT[0]="Tossup"
        HASSKIPPED[0]=True
        HASSKIPPED[1]=QUESTION[0]
        Thread(target=setHasSkipped).start()
        reset()
        LASTSKIPP[0]=time.time()

def setHasSkipped():
    time.sleep(0.5)
    HASSKIPPED[0]=False

def reset(*args):
    root.unbind("h")
    root.unbind("l")
    root.unbind("i")
    root.unbind("m")
    CURSCREEN[0]="Reading"
    ansFrame.grid_remove()
    ansRevFrame.grid_remove()
    saveQFrame.grid_remove()
    saveHistBtn.grid_remove()
    savelitBtn.grid_remove()
    savelangBtn.grid_remove()
    saveMythBtn.grid_remove()
    favoriteQuestionBtn.grid_remove()
    saved.grid_remove()
    factSaveFrame.grid_remove()
    saveFaultyFrame.grid_remove()
    root.unbind("n")
    root.unbind("f")
    root.unbind("s")
    root.bind("<space>",buzzFx) #space
    ansEntry.delete(0,'end')
    if QUESTIONS or CURPOINT[0]!="Tossup":
        while CURQ:CURQ.remove(CURQ[0])
        try:
            if CURPOINT[0]=="Tossup":
                q.config(text=" ".join(CURQ))
                qb1.config(text="\n"+" ".join(CURQ))
                qb2.config(text="\n"+" ".join(CURQ))
                b1Frame.grid_remove()
                b2Frame.grid_remove()
                saveFaultyConf.grid_remove()
                CURQLABEL[0]=q
                tp=QUESTIONS[0]
                QUESTIONS.remove(tp)
                forSaving=tp[0]+"BONUS:"+tp[1]
                if tp[2]:forSaving+="BONUS:"+tp[2]+"\n"
                else:forSaving+="\n"
                LASTEXTRACTED[0]=forSaving
                tu=tp[0].split("ANSWER:")
                b1=tp[1].split("ANSWER:")
                b2=[]
                if tp[2]:b2=tp[2].split("ANSWER:")
                
                QUESTION[0],ANSWER[0],BONUS1[0],BONUS1ANS[0]=tu[0].split(" "),tu[1],b1[0].split(" "),b1[1]
                if b2:BONUS2[0],BONUS2ANS[0]=b2[0].split(" "),b2[1]
                else:BONUS2[0],BONUS2ANS[0]="",""
            elif CURPOINT[0]=="B1":
                qb1.config(text="\n"+" ".join(CURQ))
                qb2.config(text="\n"+" ".join(CURQ))
                b1Frame.grid()
                CURQLABEL[0]=qb1
            elif CURPOINT[0]=="B2" and BONUS2[0]:
                CURQLABEL[0]=qb2
                b2Frame.grid()
                qb2.config(text="\n"+" ".join(CURQ))
            saved.grid_remove()

            readNext.config(text="Buzz",command=buzzFx)
            mainframe.focus()
            curThread=Thread(target=readQuestion)
            curThread.start()
        except:
            displayRoundFinished()
    else:
        displayRoundFinished()

def displayAns(*args):
    if SHOWINGCATS[0]:
        root.bind("h",saveToHist)
        root.bind("l",saveToLang)
        root.bind("i",saveToLit)
        root.bind("m",saveToMyth)
    mainframe.focus()
    root.unbind("<Return>") #Return
    ansSubmission.config(command=doNothing)
    ansGiven=ans.get()
    gvAns.config(text=f"You gave: {ansGiven}")
    CURQLABEL[0].config(text="\n"+" ".join(QUESTION[0]))
    ansRevFrame.grid()
    saveFaultyFrame.grid()
    favoriteQuestionBtn.grid()

    if CURPOINT[0]=="Tossup":
        if BONUS1[0]:
            q.config(text=" ".join(QUESTION[0])+"\nANS: "+ANSWER[0])
            QUESTION[0]=BONUS1[0]
            ANSWER[0]=BONUS1ANS[0]
            CURPOINT[0]="B1"
    elif CURPOINT[0]=="B1":
        if BONUS2[0]:
            qb1.config(text=" ".join(QUESTION[0])+"\nANS: "+ANSWER[0])
            QUESTION[0]=BONUS2[0]
            ANSWER[0]=BONUS2ANS[0]
            CURPOINT[0]="B2"
        else:
            qb1.config(text=" ".join(QUESTION[0])+"\nANS: "+ANSWER[0])
            CURPOINT[0]="Tossup"
    else:
        qb2.config(text=" ".join(QUESTION[0])+"\nANS: "+ANSWER[0])
        CURPOINT[0]="Tossup"
    #factSaveFrame.grid()
    qb="Bonus"if not CURPOINT[0]=="Tossup" else "Question"
    readNext.config(text=f"Read Next {qb}",command=reset)
    if SORTING[0]:
        saveQFrame.grid()
        root.bind("s",showCatsForSaving)
    root.bind("n",reset)
    #root.bind("f",selectSaveFact)

def displayRoundFinished():
    for itm in questionReadingItms:itm.grid_remove()
    roundFinishedLabel.grid()
    returnHomeBtn.grid()

def buzzFx(*args):
    root.unbind("<space>") #space
    CURSCREEN[0]=="Answered"
    bindingThread=Thread(target=checkKeyBindings)
    bindingThread.start()
    BUZZ[0]=True

def doNothing():
    return

def readQuestion():
    root.bind("s",skipQuestion)
    while CURQ:CURQ.remove(CURQ[0])
    wordind=0
    BUZZ[0]=False
    toRead=QUESTION[0]
    while wordind<len(QUESTION[0]) and not BUZZ[0]:
        if HASSKIPPED[0] and HASSKIPPED[1]==toRead:
            print("Skipped!")
            return
        CURQ.append(QUESTION[0][wordind])
        CURQLABEL[0].config(text="\n"+" ".join(CURQ))
        tSleep=.04 if QUESTION[0][wordind].split("'")[0].lower() in DCTENG else .06
        if "," in QUESTION[0][wordind]:tSleep+=.02
        time.sleep(tSleep*len(QUESTION[0][wordind])*READSPEED[0])
        wordind+=1
    tmer=time.time()
    while time.time()-tmer<7.5 and not BUZZ[0]:
        if HASSKIPPED[0] and HASSKIPPED[1]==toRead:return
        continue
    if wordind<len(QUESTION[0]):    
        QUESTION[0][wordind-1]+="*"
    else:QUESTION[0][-1]+="*"
    root.unbind("s")
    ansSubmission.config(command=displayAns)
    ansEntry.focus()
    root.bind("<Return>",displayAns) #Return
    ansFrame.grid()

def playFavorites(*args):
    RD2PLAY[0]="Favorites.txt"
    for itm in homeScreenItms:itm.grid_remove()
    loadSelectedFile()
def setRoundName(n):
    playFavoritesBtn.grid_remove()
    if not "Parsed" in RD2PLAY[0]:
        if RD2PLAY[0]=="" and n in LEVELS:
            RD2PLAY[0]+=n
            RD2PLAY[0]+="_"
            if not n=="Advanced":
                if n=="Novice": 
                    roundOptionsNovice.grid()
                    SELECTEDLEVELRDOPTION[0]=roundOptionsNovice
                else:
                    roundOptionsIntermediate.grid()
                    SELECTEDLEVELRDOPTION[0]=roundOptionsNovice
            else:

                roundOptionsAdvanced.grid()
                SELECTEDLEVELRDOPTION[0]=roundOptionsAdvanced
            difficultyOptions.grid_remove()
        elif n in ROUNDNAMES:
            RD2PLAY[0]+=n
            RD2PLAY[0]+="_"
            SELECTEDLEVELRDOPTION[0].grid_remove()
            for yr in DCTYEARS[RD2PLAY[0]]:yr.grid()
            selectYear.grid()
        elif n in CATEGORIES:
            RD2PLAY[0]+=n
            SELECTEDLEVELRDOPTION[0].grid_remove()
            txtConfirmLbl=RD2PLAY[0].replace("_"," ")
            confirmLbl.config(text=f"You have selected {txtConfirmLbl}; Play?")
            confirmLbl.config(font=("Courier",15))
            RD2PLAY[0]+=".txt"
            confirmFrm.grid()
        else: #Selects the year and prepares to load round
            for yr in DCTYEARS[RD2PLAY[0]]:yr.grid_remove()
            RD2PLAY[0]+=n
            txtConfirmLbl=RD2PLAY[0].replace("_"," ")
            confirmLbl.config(text=f"You have selected {txtConfirmLbl}; Play?")
            confirmLbl.config(font=("Courier",15))
            RD2PLAY[0]+="_Parsed.txt"
            selectYear.grid_remove()
            confirmFrm.grid()
def back2Difficulty():
    roundOptionsAdvanced.grid_remove()
    roundOptionsIntermediate.grid_remove()
    roundOptionsNovice.grid_remove()
    difficultyOptions.grid()
    RD2PLAY[0]=""
def back2School():
    selectYear.grid_remove()
    SELECTEDLEVELRDOPTION[0].grid()
    RD2PLAY[0]=RD2PLAY[0].split("_")[0]+"_"
def back2Year():
    confirmFrm.grid_remove()
    if "History" or "Literature" or "Language" or "Mythology" in RD2PLAY[0]:
        SELECTEDLEVELRDOPTION[0].grid()
        RD2PLAY[0]=RD2PLAY[0].split("_")[0]+"_"
    else:
        selectYear.grid()
        RD2PLAY[0]="_".join(RD2PLAY[0].split("_")[:2])+"_"
        for yr in DCTYEARS[RD2PLAY[0]]:yr.grid()
def loadSelectedFile():
    CURPOINT[0]="Tossup"
    print(RD2PLAY[0])
    qs=open(p+"Rounds/"+RD2PLAY[0],encoding='utf-8').read()
    while "  " in qs:
        qs=qs.replace("  "," ")
    qs=qs.splitlines()
    if "History" in RD2PLAY[0] or "Literature" in RD2PLAY[0] or "Language" in RD2PLAY[0] or "Mythology" in RD2PLAY[0]:
        SORTING[0]=False
    if SORTING[0]:
        seen={*open(p+'Rounds/Faulty_Questions.txt',encoding='utf-8').read().splitlines()}|{*open(p+'Rounds/Advanced_History.txt',encoding='utf-8').read().splitlines()}|{*open(p+'Rounds/Advanced_Language.txt',encoding='utf-8').read().splitlines()}|{*open(p+'Rounds/Advanced_Literature.txt',encoding='utf-8').read().splitlines()}|{*open(p+'Rounds/Advanced_Mythology.txt',encoding='utf-8').read().splitlines()}
    else:
        seen={*open(p+'Rounds/Faulty_Questions.txt',encoding='utf-8').read().splitlines()}
    qs={*qs}
    toRemove=set()
    for question in qs:
        if f"{RD2PLAY[0]} {question}" in seen:
            toRemove.add(question)
    qs-=(seen|toRemove)
    qs=[*qs]
    while QUESTIONS:QUESTIONS.remove(QUESTIONS[0])
    itms=[]
    for ind in range(len(qs)):
        temp=qs[ind].split("BONUS:")
        if len(temp)>2:itm=(temp[0],temp[1],temp[2])
        else:itm=(temp[0],temp[1],"")
        itms.append(itm)
    for itm in itms:
        QUESTIONS.append(itm)
    random.shuffle(QUESTIONS)
    print(len(QUESTIONS))
    questionScreen()

def recordFaultyQuestion():
    a={*open(p+'Rounds/Faulty_Questions.txt',encoding='utf-8').read().splitlines()}
    with open(p+"Rounds/Faulty_Questions.txt","a",encoding='utf-8') as output:
        toW=f"{RD2PLAY[0]} {LASTEXTRACTED[0]}"
        if not toW[:-1] in a:
            output.write(toW)
    saveFaultyConf.grid()



#The display
root=Tk()
root.title("Certamen Reader")
root.minsize(1050,800)

mainframe = ttk.Frame(root,padding="3 3 12 12",width=1000,height=750)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

#Question Reading
questionFrame=ttk.Frame(mainframe)
topFrm=ttk.Frame(questionFrame)
readNext=ttk.Button(topFrm, text="Read Question", command=reset)
readNext.grid(column=0, row=0, sticky=W)
skipQuestionBtn=ttk.Button(topFrm,text="Skip Question",command=skipQuestion)
skipQuestionBtn.grid(column=1,row=0,sticky=W)
topFrm.grid(row=0,column=0,sticky=W)
q=ttk.Label(questionFrame,text=CURQ,wraplength=990)
q.grid(row=1,column=0,sticky=(EW))
q.config(font=("Courier",16))
questionFrame.grid(row=0,column=0,sticky=W)
questionFrame.grid_remove()

b1Frame=ttk.Frame(mainframe)
qb1=ttk.Label(b1Frame,text="\n",wraplength=990)
qb1.grid(row=0,column=0,sticky=(EW))
qb1.config(font=("Courier",16))
b1Frame.grid(row=1,column=0,sticky=W)
b1Frame.grid_remove()

b2Frame=ttk.Frame(mainframe)
qb2=ttk.Label(b2Frame,text="\n",wraplength=950)
qb2.grid(row=0,column=0,sticky=(EW))
qb2.config(font=("Courier",16))
b2Frame.grid(row=2,column=0,sticky=W)
b2Frame.grid_remove()

CURQLABEL.append(q)

#Answering
ansFrame=ttk.Frame(mainframe)
ansPrompt=ttk.Label(ansFrame,text="Enter answer below:")
ans=StringVar()
ansEntry=ttk.Entry(ansFrame,width=100,textvariable=ans)
ansPrompt.grid(row=0,column=0,sticky=(EW))
ansEntry.grid(row=1,column=0,sticky=(EW))
ansSubmission=ttk.Button(ansFrame,text="Submit Answer",command=doNothing)
ansSubmission.grid(row=1,column=0,sticky=(E))
ansFrame.grid(row=3,column=0,sticky=W)
ansFrame.grid_remove()

#Revealing Answer
ansRevFrame=ttk.Frame(mainframe)
gvAns=ttk.Label(ansRevFrame,text="")
gvAns.grid(row=0,column=0,sticky=(EW))
ansRevFrame.grid(row=4,column=0,sticky=W)
ansRevFrame.grid_remove()

#Saving Facts
factSaveFrame=ttk.Frame(mainframe)
factSavetxt=StringVar()
factSave=ttk.Entry(factSaveFrame,width=100,textvariable=factSavetxt)
factSave.grid(column=0,row=0,sticky=W)
factSaveBtn=ttk.Button(factSaveFrame,text="Save Fact",command=saveFact)
factSaveBtn.grid(column=1,row=0,sticky=W)
factSaveFrame.grid(row=17,column=0,sticky=W)
factSaveFrame.grid_remove()

#Saving questions to categories
saveQFrame=ttk.Frame(mainframe)
saveQBtn=ttk.Button(saveQFrame,text="Save to a category?",command=showCatsForSaving)
saveQBtn.grid(column=0,row=1,sticky=W)
saveHistBtn=ttk.Button(saveQFrame,text="History <h>",command=saveToHist)
saveHistBtn.grid(column=0,row=2,sticky=W)
savelitBtn=ttk.Button(saveQFrame,text="Literature <i>",command=saveToLit)
savelitBtn.grid(column=0,row=3,sticky=W)
savelangBtn=ttk.Button(saveQFrame,text="Language <l>",command=saveToLang)
savelangBtn.grid(column=0,row=4,sticky=W)
saveMythBtn=ttk.Button(saveQFrame,text="Myth <m>",command=saveToMyth)
saveMythBtn.grid(column=0,row=5,sticky=W)
saved=ttk.Label(saveQFrame,text="Saved!")
saved.grid(column=0,row=6,sticky=W)
saveHistBtn.grid_remove()
savelitBtn.grid_remove()
savelangBtn.grid_remove()
saveMythBtn.grid_remove()
saved.grid_remove()
saveQFrame.grid(column=0,row=5,sticky=W)
saveQFrame.grid_remove()

saveFaultyFrame=ttk.Frame(mainframe)
saveFaultyBtn=ttk.Button(saveFaultyFrame,text="Report Faulty Question",command=recordFaultyQuestion)
saveFaultyBtn.grid(row=0,column=0,sticky=W)
saveFaultyConf=ttk.Label(saveFaultyFrame,text="Reported")
saveFaultyConf.grid(row=0,column=1,sticky=W)
saveFaultyConf.grid_remove()
saveFaultyFrame.grid(row=18,column=0,sticky=W)

roundFinishedLabel=ttk.Label(mainframe,wraplength=990,text="You have read all available questions; return home to choose another round/category")
roundFinishedLabel.config(font=("Courier",20))
roundFinishedLabel.grid(column=0,row=18,sticky=W)
roundFinishedLabel.grid_remove()

questionReadingItms=[questionFrame,ansRevFrame,ansFrame,factSaveFrame,saveQFrame,b1Frame,b2Frame,saveFaultyFrame,roundFinishedLabel,topFrm]

favoriteQuestionBtn = ttk.Button(mainframe,text="Save Question as Favorite",command=favoriteQuestion)
favoriteQuestionBtn.grid(row=19,column=0,sticky=SW)
questionReadingItms.append(favoriteQuestionBtn)

readingSpeedFrm = ttk.Frame(mainframe)
var=DoubleVar()
readingSpeedLbl = ttk.Label(readingSpeedFrm,text="Reading Speed")
readingSpeedLbl.grid(column=0,row=0,sticky=SW)
readingSpeedSld = ttk.Scale(readingSpeedFrm,from_=-0.8,to_=0.8,command=updateReadSpeed, variable=var)
readingSpeedSld.set(0.0)
readingSpeedSld.grid(column=1,row=0,sticky=W)
questionReadingItms.append(readingSpeedFrm)
readingSpeedFrm.grid(row=20,column=0,sticky=SW)

returnHomeBtn=ttk.Button(mainframe,text="Return Home",command=homeScreen)
returnHomeBtn.grid(column=0,row=21,sticky=SW)
questionReadingItms.append(returnHomeBtn)

#########################################################################################################################
#########################################################################################################################
#########################################################################################################################
#########################################################################################################################
#Create the homescreen: 
welcomeText=ttk.Label(mainframe,text="Welcome! Please choose a round or category to play")
welcomeText.grid(column=0,row=0,sticky=EW)
welcomeText.grid_remove()
welcomeText.config(font=("Courier",20))


#Select the difficulty
difficultyOptions=ttk.Frame(mainframe)
difficultyLabel=ttk.Label(difficultyOptions,text="\nChoose a level:\n")
difficultyLabel.config(font=("Courier",15))
difficulties=[ttk.Button(difficultyOptions,text="Novice",command=lambda:setRoundName("Novice")),
              ttk.Button(difficultyOptions,text="Intermediate",command=lambda:setRoundName("Intermediate")),
              ttk.Button(difficultyOptions,text="Advanced - Hard",command=lambda:setRoundName("Advanced")),
              ttk.Button(difficultyOptions,text="Advanced - Easy",command=lambda:setRoundName("AdvancedE"))
            ]
difficultyLabel.grid(column=0,columnspan=len(difficulties),row=0,sticky=W)
for i in range(len(difficulties)):
    difficulties[i].grid(column=i,row=1,sticky=W)    
difficultyOptions.grid(row=1,column=0,sticky=W)
difficultyOptions.grid_remove()

playFavoritesBtn =ttk.Button(mainframe,text="Play Favorite Questions",command=playFavorites)
playFavoritesBtn.grid(row=2,column=0,sticky=SW)
playFavoritesBtn.grid_remove()

flashCardsFrame=ttk.Frame(mainframe)
ttk.Label(flashCardsFrame,text="\n\n").grid(row=0,column=0,sticky=W)
flashCardsLabel=ttk.Label(flashCardsFrame,text="Or do flashcards:",font=("Courier",15))
flashCardsLabel.grid(row=1,column=0,sticky=W)
makeFlashCards=ttk.Button(flashCardsFrame,text="Create Flashcards", command=lambda:flashCardWindow(root))
makeFlashCards.grid(row=1,column=1,sticky=W)
reviewFlashCards=ttk.Button(flashCardsFrame,text="Review Flashcards", command=lambda:reviewCardWindow(root))
reviewFlashCards.grid(row=1,column=2,sticky=W)
flashCardsFrame.grid(row=10,column=0,sticky=W)
flashCardsFrame.grid_remove()

homeScreenItms = [difficultyOptions,playFavoritesBtn]
ttk.Button(mainframe,text="Search Question Bank",command=lambda:searchForQWindow(root,ALLQUESTIONS)).grid(row=11,column=0,sticky=W)

#Select the School
roundOptionsAdvanced=ttk.Frame(mainframe)
backButton=ttk.Button(roundOptionsAdvanced,text="Back",command=back2Difficulty)
backButton.grid(column=0,row=2,sticky=W)
schoolLbl=ttk.Label(roundOptionsAdvanced,text="\nChoose a school:\n")
schoolLbl.config(font=("Courier",15))
rounds=[ttk.Button(roundOptionsAdvanced,text="Harvard",command=lambda:setRoundName("Harvard")),
        ttk.Button(roundOptionsAdvanced,text="Yale",command=lambda:setRoundName("Yale")),
        ttk.Button(roundOptionsAdvanced,text="Princeton",command=lambda:setRoundName("Princeton")),
        ttk.Button(roundOptionsAdvanced,text="VA State Finals",command=lambda:setRoundName("VAFinals")),
        #ttk.Button(roundOptionsAdvanced,text="VA Kickoff",command=lambda:setRoundName("VAKickoff")),
        ttk.Button(roundOptionsAdvanced,text="Keartamen",command=lambda:setRoundName("Keartamen")),
        ttk.Button(roundOptionsAdvanced,text="NJCL Nats",command=lambda:setRoundName("NJCL")),
        ttk.Button(roundOptionsAdvanced,text="Longhorn",command=lambda:setRoundName("Longhorn"))]
for i in range(len(rounds)):
    rounds[i].grid(column=i,row=1,sticky=W)
schoolLbl.grid(column=0,columnspan=len(rounds),row=0,sticky=W)
categoryLbl=ttk.Label(roundOptionsAdvanced,text="\nOr, choose a category:\n")
categoryLbl.config(font=("Courier",15))
cats=[ttk.Button(roundOptionsAdvanced,text="History",command=lambda:setRoundName("History")),
      ttk.Button(roundOptionsAdvanced,text="Language",command=lambda:setRoundName("Language")),
      ttk.Button(roundOptionsAdvanced,text="Mythology",command=lambda:setRoundName("Mythology")),
      ttk.Button(roundOptionsAdvanced,text="Literature",command=lambda:setRoundName("Literature"))]
for i in range(len(cats)):
    cats[i].grid(column=i,row=3,sticky=W)
categoryLbl.grid(column=0,row=2,columnspan=len(cats),sticky=W)
roundOptionsAdvanced.grid(row=1,column=0,sticky=W)
roundOptionsAdvanced.grid_remove()



roundOptionsIntermediate=ttk.Frame(mainframe)
backButton1=ttk.Button(roundOptionsIntermediate,text="Back",command=back2Difficulty)
backButton1.grid(column=0,row=2,sticky=W)
schoolLblIntermediate=ttk.Label(roundOptionsIntermediate,text="Unfortunately, no rounds are available at this time")#"\nChoose a school:\n")
schoolLblIntermediate.config(font=("Courier",15))
intermediateRounds=[]#ttk.Button(roundOptionsIntermediate,text="Harvard",command=lambda:setRoundName("Harvard"))]
for i in range(len(intermediateRounds)):
    intermediateRounds[i].grid(column=i,row=1,sticky=W)
colspan=len(intermediateRounds) if intermediateRounds else 1
schoolLblIntermediate.grid(column=0,columnspan=colspan,row=0,sticky=W)
roundOptionsIntermediate.grid(row=1,column=0,sticky=W)
roundOptionsIntermediate.grid_remove()

roundOptionsNovice=ttk.Frame(mainframe)
backButton2=ttk.Button(roundOptionsNovice,text="Back",command=back2Difficulty)
backButton2.grid(column=0,row=2,sticky=W)
schoolLblNovice=ttk.Label(roundOptionsNovice,text="Unfortunately, no rounds are available at this time")#"\nChoose a school:\n")
schoolLblNovice.config(font=("Courier",15))
noviceRounds=[]#ttk.Button(roundOptionsNovice,text="Harvard",command=lambda:setRoundName("Harvard"))]
for i in range(len(noviceRounds)):
    noviceRounds[i].grid(column=i,row=1,sticky=W)
colspan=len(noviceRounds) if noviceRounds else 1
schoolLblNovice.grid(column=0,columnspan=colspan,row=0,sticky=W)
roundOptionsNovice.grid(row=1,column=0,sticky=W)
roundOptionsNovice.grid_remove()


#Select the year
selectYear=ttk.Frame(mainframe)
backButton3=ttk.Button(selectYear,text="Back",command=back2School)
backButton3.grid(row=2,column=0,sticky=W)
harvardYearsAdvanced=[ttk.Button(selectYear,text="2025",command=lambda:setRoundName("2025")),
                    ttk.Button(selectYear,text="2024",command=lambda:setRoundName("2024")),
                    ttk.Button(selectYear,text="2023",command=lambda:setRoundName("2023")),
                    ttk.Button(selectYear,text="2022",command=lambda:setRoundName("2022")),
                    ttk.Button(selectYear,text="2021",command=lambda:setRoundName("2021")),
                    ttk.Button(selectYear,text="2019",command=lambda:setRoundName("2019")),
                    ttk.Button(selectYear,text="2018",command=lambda:setRoundName("2018")),
                    ttk.Button(selectYear,text="2017",command=lambda:setRoundName("2017")),
                    ttk.Button(selectYear,text="2015",command=lambda:setRoundName("2015")),
                    ttk.Button(selectYear,text="2014",command=lambda:setRoundName("2014")),
                    ttk.Button(selectYear,text="2013",command=lambda:setRoundName("2013")),
                    ttk.Button(selectYear,text="2012",command=lambda:setRoundName("2012"))]
                    #ttk.Button(selectYear,text="2010",command=lambda:setRoundName("2010"))]
yaleYearsAdvanced=  [ttk.Button(selectYear,text="2024",command=lambda:setRoundName("2024")),
                    ttk.Button(selectYear,text="2023",command=lambda:setRoundName("2023")),
                    ttk.Button(selectYear,text="2022",command=lambda:setRoundName("2022")),
                    ttk.Button(selectYear,text="2021",command=lambda:setRoundName("2021")),
                    ttk.Button(selectYear,text="2020",command=lambda:setRoundName("2020")),
                    ttk.Button(selectYear,text="2019",command=lambda:setRoundName("2019")),
                    ttk.Button(selectYear,text="2018",command=lambda:setRoundName("2018")),
                    ttk.Button(selectYear,text="2017",command=lambda:setRoundName("2017")),
                    ttk.Button(selectYear,text="2016",command=lambda:setRoundName("2016")),
                    ttk.Button(selectYear,text="2015",command=lambda:setRoundName("2015")),
                    ttk.Button(selectYear,text="2014",command=lambda:setRoundName("2014")),
                    ttk.Button(selectYear,text="2013",command=lambda:setRoundName("2013")),
                    ttk.Button(selectYear,text="2012",command=lambda:setRoundName("2012")),]
princetonYearsAdvanced=[ttk.Button(selectYear,text="2025",command=lambda:setRoundName("2025")),
                        ttk.Button(selectYear,text="2022",command=lambda:setRoundName("2022")),
                        ttk.Button(selectYear,text="2021",command=lambda:setRoundName("2021")),
                        ttk.Button(selectYear,text="2020",command=lambda:setRoundName("2020"))]
vaFinalsYearsAdvanced=[ttk.Button(selectYear,text="2023",command=lambda:setRoundName("2023")),
                       ttk.Button(selectYear,text="2022",command=lambda:setRoundName("2022")),
                       ttk.Button(selectYear,text="2021",command=lambda:setRoundName("2021")),
                       ttk.Button(selectYear,text="2019",command=lambda:setRoundName("2019")),
                       ttk.Button(selectYear,text="2018",command=lambda:setRoundName("2018")),
                       ttk.Button(selectYear,text="2017",command=lambda:setRoundName("2017")),
                       ttk.Button(selectYear,text="2017_Lvl3",command=lambda:setRoundName("2017_Lvl3"))]
                       #ttk.Button(selectYear,text="2016",command=lambda:setRoundName("2016"))]
vaKickoffYearsAdvanced=[ttk.Button(selectYear,text="2023",command=lambda:setRoundName("2023"))]
keartamenYearsAdvanced=[ttk.Button(selectYear,text="2024",command=lambda:setRoundName("2024")),
                        ttk.Button(selectYear,text="2023",command=lambda:setRoundName("2023")),
                        ttk.Button(selectYear,text="2022",command=lambda:setRoundName("2022")),
                        ttk.Button(selectYear,text="2021",command=lambda:setRoundName("2021")),
                        ttk.Button(selectYear,text="2020",command=lambda:setRoundName("2020")),]
NJCLYearsAdvanced=[ttk.Button(selectYear,text="2024",command=lambda:setRoundName("2024")),
                    ttk.Button(selectYear,text="2023",command=lambda:setRoundName("2023")),
                    ttk.Button(selectYear,text="2022",command=lambda:setRoundName("2022")),
                    ttk.Button(selectYear,text="2021",command=lambda:setRoundName("2021")),
                    ttk.Button(selectYear,text="2020",command=lambda:setRoundName("2020")),
                    ttk.Button(selectYear,text="2019",command=lambda:setRoundName("2019"))]
longhornYearsAdvanced=[ttk.Button(selectYear,text="2024",command=lambda:setRoundName("2024")),
                       ttk.Button(selectYear,text="2022",command=lambda:setRoundName("2022")),
                       ttk.Button(selectYear,text="2021",command=lambda:setRoundName("2021"))]


DCTYEARS["Advanced_Yale_"]=yaleYearsAdvanced
DCTYEARS["Advanced_Princeton_"]=princetonYearsAdvanced
DCTYEARS["Advanced_Harvard_"]=harvardYearsAdvanced
DCTYEARS["Advanced_VAFinals_"]=vaFinalsYearsAdvanced
DCTYEARS['Advanced_VAKickoff_']=vaKickoffYearsAdvanced
DCTYEARS["Advanced_Keartamen_"]=keartamenYearsAdvanced
DCTYEARS["Advanced_NJCL_"]=NJCLYearsAdvanced
DCTYEARS["Advanced_Longhorn_"]=longhornYearsAdvanced

for i in range(len(harvardYearsAdvanced),0,-1):
    harvardYearsAdvanced[i-1].grid(column=i-1,row=1,sticky=W)
    harvardYearsAdvanced[i-1].grid_remove()
for i in range(len(yaleYearsAdvanced)):
    yaleYearsAdvanced[i].grid(column=i,row=1,sticky=W)
    yaleYearsAdvanced[i].grid_remove()
for i in range(len(princetonYearsAdvanced)):
    princetonYearsAdvanced[i].grid(column=i,row=1,sticky=W)
    princetonYearsAdvanced[i].grid_remove()
for i in range(len(vaFinalsYearsAdvanced)):
    vaFinalsYearsAdvanced[i].grid(column=i,row=1,sticky=W)
    vaFinalsYearsAdvanced[i].grid_remove()
for i in range(len(vaKickoffYearsAdvanced)):
    vaKickoffYearsAdvanced[i].grid(column=i,row=1,sticky=W)
    vaKickoffYearsAdvanced[i].grid_remove()
for i in range(len(keartamenYearsAdvanced)):
    keartamenYearsAdvanced[i].grid(column=i,row=1,sticky=W)
    keartamenYearsAdvanced[i].grid_remove()
for i in range(len(NJCLYearsAdvanced)):
    NJCLYearsAdvanced[i].grid(column=i,row=1,sticky=W)
    NJCLYearsAdvanced[i].grid_remove()
for i in range(len(longhornYearsAdvanced)):
    longhornYearsAdvanced[i].grid(column=i,row=1,sticky=W)
    longhornYearsAdvanced[i].grid_remove()
yrLbl=ttk.Label(selectYear,text="\nChoose a year:\n")
yrLbl.grid(row=0,column=0,columnspan=len(harvardYearsAdvanced),sticky=W)
yrLbl.config(font=("Courier",15))

#Confirm selection
confirmFrm=ttk.Frame(mainframe)
backButton4=ttk.Button(confirmFrm,text="Back",command=back2Year)
backButton4.grid(row=0,column=2,sticky=W)
confirmLbl=ttk.Label(confirmFrm,text=f"You have selected ; Play?")
confirmLbl.grid(row=0,column=0,sticky=W)
confirmBtn=ttk.Button(confirmFrm,text="Play", command=loadSelectedFile)
confirmBtn.grid(row=0,column=1,sticky=W)
confirmFrm.grid(row=1,column=0,sticky=W)
confirmFrm.grid_remove()

selectYear.grid(row=2,column=0,sticky=W)
selectYear.grid_remove()

if __name__=="__main__":
    mainframe.focus()
    homeScreen()
    root.mainloop()