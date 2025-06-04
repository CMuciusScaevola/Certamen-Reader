#Handles simpler round formattings that have "ANS" to indicate where answerlines start

import sys;args=sys.argv[1:]
import re

st=open("Raw Rounds/"+args[0]+".txt",encoding='utf-8').read()
#Remove common items that are undesirable
while "——" in st:st=st.replace("——","—").replace("*","")
while "  " in st:st=st.replace("  "," ")
for num in range(1,21):st=st.replace(str(num)+".",str(num)+". ")
st=st.replace("a. BONUS","BONUS").replace("b. BONUS","BONUS").replace("WRITE-DOWN","").replace("WRITE DOWN","").replace("WRITEDOWN","")
st=st.replace("ANS:\n","ANS: ")


#Get rid of page numbers:
ind = 0
while ind<len(st):
    match = re.search(r"(?<=\n)\d+\n\n",st[ind:],flags=re.S|re.UNICODE)
    
    if match:

        st=st[:match.span()[0]+ind]+""+st[match.span()[1]+ind:]
        ind=match.span()[1]+ind
        match=""
    else:ind=len(st) #ends the loop if no more spots are found

#Make sure all answerlines have no newlines
ind=0
while ind<len(st):
    match = re.search(r"(?<=[A-Z]([A-Z]| ))\n(?=[AC-Z\(\[]\|)(?!B1:|B2:)",st[ind:],flags=re.S|re.UNICODE)
    
    if match:

        st=st[:match.span()[0]+ind]+" "+st[match.span()[1]+ind:]
        ind=match.span()[1]+ind
        match=""
    else:ind=len(st) #ends the loop if no more spots are found

st="\n"+st+"\n"
while "\n\n" in st:
    st=st.replace("\n\n","\n")
matches=re.findall(r"(?<=TOSSUP:).*?BONUS.*?ANS.*?(?=\n.*?TOSSUP)",st,re.S)
tossups=[]
tossupAnswers=[]
bonus1s=[]
bonus1answers=[]
bonus2s=[]
bonus2answers=[]
replacementct=0

with open("Download/Rounds/" +args[0]+"_Parsed.txt",'w',encoding='utf-8') as output:
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
        #print(tossup)
        tossupAns=tu.split("ANS:")[1]
        tossups.append(tossup)
        tossupAnswers.append(tossupAns)
        #print(b1)
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
    