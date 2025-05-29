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
    showResultsfrm.grid(row=1,column=0,sticky=W)
    moveResultsRight = ttk.Button(showResultsfrm,text=">",command=updateSearchResultsRight)
    moveResultsLeft=ttk.Button(showResultsfrm,text="<",command=updateSearchResultsLeft)

    displayResultslbl = ttk.Label(sfQMainframe,font = ("Calibri",17),text = "",wraplength = 800)
    displayResultslbl.grid(row=2,column = 0,sticky= W)

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
        for q in allQs:
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
        print(TOPRANGE[0])


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
