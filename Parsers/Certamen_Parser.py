import sys;args=sys.argv[1:]
import re

st=open(args[0]+".txt").read()
st=st.replace("**SCORE CHECK**","").replace("SCORE CHECK","").replace("LATIN LITERATURE","").replace("â€™","'").replace("È³","y").replace("ROMAN HISTORY","").replace("EXTRA HISTORY","").replace("EXTRA MYTHOLOGY","").replace("B3","B1").replace("B4","B2").replace("Bonus 1","B1").replace("Bonus 2","B2").replace("B1 & B2","B1").replace("B1/2","B1").replace("B1/B2","B1").replace("________________","").replace("â€¦","...")
st=st.replace("LANGUAGE", "").replace("newline","\n").replace("LATIN LITERATURE","").replace("newline","\n").replace(" and "," & ").replace(" or ", " | ").replace("(or","(|").replace("Prompt on","PROMPT ON").replace("prompt on","PROMPT ON").replace("Bonuses 1 & 2","B1").replace("B1+B2","B1").replace("B1+2","B1").replace("B1 ","B1. ").replace("B2 ","B2. ")
st="\n"+st+"\n"
while "\n\n" in st:
    st=st.replace("\n\n","\n")
#matches=re.findall(r"(?<=[^A-Za-z])\d?\d\..*?\n(?=\d?\d\.|$)",st,re.S)
matches=re.findall(r"(?<=[^A-Za-z])\d?\d(?:\.|:).*?\n(?=\d?\d(?:\.|:)|$)",st,re.S)
tossups=[]
tossupAnswers=[]
bonus1s=[]
bonus1answers=[]
bonus2s=[]
bonus2answers=[]
replacementct=0
lens = []
with open("Download/Rounds/" +args[0]+"_Parsed.txt",'w') as output:
    print(len(matches))
    for match in matches:
        lens.append((len(match),match))
        print("Hello",match,"\n\n")
        if "B1 & B2" in match:replacementct+=1
        match=match.replace("B1&B2","B1").replace("B1&2","B1").replace("B1 & B2","B1").replace("B1.","B1:").replace("B2.","B2:")
        match=match.split("B1:") if "B1:" in match else match.split("B1.")
        tu=match[0]
        boni="B1:" +match[1]
        if "B2:" in boni:
            boni=boni.split("B2:")
            boni[1]="B2:"+boni[1]
        else:boni=[boni]
        tossup=re.findall(r"\d(?::|\.) .*?\n(?=[^a-z\n]+$)",tu,re.S)
        if not tossup:tossup=re.findall(r"\d(?:\.|:) .*?\n(?=[^a-z\n]+$)",tu,re.S)
        tossup=tossup[0]
        tossupAns=tu[tu.index(tossup)+len(tossup):]
        tossups.append(tossup)
        tossupAnswers.append(tossupAns)
        print(boni)
        bonus1=re.findall(r"\d(?:\.|:).*?\n(?=[^a-z\n]+$)",boni[0],re.S)[0]
        bonus1ans=boni[0][boni[0].index(bonus1)+len(bonus1):]
        bonus1s.append(bonus1)
        bonus1answers.append(bonus1ans)
        bonus2=""
        if len(boni)>1:
            bonus2=re.findall(r"\d(?:\.|:).*?\n(?=[^a-z\n]+$)",boni[1],re.S)
            if bonus2:
                bonus2=bonus2[0]
                bonus2ans=boni[1][boni[1].index(bonus2)+len(bonus2):]
                bonus2s.append(bonus2)
                bonus2answers.append(bonus2ans) 
        stringToWrite=tossup[3:]+"ANSWER:"+tossupAns+"BONUS:"+bonus1[2:]+"ANSWER:"+bonus1ans
        if bonus2: stringToWrite+="BONUS:"+bonus2[2:]+"ANSWER:"+bonus2ans
        stringToWrite=stringToWrite.replace("\n"," ").replace(" & "," and ").replace(" | ", " or ").replace("(|","(or")
        output.write(stringToWrite+"\n")
print(len(matches))
print(max(lens))