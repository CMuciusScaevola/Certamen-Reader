# Certamen-Reader
Reads Certamen questions and allows buzzing

Currently only contains Advanced level rounds

Flashcard feature is not as good as online ones such as Anki, but it mostly functions and does basic spaced repetition. 

"Search for term within rounds" button allows searching for exact term matches within all questions. Can also use boolean searches with and & or.

Report faulty question saves the question to a faulty questions file, but I have to fix them manually. Faulty questions are those with incorrect information or those that have been incorrectly parsed (e.g. a part of the answerline is shown with the question itself)

Facts are saved to a text file; I will later implement a way to look over them without having to open that text file.

Once answer is submitted, the correct answer will be displayed; the reader does not grade answers.

Keybindings:
Read next question/bonus: "n"
Skip current question (only works whilst reading, not after answering): "s"
Save fact: "f" once question is finished
Buzz: spacebar
Submit answer: enter
