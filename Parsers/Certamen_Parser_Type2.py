import sys;args=sys.argv[1:]
import re

st=open(args[0]+".txt").read()
st=st.replace("**SCORE CHECK**","").replace("SCORE CHECK","").replace("LATIN LITERATURE","").replace("ROMAN HISTORY","").replace("EXTRA HISTORY","").replace("EXTRA MYTHOLOGY","").replace("È³","y").replace("â€™","'")#.replace("B3","B1").replace("B4","B2").replace("Bonus 1","B1").replace("Bonus 2","B2").replace("B1 & B2","B1").replace("B1/2","B1").replace("B1/B2","B1").replace("________________","").replace("â€¦","...")
st=st.replace("LANGUAGE", "").replace("LATIN LITERATURE","").replace("newline","\n").replace(" and "," & ").replace(" or ", " | ").replace("(or","(|").replace("Prompt on","PROMPT ON").replace("prompt on","PROMPT ON").replace("\nANS:"," ANS:")#.replace("Bonuses 1 & 2","B1").replace("B1+B2","B1").replace("B1+2","B1").replace("B1 ","B1. ").replace("B2 ","B2. ")
st="\n"+st+"\n"
while "\n\n" in st or "  " in st:
    st=st.replace("\n\n","\n").replace("  "," ")
matches=re.findall(r"(?<=TOSSUP:).*?BONUS.*?ANS.*?(?=\n.*?TOSSUP)",st,re.S)
tossups=[]
tossupAnswers=[]
bonus1s=[]
bonus1answers=[]
bonus2s=[]
bonus2answers=[]
replacementct=0

with open("Download/Rounds/" +args[0]+"_Parsed.txt",'w') as output:
    for match in matches:
        match=match.replace("1.","").replace("2.","").replace("\n"," ")
        match=match.split("BONUS:")
        print(match)
        tu=match[0]
        b1=match[1]
        if len(match)>2:
            b2=match[2]
        else:b2=""
        tossup=tu.split("ANS:")[0]
        print(tossup)
        tossupAns=tu.split("ANS:")[1]
        tossups.append(tossup)
        tossupAnswers.append(tossupAns)
        print(b1)
        bonus1=b1.split("ANS:")[0]
        bonus1ans=b1.split("ANS:")[1]
        bonus1s.append(bonus1)
        bonus1answers.append(bonus1ans)
        bonus2=""
        if b2:
            bonus2=b2.split("ANS:")[0]
            bonus2ans=b2.split("ANS:")[1]
            bonus2s.append(bonus2)
            bonus2answers.append(bonus2ans) 
        stringToWrite=tossup+"ANSWER:"+tossupAns+"BONUS:"+bonus1+"ANSWER:"+bonus1ans
        if bonus2: stringToWrite+="BONUS:"+bonus2+"ANSWER:"+bonus2ans
        stringToWrite=stringToWrite.replace("\n"," ").replace(" & "," and ").replace(" | ", " or ").replace("(|","(or")
        output.write(stringToWrite+"\n")
print(len(matches))
    