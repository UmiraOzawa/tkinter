import tkinter as tk
import tkinter.messagebox
import random

login_ready = 0
test_finished = 0
# Add the information of student into file excel named login.csv
def Add_user():
    global entryLogin, entryPassword, login_ready 
    doc_login = open("login.csv", "a")
    if(entryLogin.get() != "" and entryPassword.get() != ""):
        login_ready = 1
        doc_login.write(entryLogin.get()+";"+entryPassword.get()+";")
        tk.messagebox.showinfo(title='Un message important...', message= "Login succesfully")
        entryLogin.delete(0, "end")
        entryPassword.delete(0,"end")
    else: 
        login_ready = 0
        tk.messagebox.showinfo(title='Un message important...', message= "Missing fields")
        entryLogin.delete(0, "end")
        entryPassword.delete(0,"end")
    doc_login.close()


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
random.shuffle(list_questions)

# Créer la classe QCM
class QCM():
    def __init__(self):
        self.qcm_frame = tk.Toplevel(master= mainWnd, width = 750, height = 500)
        self.q_number = 0
        self.create_frame_title()
        self.display_qnb()
        self.display_title()
        self.display_question()
        self.opt_selected = tk.IntVar()
        self.opts = self.radio_buttons()
        self.display_reponses()
        self.valide_button()
        self.point = 0
        self.display_points()
        self.data_size=len(list_questions)
        self.qcm_frame.protocol("WM_DELETE_WINDOW", self.check_closed)

    def create_frame_title(self):
        self.qcm_frame.title("QCM")    
    def display_title(self):
        title = tk.Label(master = self.qcm_frame ,text = "QCM", font = ("Arial", 20))
        title.place(x = 300, y = 0)
    def display_question(self):
        question = tk.Label(master = self.qcm_frame ,text = list_questions[self.q_number].title, font = ("Arial", 15), width=60,justify="left")
        question.place(x = 0, y = 75)
    def display_qnb(self):
        qnb = tk.Label(master = self.qcm_frame ,text = "Question "+str(self.q_number +1), font = ("Arial", 15), width=30)
        qnb.place(x = 500, y = 0)

    def check_ans(self, q_number):
        # checks for if the selected option is correct
        if self.opt_selected.get() == list_questions[self.q_number].reponses.index(list_questions[self.q_number].reponse_correcte.replace("\n", "")) +1:
            # if the option is correct it return true
            return True
        
    def valide(self):
         
        # Check if the answer is correct
        if self.check_ans(self.q_number):
             
            # if the answer is correct it increments the correct by 1
            self.point += 1
         
        else: 
            correcteur = tkinter.messagebox.showinfo("You have wrong anwser", "The right answer is: " + list_questions[self.q_number].reponse_correcte)
         # Moves to next Question by incrementing the q_no counter
        self.q_number += 1
         
        # checks if the q_no size is equal to the data size
        if self.q_number==self.data_size:
            # if it is correct then it displays the score
            test_finished = 1
            self.display_points()
            self.display_result()
            self.add_result()
            # destroys the GUI
            mainWnd.destroy()
        else:
            # shows the next question
            for widgets in self.qcm_frame.winfo_children():
                widgets.destroy()
            self.create_frame_title()
            self.display_title()
            self.opts = self.radio_buttons()
            self.display_qnb()
            self.display_question()
            self.display_reponses()
            self.display_points()
            self.valide_button()
    def add_result(self):
        if login_ready == 1:
            # Add the result into the file excel named result.csv
            doc_result = open("login.csv", "a")
            doc_result.write(str(self.point) + "\n")
            doc_result.close()
        
    def display_result(self):
        # displays the result when the quiz ends
        result = tkinter.messagebox.showinfo("Resultat", "You scored "+str(self.point)+" points")
    def valide_button(self):
        # button to display the next question
        button = tk.Button(master = self.qcm_frame, text = "Valide", command = self.valide, width = 10, bg = "grey", fg = "white", font = ("ariel", 16, "bold"))
        button.place(x = 350, y = 380)
    
    def display_points(self):
        # displays the points scored by the user
         point = tk.Label(master = self.qcm_frame ,text = "You scored "+str(self.point), font = ("Arial", 15), width= 15)
         point.place(x = 0, y = 0)
         
    def radio_buttons(self):
         
        # initialize the list with an empty list of options
        q_list = []
         
        # position of the first option
        y_pos = 150
         
        # adding the options to the list
        while len(q_list) < len(list_questions[self.q_number].reponses):
             
            # setting the radio button properties
            radio_btn = tk.Radiobutton(master = self.qcm_frame,text=" ",variable=self.opt_selected, value = len(q_list) +1, font = ("ariel",14), width=30, justify="left")
             
            # adding the button to the list
            q_list.append(radio_btn)
             
            # placing the button
            radio_btn.place(x = 100, y = y_pos)
             
            # incrementing the y-axis position by 40
            y_pos += 40
         
        # return the radio buttons
        return q_list
    
    def display_reponses(self):
        val=0
        # deselecting the options
        self.opt_selected.set(0)
         
        # looping over the options to be displayed for the
        # text of the radio buttons.
        for option in list_questions[self.q_number].reponses:
            self.opts[val]['text']=option
            val+=1   

    def check_closed(self):
        if test_finished !=1:    
            self.add_result()
        self.qcm_frame.destroy()
        login_frame.quit()

# Main window (login frame)
mainWnd = tk.Tk(className='Login')

login_frame = tk.Canvas(master = mainWnd, width = 300,
                 height = 300)


  
login_frame.pack(fill="both", expand=True)


labelLogin = tk.Label(master=login_frame, text='Username: ')
labelLogin.place(x=0, y=50)
entryLogin = tk.Entry(master=login_frame)
entryLogin.place(x=75, y=50)

labelPassword = tk.Label(master=login_frame, text='Password: ')
labelPassword.place(x=0, y=75)
entryPassword = tk.Entry(master=login_frame, show="*")
entryPassword.place(x=75, y=75)

buttonLogin = tk.Button(master=login_frame, text='Login', command = lambda: [Add_user(), QCM()])
buttonLogin.place(x=110, y=100)
mainWnd.bind('<Return>', lambda event: [Add_user(), QCM()])

# Event loop
mainWnd.mainloop()
