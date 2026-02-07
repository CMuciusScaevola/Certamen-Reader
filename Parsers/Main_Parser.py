#Handles most cases pretty well, designed for collegiate rounds as well as NJCL and Keartamen, which follow similar formats

import sys;args=sys.argv[1:]
import re

st=open("Raw Rounds/"+args[0]+".txt",encoding='utf-8').read()
#Remove common items that are undesirable
while "——" in st:st=st.replace("——","—").replace("*","")
st=st.replace("Tossup.","TU1:").replace("Bonus.","B1: ").replace("*PAUSE FOR SCORE UPDATE*","").replace("**PAUSE FOR SCORE UPDATE**","").replace("***PAUSE FOR SCORE UPDATE***","").replace("TOSSUP","TU1").replace("BONUS","B1").replace("***PAUSE FOR SCORE CHECK***","").replace("**PAUSE FOR SCORE CHECK**","").replace("*PAUSE FOR SCORE CHECK*","")
st=st.replace("\t","  ").replace("— [FINAL SCORE CHECK] —","").replace("— [SCORE CHECK] —","").replace(" B1","\nB1").replace(" B2","\nB2")
st=st.replace("**SCORE CHECK**","").replace("SCORE CHECK","").replace("Score Check","").replace("LATIN LITERATURE","").replace("ROMAN HISTORY","").replace("EXTRA HISTORY","").replace("EXTRA MYTHOLOGY","").replace("History:","").replace("Myth:","").replace("Language:","").replace("Literature:","").replace("B3","B1").replace("B4","B2").replace("Bonus 1","B1").replace("Bonus 2","B2").replace("B1 & B2","B1").replace("B1/2","B1").replace("B1/B2","B1").replace("________________","")
st=st.replace("LANGUAGE", "").replace("newline","\n").replace("EXTRA QUESTIONS","").replace("Extra Questions","").replace("LATIN LITERATURE","").replace("newline","\n").replace(" and "," & ").replace(" or ", " | ").replace("(or","(|").replace("Prompt on","PROMPT ON").replace("prompt on","PROMPT ON").replace("Bonuses 1 & 2","B1").replace("B1+B2","B1").replace("B1+2","B1").replace("B1 ","B1. ").replace("B2 ","B2. ")
st=st.replace("Advanced — Preliminary Round One","").replace("Advanced — Preliminary Round Two","").replace("Advanced — Preliminary Round Three","").replace("Advanced — Semifinals","").replace("Advanced — Finals","").replace("Advanced — Semis","").replace("Advanced — Round 1","").replace("Advanced — Round 2","").replace("Advanced — Round 3","").replace("ROUND ONE","").replace("ROUND TWO","").replace("ROUND THREE","")
st=st.replace("Advanced – Semifinal Round","").replace("Advanced – Final Round","").replace("Advanced Division","").replace("Advanced Level","").replace("Round 1","").replace("Round 2","").replace("Round 3","").replace("Semifinal Round","").replace("Final Round","").replace("vel sim","").replace("REPLACEMENT TOSSUPS","").replace("ADVANCED DIVISION","").replace("ROUND 1","").replace("ROUND 2","").replace("ROUND 3","").replace("FINAL ROUND","").replace("SEMI-FINAL ROUND","")
st=st.replace("Replacement History:","").replace("Replacement Mythology:","").replace("Replacement Language:","").replace("Replacement Literature:","").replace("HISTORY","").replace("MYTHOLOGY","").replace("LANGUAGE","").replace("LITERATURE","").replace("ADVANCED","").replace("EXTRA","")
st=st.replace("Β","\n\nB").replace("B1&B2","\n\nB1").replace("B1&2","\n\nB1").replace("B1 & B2","\n\nB1").replace("B1.","\n\nB1:").replace("B2.","\n\nB2:")
st=st.replace("4th", "4TH").replace("1st","1ST").replace("2nd","2ND").replace("3rd","3RD")

while "  " in st:st=st.replace("  "," ").replace("\n \n","\n")
for num in range(1,21):
    st=st.replace(str(num)+".",str(num)+". ").replace(" #"+str(num)," "+str(num)).replace("#"+str(num)," "+str(num))


#Get rid of page numbers:
ind = 0
while ind<len(st):
    match = re.search(r"(?<=\n)\d+\n",st[ind:],flags=re.S|re.UNICODE)
    
    if match:

        st=st[:match.span()[0]+ind]+""+st[match.span()[1]+ind:]
        ind=match.span()[1]+ind
        match=""
    else:ind=len(st) #ends the loop if no more spots are found

#Ensure there is a newline between questions and answers
ind = 0
while ind<len(st):
    match = re.search(r"(?<=[^A-Z\d](\.|\?|\"|\'|”|!)) +(?=[^a-z ][^a-z]+)",st[ind:],flags=re.S|re.UNICODE)
    if match:
        st=st[:match.span()[0]+ind]+"\n"+st[match.span()[1]+ind:]
        ind=match.span()[1]+ind
        match=""
    else:ind=len(st)

#Make sure all answerlines have no newlines
ind=0
while ind<len(st):
    match = re.search(r"(?<=[A-Z])\n(?=[AC-Z\(\[\|])(?!B1:|B2:)",st[ind:],flags=re.S|re.UNICODE)
    
    if match:
        print(match)
        st=st[:match.span()[0]+ind]+" "+st[match.span()[1]+ind:]
        ind=match.span()[1]+ind
        match=""
    else:ind=len(st) #ends the loop if no more spots are found

st="\n"+st+"\n"
while "\n\n" in st:
    st=st.replace("\n\n","\n")
while "  " in st:st=st.replace("  "," ").replace("\n \n","\n")

matches=re.findall(r"(?<=[^\w])\d?\d(?:\.|:).*?\n(?=(?:(?:TU )|TU)?\d?\d(?:\.|:)|$)",st,flags=re.S|re.UNICODE) #Extract the questions into a list (TU-B-B pairs)

tossups=[]
tossupAnswers=[]
bonus1s=[]
bonus1answers=[]
bonus2s=[]
bonus2answers=[]
lens = []
with open("Download/Rounds/" +args[0]+"_Parsed.txt",'w',encoding='utf-8') as output:
    for match in matches:
        lens.append((len(match),match))
        match=match.split("B1:") if "B1:" in match else match.split("B1.")
        tu=match[0]
        print(match)
        boni="B1:" +match[1] 
        if "B2:" in boni:
            boni=boni.split("B2:")
            boni[1]="B2:"+boni[1]
        else:boni=[boni]
        tossup=re.findall(r"\d(?::|\.) .*?\n(?=[^a-z\n]+$|GREEKANS.*$)",tu,re.S)
        if not tossup:tossup=re.findall(r"\d(?:\.|:) .*?\n(?=[^a-z\n]+$|GREEKANS.*$)",tu,re.S)
        tossup=tossup[0]
        tossupAns=tu[tu.index(tossup)+len(tossup):]
        tossups.append(tossup.replace("GREEKANS:",""))
        tossupAnswers.append(tossupAns.replace("GREEKANS:",""))
        #print(boni)
        bonus1=re.findall(r"\d(?:\.|:).*?\n(?=[^a-z\n]+$|GREEKANS.*$)",boni[0],re.S)[0]
        bonus1ans=boni[0][boni[0].index(bonus1)+len(bonus1):]
        bonus1s.append(bonus1.replace("GREEKANS:",""))
        bonus1answers.append(bonus1ans.replace("GREEKANS:",""))
        bonus2=""
        if len(boni)>1:
            bonus2=re.findall(r"\d(?:\.|:).*?\n(?=[^a-z\n]+$|GREEKANS.*$)",boni[1],re.S)
            if bonus2:
                bonus2=bonus2[0]
                bonus2ans=boni[1][boni[1].index(bonus2)+len(bonus2):]
                bonus2s.append(bonus2.replace("GREEKANS:",""))
                bonus2answers.append(bonus2ans.replace("GREEKANS:","")) 
        stringToWrite=tossup[3:]+"ANSWER:"+tossupAns+"BONUS:"+bonus1[2:]+"ANSWER:"+bonus1ans
        if bonus2: stringToWrite+="BONUS:"+bonus2[2:]+"ANSWER:"+bonus2ans
        stringToWrite=stringToWrite.replace("\n"," ").replace(" & "," and ").replace(" | ", " or ").replace("(|","(or")
        output.write(stringToWrite+"\n")
print(len(matches))
#print(max(lens))