import sys; args=sys.argv[1:]
import math, re, time, random, pathlib
from threading import Thread
import tkinter as tk
import os
from tkinter import *
from tkinter import ttk
import datetime

TYPEOPTIONS=["Basic One-Sided","Basic Two-Sided"]
CURDECKOPTIONSVAR=[]
CURCARD=["temp"]
NEWEVAL=["temp"]
CARDS=[]
GONEXT=[False]
LBLS=[]

path=(os.path.abspath("Flashcards.py"))
path=path[:-13]
if not "Reading Files" in path: 
    p=pathlib.Path(path) / "Reading Files"
else:
    p=pathlib.Path(path)

def getDecks():
    a= os.listdir(str(p/"Flashcard Decks"))
    for i,itm in enumerate(a):
        a[i]=itm[:-4]
    return a
DECKOPTIONS=sorted(getDecks()) if getDecks() else ["Default"]

def makeCard(frontText,backText,selectedDeck,frontEntry,backEntry,errorLabel,cardType):
    deck,front,back=selectedDeck.get(),frontEntry.get(),backEntry.get()
    if front and back:
        errorLabel.grid_remove()
        frontText.delete(0,'end')
        backText.delete(0,'end')
        with open(str(p/"Flashcard Decks"/f"{deck}.txt"),"a") as output:
            date=datetime.datetime.now()
            string=front.replace("\n"," ")+"**REVERSE**"+back.replace("\n"," ")+"**LASTREVIEW**"+f"{date.year}-{date.month}-{date.day}-{date.hour}-{date.minute}"+"**LEARNINGSTAGE**0"+"\n"
            output.write(string)
            if cardType=="Basic Two-Sided":
                string2=back.replace("\n"," ")+"**REVERSE**"+front.replace("\n"," ")+"**LASTREVIEW**"+f"{date.year}-{date.month}-{date.day}-{date.hour}-{date.minute}"+"**LEARNINGSTAGE**0"+"\n"
                output.write(string2)
            print("Success!!")
        frontText.focus()
    else: errorLabel.grid()

def createDeck(deck,entryToClear,mfcMenu,selectedDeck):
    if deck and not deck in getDecks():
        with open(str(p/"Flashcard Decks"/f"{deck}.txt"),"a") as output:
            entryToClear.delete(0,'end')
        print("Created!")
        DECKOPTIONS=sorted(getDecks())
        newDeckOptions=ttk.OptionMenu(mfcMenu, selectedDeck,DECKOPTIONS[0],*DECKOPTIONS)
        CURDECKOPTIONSVAR[0].grid_remove()
        CURDECKOPTIONSVAR[0]=newDeckOptions
        newDeckOptions.grid(row=0,column=2,sticky=W)

    elif deck in getDecks():print("Deck already exists")
    else:print("Need to specify a name for the new deck")

def flashCardWindow(root):
    mfcWindow=tk.Toplevel(root)
    mfcWindow.title("Create New Flashcards")
    mfcWindow.minsize(700,700)
    mfcMainframe=ttk.Frame(mfcWindow)
    mfcMainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    mfcWindow.columnconfigure(0, weight=1)
    mfcWindow.rowconfigure(0, weight=1)

    #Select Deck and Flashcard type
    mfcMenu=ttk.Frame(mfcMainframe)
    selectedType=tk.StringVar()
    selectedType.set("Basic One-Sided")
    flashCardTypeOptions=ttk.OptionMenu(mfcMenu,selectedType,"Basic One-Sided",*TYPEOPTIONS)
    flashCardTypeOptions.grid(row=0,column=0,sticky=W)
    deckLabel=ttk.Label(mfcMenu, text="Deck:")
    deckLabel.grid(row=0,column=1,sticky=W)
    selectedDeck=tk.StringVar()
    deckOptions=ttk.OptionMenu(mfcMenu, selectedDeck,DECKOPTIONS[0],*DECKOPTIONS)
    CURDECKOPTIONSVAR.append(deckOptions)
    deckOptions.grid(row=0,column=2,sticky=W)
    createDeckLbl=ttk.Label(mfcMenu,text="Create new deck:")
    createDeckLbl.grid(row=0,column=3,sticky=W)
    newDeckName=StringVar()
    newDeckEntry=ttk.Entry(mfcMenu,width=15,textvariable=newDeckName)
    newDeckEntry.grid(row=0,column=4,sticky=W)
    newDeckBtn=ttk.Button(mfcMenu, text="Create",command=lambda:createDeck(newDeckName.get(),newDeckEntry,mfcMenu,selectedDeck))
    newDeckBtn.grid(row=0,column=5,sticky=W)
    mfcMenu.grid(row=0,column=0,sticky=NW)

    #Input the front of the card
    frontFrame=ttk.Frame(mfcMainframe)
    frontLbl=ttk.Label(frontFrame,text="\nFront of the card:")
    frontLbl.grid(row=0,column=0,sticky=W)
    front=StringVar()
    frontText=ttk.Entry(frontFrame,width=50,textvariable=front)
    frontText.grid(row=1,column=0,sticky=W)
    frontFrame.grid(row=1,column=0,sticky=W)

    #Input the back of the card
    backFrame=ttk.Frame(mfcMainframe)
    backLbl=ttk.Label(backFrame,text="\nBack of the card:")
    backLbl.grid(row=0,column=0,sticky=W)
    back=StringVar()
    backText=ttk.Entry(backFrame,width=50,textvariable=back)
    backText.grid(row=1,column=0,sticky=W)
    backFrame.grid(row=2,column=0,sticky=W)

    saveCardFrame=ttk.Frame(mfcMainframe)
    ttk.Label(saveCardFrame,text="\n").grid(row=0,column=0,sticky=W)
    errorLabel=ttk.Label(saveCardFrame,text="Please input both a front and a back for the card")
    saveCardBtn=ttk.Button(saveCardFrame,text="Save new flashcard",command=lambda:makeCard(frontText,backText,selectedDeck,front,back,errorLabel,selectedType.get()))
    saveCardBtn.grid(row=1,column=0,sticky=W)
    errorLabel.grid(row=2,column=0,sticky=W)
    errorLabel.grid_remove()
    saveCardFrame.grid(row=3,column=0,sticky=W)

    frontText.focus()

def setGoNext(*args):
    GONEXT[0]=True

def reviewDeck(deckfile,relevantFrames):
    btnFrm=relevantFrames[5]
    window=relevantFrames[4]
    frontLbl,backLbl=relevantFrames[2],relevantFrames[3]
    relevantFrames[1].focus()
    deck=open(str(p/"Flashcard Decks"/f"{deckfile}.txt")).read().splitlines()
    relevantFrames[0].grid_remove()
    relevantFrames[1].grid()
    toReview=[]
    dormant=[]
    for itm in deck:
        card,info=itm.split("**LASTREVIEW**")[0],itm.split("**LASTREVIEW**")[1]
        num=needsReviewing(info)
        if num<99999999:toReview.append((num,card,float(info.split("**LEARNINGSTAGE**")[1]),info.split("**LEARNINGSTAGE**")[0]))
        else:dormant.append(itm)
    while toReview:
        saveDeck(toReview,dormant,deckfile)
        GONEXT[0]==False
        frontLbl.config(text="")
        backLbl.config(text="")
        btnFrm.grid_remove()
        toReview=sorted(toReview)
        curCard=toReview[0]
        CURCARD[0]=curCard
        frontSide,backSide=curCard[1].split("**REVERSE**")[0],curCard[1].split("**REVERSE**")[1]
        frontLbl.config(text=frontSide)
        window.bind("<space>",setGoNext)
        while not GONEXT[0]:
            if not tk.Toplevel.winfo_exists(window) or not tk.Tk.winfo_exists(relevantFrames[6]):
                saveDeck(toReview,dormant,deckfile)
                return
            time.sleep(0.1)
        window.bind("<space>",lambda _:flashCardRight(1))
        backLbl.config(text=backSide)
        window.bind("1",flashCardWrong)
        window.bind("2",lambda _:flashCardRight(0.4))
        window.bind("3",lambda _:flashCardRight(1))
        window.bind("4",lambda _:flashCardRight(2))
        btnFrm.grid()
        while GONEXT[0]:
            if not tk.Toplevel.winfo_exists(window) or not tk.Tk.winfo_exists(relevantFrames[6]):
                saveDeck(toReview,dormant,deckfile)
                return
            time.sleep(0.1)
        window.unbind("1")
        window.unbind("2")
        window.unbind("3")
        window.unbind("4")
        toReview=toReview[1:]
        if NEWEVAL[0][0]==99999999:dormant.append(curCard[1]+"**LASTREVIEW**"+NEWEVAL[0][3]+"**LEARNINGSTAGE**"+f"{NEWEVAL[0][2]}") #the card's been successfully reviewed
        else: #the card needs to be reviewed again today
            ind = 0
            while ind<len(toReview) and toReview[ind][0]<=NEWEVAL[0][0]:ind+=1
            toReview=toReview[:ind]+[(NEWEVAL[0][0],NEWEVAL[0][1],NEWEVAL[0][2],NEWEVAL[0][3])]+toReview[ind:]
    saveDeck(toReview,dormant,deckfile)
    frontLbl.grid_remove()
    backLbl.grid_remove()
    btnFrm.grid_remove()
    relevantFrames[7].grid()

def saveDeck(toReview,dormant,deck):
    with open(str(p/"Flashcard Decks"/f"{deck}.txt"),"w") as output:
        for itm in dormant:output.write(itm+"\n")
        for itm in toReview:output.write(itm[1]+"**LASTREVIEW**"+itm[3]+"**LEARNINGSTAGE**"+f"{itm[2]}"+"\n")

def needsReviewing(info): #given info about a card, determines if it needs reviewing at the current moment
    lastRev,learnStage=info.split("**LEARNINGSTAGE**")[0].split("-"),float(info.split("**LEARNINGSTAGE**")[1])
    elapsedDays=(datetime.date.today()-datetime.date(int(lastRev[0]),int(lastRev[1]),int(lastRev[2]))).days
    print(elapsedDays)
    if elapsedDays==0:
        if learnStage>=1:
            return 99999999
        if learnStage==0:return 0
        curTime=datetime.datetime.now()
        elapsedMins=curTime.hour*60+curTime.minute-int(lastRev[3])-int(lastRev[4])
        neededMins=int(10+learnStage*10)
        if elapsedMins>=neededMins:return 0
        return neededMins-elapsedMins
    neededDays=int(2**(learnStage-1))
    if neededDays<=elapsedDays:return 0
    return 99999999
    
def flashCardWrong(*args):
    print(CURCARD[0])
    if CURCARD[0][2]>=1:
        date=datetime.datetime.now()
        NEWEVAL[0]=(10,CURCARD[0][1],0.5+0.1*CURCARD[0][2],f"{date.year}-{date.month}-{date.day}-{date.hour}-{date.minute}")
    else:
        date=datetime.datetime.now()
        NEWEVAL[0]=(1,CURCARD[0][1],0,f"{date.year}-{date.month}-{date.day}-{date.hour}-{date.minute}")
    GONEXT[0]=False
    return

def flashCardRight(inc):
    print(CURCARD[0])
    newLearningStage=CURCARD[0][2]+inc
    if newLearningStage>=1:
        date=datetime.datetime.now()
        NEWEVAL[0]=(99999999,CURCARD[0][1],newLearningStage,f"{date.year}-{date.month}-{date.day}-{date.hour}-{date.minute}")
    else:
        date=datetime.datetime.now()
        NEWEVAL[0]=(inc,CURCARD[0][1],newLearningStage,f"{date.year}-{date.month}-{date.day}-{date.hour}-{date.minute}")
    GONEXT[0]=False
    return

def returnToSelectDeckFrame(revDeckFrm,selDeckFrm,finishedReview,otherThings):
    ds=getDecks()
    for l in LBLS:
        l.grid_remove()
        LBLS.remove(l)
    for i,d in enumerate(ds):
        th=getNewThread(d,otherThings)
        tmpLbl=ttk.Button(selDeckFrm,text=d,command=th.start)
        tmpLbl.grid(row=i+1,column=0,sticky=W)
        LBLS.append(tmpLbl)
    revDeckFrm.grid_remove()
    finishedReview.grid_remove()
    selDeckFrm.grid()

def reviewCardWindow(root):
    rfcWindow=tk.Toplevel(root)
    rfcWindow.title("Review Flashcards")
    rfcWindow.minsize(700,700)
    rfcMainframe=ttk.Frame(rfcWindow)
    rfcMainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    rfcWindow.columnconfigure(0, weight=1)
    rfcWindow.rowconfigure(0, weight=1)

    #Reviewing a deck:
    reviewDeckFrame=ttk.Frame(rfcMainframe)
    frontLbl=ttk.Label(reviewDeckFrame,wraplength=600,text="",font=("Calibri",18),justify='center')
    frontLbl.grid(row=0,column=0,sticky=EW)
    backLbl=ttk.Label(reviewDeckFrame,wraplength=600,text="",font=("Calibri",18),justify='center')
    backLbl.grid(row=1,column=0,sticky=EW)
    ttk.Label(reviewDeckFrame,text="\n\n").grid(row=2,column=0,sticky=W)
    btnFrm=ttk.Frame(reviewDeckFrame)
    wrongBtn=ttk.Button(btnFrm,text="Wrong",command=flashCardWrong)
    hardBtn=ttk.Button(btnFrm,text="Hard",command=lambda:flashCardRight(0.4))
    rightBtn=ttk.Button(btnFrm,text="Correct",command=lambda:flashCardRight(1))
    easyBtn=ttk.Button(btnFrm, text="Too easy",command=lambda:flashCardRight(2))
    wrongBtn.grid(row=0,column=0,sticky=W)
    hardBtn.grid(row=0,column=1,sticky=W)
    rightBtn.grid(row=0,column=2,sticky=W)
    easyBtn.grid(row=0,column=3,sticky=W)
    btnFrm.grid(row=3,column=0,sticky=W)
    finishedReview=ttk.Label(reviewDeckFrame,text="You have completed all reviews for this deck due today!")
    finishedReview.grid(row=4,column=0,sticky=W)
    finishedReview.grid_remove()
    ttk.Label(reviewDeckFrame,text="\n\n").grid(row=8,column=0,sticky=W)
    

    #Select the deck to review:
    selectDeckFrame=ttk.Frame(rfcMainframe)
    ttk.Label(selectDeckFrame,text="Select a deck to review\n",font=("Courier",20)).grid(row=0,column=0,sticky=W)
    ds=getDecks()
    otherThings=[selectDeckFrame,reviewDeckFrame,frontLbl,backLbl,rfcWindow,btnFrm,root,finishedReview]
    for i,d in enumerate(ds):
        th=getNewThread(d,otherThings)
        tmpLbl=ttk.Button(selectDeckFrame,text=d,command=th.start)
        tmpLbl.grid(row=i+1,column=0,sticky=W)
        LBLS.append(tmpLbl)
    selectDeckFrame.grid(row=0,column=0,sticky=NW)



    returnToDeckSelection=ttk.Button(reviewDeckFrame,text="Select a different deck",command=lambda:returnToSelectDeckFrame(reviewDeckFrame,selectDeckFrame,finishedReview,otherThings))
    returnToDeckSelection.grid(row=9,column=0,sticky=W)
    reviewDeckFrame.grid(row=0,column=0,sticky=NW)
    reviewDeckFrame.grid_remove()

def getNewThread(d,l):
    return Thread(target=lambda:reviewDeck(d,l))
