import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF



class PDF(FPDF):#
    def __init__(self):
        super().__init__()
        
    def print_pdf(self,item):
        self.cell(w=35, h=5, txt=str(item),  ln=1)
        
    def header(self):
        self.set_font('Arial','', 10)
        self.cell(0, 10, 'Reporting Course Performance to Students', 1, 1, 'C')
        self.cell(w=60, h=10, txt=" ",ln=1, align='C')
        
    def add_information(self,label,data,report_name):#1
        for i in range(len(label)):
            self.set_font('Arial', 'B', 10)
            self.cell(w=25, h=5, txt=label[i]+":", ln=0)
            self.set_font('Arial', '', 10)
            if pd.isnull(data[label[i]].iloc[0]) == False:
                self.cell(w=35, h=5, txt=str(data[label[i]].iloc[0]),  ln=1)
            else:
                self.cell(w=35, h=5, txt="not submit",  ln=1)
                
    def miss_activites(self,data,labels):
        miss =[]
        for i in range(len(labels)):
            if str(data[labels[i]].iloc[0]) == "nan":
                
                miss.append(labels[i])
        self.set_font('Arial', 'B', 12)
        self.cell(w=10, h=20, txt=" Course activities that the student miss or did not submit :", ln=0)
        if len(miss) != 0:
            self.cell(w=10, h=30, txt=str(miss),ln=1)
        else:
            self.cell(w=10, h=30, txt="all submit",ln=1)
            
    def pdf_image(self,url):
        self.image(url, x = 10, y = None, w = 120, h = 0, type = 'PNG')
                
    def weight(self,data,labels):
        x = data[data["Rubric"]=="Weight"]
        student_count =[]
        labels2 = labels[2:]
        for i in range(len(labels2)):
             student_count.append(x[labels2[i]].iloc[0])
        return student_count   
    
    def course_weight(self,data,labels):
        student_count = self.weight(data,labels)  
        fig, ax = plt.subplots()
        ax.pie(student_count[:-1],radius=1, labels= labels[2:-1],autopct=lambda p:'{:.0f}%'.format(p))
        ax.set_title('weights of course activitiese')
        plt.savefig('./pie_chart.png')
        self.pdf_image('./pie_chart.png')
        
    def student_grades(self,data,specific_data,labels2):
        student_count =  self.weight(data,labels)  
        actual_count = specific_data.iloc[0].iloc[2:]
        x = np.arange(len(labels2))
        width = 0.3
        fig, ax = plt.subplots()
        ax.bar(x, student_count, width, label='Full grade', color = "red")
        width = 0.2
        ax.bar(x, actual_count, width, label='your grade' , color = "blue")
        ax.set_ylabel('PPU Students')
        ax.set_title('Students per College')
        ax.set_xticks(x)
        ax.set_xticklabels(labels2, rotation='vertical')
        ax.legend()
        fig.tight_layout()
        plt.savefig('./bar chart of the student grades.png')
        self.pdf_image('./bar chart of the student grades.png')
        
    def rank(self,specific_data,data):
        s = specific_data[labels[-1]].iloc[0]
        male_count = np.sort(data[labels[-1]][1:])
        c= np.where(male_count == s)
        x= np.arange(10)
        width = 0.7
        fig, ax = plt.subplots()
        ax.bar( x,male_count, width, color = "blue")
        ax.bar( x[c],s, width,  color = "red")
        v=[]
        for i in range(len(x)):
            if i != c[0][0]:
                v.append(" ")
            else:
                v.append("you")
        plt.xticks(np.arange(len(x))) 
        ax.set_xticklabels(v, rotation='vertical', fontsize=12)  
        ax.set_ylabel('Grades')
        ax.set_title('whole class')
        ax.legend()
        fig.tight_layout()
        plt.savefig('./rank.png')
        self.pdf_image('./rank.png')
        
   
                
                 
         




df = pd.read_excel("grades.xlsx")#read data from excel file
labels = ["Name","Email","HW1","HW2","First","Second","Final","Total Grade"]#take the main labels from the excel file
students_data = df[labels]#only the student data


    
    
def grades(data,labels):
    '''    
    #1 Student grades in each of the course activities 
    (e.g., First, Second, HW1, Final, etc.)
    '''
    students_data = data[labels]#only the student data
    names = students_data[labels[0]]#list for all students name,labels[0]== "Names"
    for i in range(len(names)):#generate pdf file for all student
        if pd.isnull(names[i]) == False:#chic if the name value is nan do not analyze
            student_information = students_data[students_data["Name"] == names[i]]#Information for each student individually
            pdf = PDF()
            pdf.add_page()
            pdf.add_information(labels,student_information ,names[i])#1
            pdf.miss_activites(student_information, labels)#2
            pdf.course_weight(df,labels)
            pdf.student_grades(data,student_information,labels[2:])
            pdf.rank(student_information,students_data)
            
    
            pdf.output(names[i]+".pdf", 'F')
            
grades(df,labels)            