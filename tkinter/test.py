#Creer la classe Questions
class Questions:
    def __init__(self):
        self.title = ""
        self.reponses = []
        self.reponse_correcte = " "
    def __repr__(self):
        return self.title + " " + str(self.reponses) + " " + self.reponse_correcte

# Read the csv file and add the questions into the list
list_questions = []
doc = open("question.csv", "r")
line = doc.readline()
while line != "":
    line = doc.readline()
    if(line != ""):
        question = Questions()
        question.title = line
        question.reponses = doc.readline().split(";")
        for i in range(len(question.reponses)):
            question.reponses[i] = question.reponses[i].replace("\n", "") 
        question.reponse_correcte = doc.readline()
        list_questions.append(question)
doc.close()
b = 100
a= b
b = 6
print(a)