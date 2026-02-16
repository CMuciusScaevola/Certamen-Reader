import tkinter as tk
from tkinter import *
from tkinter import ttk
SEARCHRESULTS = []
CURRESULTIDX=[1]
TTKITMS = {}
ALLQS=[]
TOPRANGE=[0]
BOOLS=['And','Or']


def searchForQWindow(root,allQs):
    ALLQS.append(allQs)
    searchWindow=tk.Toplevel(root)
    searchWindow.title("Search within rounds")
    searchWindow.minsize(900,600)
    sfQMainframe=ttk.Frame(searchWindow)
    sfQMainframe.grid(column=0, row=0, sticky=(N, W, E, S))
    searchWindow.columnconfigure(0, weight=1)
    searchWindow.rowconfigure(0, weight=1)
    searchWindow.bind("<Return>",searchForTerm)
    
    searchBarFrm = ttk.Frame(sfQMainframe)
    searchTerm = StringVar()
    TTKITMS["searchTerm"]=searchTerm
    searchEntry = ttk.Entry(searchBarFrm,width=30,textvariable=searchTerm)
    sb1=StringVar()
    TTKITMS['sb1']=sb1
    searchBool1 = ttk.OptionMenu(searchBarFrm,sb1,BOOLS[0],*BOOLS)
    searchTerm1 = StringVar()
    TTKITMS["searchTerm1"]=searchTerm1

    yearLvlFrm = ttk.Frame(sfQMainframe)
    lvlLbl=ttk.Label(yearLvlFrm,text="Level:")
    advCheckVar=IntVar()
    advCheckVar.set(1)
    intCheckVar=IntVar()
    intCheckVar.set(1)
    noviceCheckVar=IntVar()
    noviceCheckVar.set(1)
    agonCheckVar=IntVar()
    agonCheckVar.set(1)
    eliteCheckVar=IntVar()
    eliteCheckVar.set(1)
    TTKITMS['advCheckVar']=advCheckVar
    TTKITMS['intCheckVar']=intCheckVar
    TTKITMS['noviceCheckVar']=noviceCheckVar
    TTKITMS['agonCheckVar']=agonCheckVar
    TTKITMS['eliteCheckVar']=eliteCheckVar
    advancedCheck=ttk.Checkbutton(yearLvlFrm,text="Advanced",variable=advCheckVar)
    advancedCheck.grid(row=0,column=2)
    intermediateCheck=ttk.Checkbutton(yearLvlFrm,text="Intermediate",variable=intCheckVar)
    intermediateCheck.grid(row=0,column=3)
    noviceCheck=ttk.Checkbutton(yearLvlFrm,text="Novice",variable=noviceCheckVar)
    noviceCheck.grid(row=0,column=4)
    agonCheck=ttk.Checkbutton(yearLvlFrm,text="Agon",variable=agonCheckVar)
    agonCheck.grid(row=0,column=5)
    eliteCheck=ttk.Checkbutton(yearLvlFrm,text="Elite",variable=eliteCheckVar)
    eliteCheck.grid(row=0,column=1)
    lvlLbl.grid(row=0,column=0,sticky=W)
    #lvls.grid(row=0,column=1,sticky=W)
    yearLvlFrm.grid(row=1,column=0,sticky=W)

    searchEntry1 = ttk.Entry(searchBarFrm,width=30,textvariable=searchTerm1)
    searchBtn = ttk.Button(searchBarFrm,text="Search",command=searchForTerm)
    searchEntry.grid(row=0,column=0,sticky=W)
    searchEntry.focus()
    searchBool1.grid(row=0,column=1,sticky=W)
    searchEntry1.grid(row=0,column=2,sticky=W)
    searchBtn.grid(row=0,column=3,sticky=W)
    searchBarFrm.grid(row=0,column=0,sticky=W)

    showResultsfrm = ttk.Frame(sfQMainframe)
    showResultslbl = ttk.Label(showResultsfrm,font = ("Calibri", 17),text="",wraplength=800)
    showResultslbl.grid(row = 0,column = 0,sticky = W)
    showResultsfrm.grid(row=2,column=0,sticky=W)
    moveResultsRight = ttk.Button(showResultsfrm,text=">",command=updateSearchResultsRight)
    moveResultsLeft=ttk.Button(showResultsfrm,text="<",command=updateSearchResultsLeft)

    displayResultslbl = ttk.Label(sfQMainframe,font = ("Calibri",17),text = "",wraplength = 800)
    displayResultslbl.grid(row=3,column = 0,sticky= W)

    TTKITMS['displayResultslbl']=displayResultslbl
    TTKITMS['moveResultsRight']=moveResultsRight
    TTKITMS['showResultslbl']=showResultslbl
    TTKITMS['moveResultsLeft']=moveResultsLeft

def searchForTerm(*args):
    allQs=ALLQS[0]
    while SEARCHRESULTS:SEARCHRESULTS.remove(SEARCHRESULTS[0])
    CURRESULTIDX[0]=1
    TOPRANGE[0]=0
    term = TTKITMS['searchTerm'].get()
    term1=TTKITMS['searchTerm1'].get()
    if term:
        lvlOptions = []
        if TTKITMS["advCheckVar"].get():lvlOptions.append("from Advanced")
        if TTKITMS['intCheckVar'].get():lvlOptions.append("from Intermediate")
        if TTKITMS['noviceCheckVar'].get():lvlOptions.append("from Novice")
        if TTKITMS['agonCheckVar'].get():lvlOptions.append("from Agon")
        if TTKITMS['eliteCheckVar'].get():lvlOptions.append("from Elite")
        #print(lvlOptions)
        for q in allQs:
            for itm in lvlOptions:
                if itm in q:
                    if term.lower() in q.lower(): 
                        if term1 and TTKITMS['sb1'].get()=="And":
                            if term1.lower() in q.lower():
                                SEARCHRESULTS.append(q)
                        else:
                            SEARCHRESULTS.append(q)
                    elif term1 and TTKITMS['sb1'].get()=="Or":
                        if term1.lower() in q.lower():
                            SEARCHRESULTS.append(q)
        lbl = TTKITMS['showResultslbl']
        displayResultslbl=TTKITMS['displayResultslbl']
        moveResultsRight=TTKITMS['moveResultsRight']
        moveResultsLeft=TTKITMS['moveResultsLeft']
        moveResultsLeft.grid(row=0,column=1,sticky=W)
        moveResultsRight.grid(row=0,column=2,sticky=W)
        displayResultslbl.grid_remove()
        i=0
        while displayResultslbl.winfo_reqheight()<550 and TOPRANGE[0]<=len(SEARCHRESULTS):
            TOPRANGE[0] = CURRESULTIDX[0]+i
            resultsToShow = "\n\n".join(q for q in SEARCHRESULTS[CURRESULTIDX[0]-1:TOPRANGE[0]])
            displayResultslbl.config(text=resultsToShow)
            i+=1
        TOPRANGE[0]-=1
        resultsToShow = "\n\n".join(q for q in SEARCHRESULTS[CURRESULTIDX[0]-1:TOPRANGE[0]])
        displayResultslbl.config(text=resultsToShow)
        if len(SEARCHRESULTS)<TOPRANGE[0]:TOPRANGE[0] = len(SEARCHRESULTS)

        lbl.config(text = f"Showing results {CURRESULTIDX[0]}-{TOPRANGE[0]} of {len(SEARCHRESULTS)}")
        displayResultslbl.grid()
        #print(TOPRANGE[0])


def updateSearchResultsRight():
    if TOPRANGE[0]!=len(SEARCHRESULTS):
        CURRESULTIDX[0]=TOPRANGE[0]+1
        lbl = TTKITMS['showResultslbl']
        displayResultslbl=TTKITMS['displayResultslbl']
        displayResultslbl.grid_remove()
        i=0
        while displayResultslbl.winfo_reqheight()<550 and TOPRANGE[0]<=len(SEARCHRESULTS):
            TOPRANGE[0] = CURRESULTIDX[0]+i
            resultsToShow = "\n\n".join(q for q in SEARCHRESULTS[CURRESULTIDX[0]-1:TOPRANGE[0]])
            displayResultslbl.config(text=resultsToShow)
            i+=1
        TOPRANGE[0]-=1
        resultsToShow = "\n\n".join(q for q in SEARCHRESULTS[CURRESULTIDX[0]-1:TOPRANGE[0]])
        displayResultslbl.config(text=resultsToShow)
        if len(SEARCHRESULTS)<TOPRANGE[0]:TOPRANGE[0] = len(SEARCHRESULTS)

        lbl.config(text = f"Showing results {CURRESULTIDX[0]}-{TOPRANGE[0]} of {len(SEARCHRESULTS)}")
        displayResultslbl.grid()


def updateSearchResultsLeft():
    if CURRESULTIDX[0]!=1:
        TOPRANGE[0]=CURRESULTIDX[0]-1
        lbl = TTKITMS['showResultslbl']
        displayResultslbl=TTKITMS['displayResultslbl']
        displayResultslbl.grid_remove()
        while displayResultslbl.winfo_reqheight()<550 and CURRESULTIDX[0]>=1:
            CURRESULTIDX[0] = CURRESULTIDX[0]-1
            resultsToShow = "\n\n".join(q for q in SEARCHRESULTS[CURRESULTIDX[0]-1:TOPRANGE[0]])
            displayResultslbl.config(text=resultsToShow)

        CURRESULTIDX[0]+=1
        resultsToShow = "\n\n".join(q for q in SEARCHRESULTS[CURRESULTIDX[0]-1:TOPRANGE[0]])
        displayResultslbl.config(text=resultsToShow)
        if len(SEARCHRESULTS)<TOPRANGE[0]:TOPRANGE[0] = len(SEARCHRESULTS)

        lbl.config(text = f"Showing results {CURRESULTIDX[0]}-{TOPRANGE[0]} of {len(SEARCHRESULTS)}")
        displayResultslbl.grid()
