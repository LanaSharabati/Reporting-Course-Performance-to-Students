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
        self.set_font('Arial','', 26)
        self.set_fill_color(r= 192, g= 192, b = 192)
        self.cell(0, 10, 'Reporting Course Performance to Students', 1, 1, 'C',fill=True)
        self.cell(w=60, h=10, txt=" ",ln=1, align='C')
        
        
    def add_information(self,label,data):
        '''
        add the information for single student in pdf file
        
        '''
        for i in range(len(label)):
            self.set_font('Arial', 'B', 12)
            self.cell(w=25, h=5, txt=label[i]+":", ln=0)
            self.set_font('Arial', '', 12)
            if pd.isnull(data[label[i]].iloc[0]) == False:
                self.cell(w=35, h=5, txt=str(data[label[i]].iloc[0]),  ln=1)
            else:
                self.set_fill_color(r= 255, g= 204, b = 0)
                self.cell(w=35, h=5, txt="not submit",  ln=1,fill=True)
                
                
    def miss_activites(self,data,labels):
        '''
        add the student miss activetes if he miss 

        '''
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
        '''
        add image to pdf file

        '''
        self.image(url, x = 10, y = None, w = 130, h = 0, type = 'PNG')
          
        
    def weight(self,data,labels2):
        '''
        return list of wight for given labels
        '''
        rubric = data[data["Rubric"]=="Weight"]
        weight_value =[]
        for i in range(len(labels2)):
             weight_value.append(rubric[labels2[i]].iloc[0])
        return weight_value   
    
# class charts():    
    def course_weight(self,data,labels):
        '''
        A pie chart showing the weights of course activities
        then save as image to add in pdf file

        '''
        student_count = self.weight(data,labels[2:])#remove "Name" and "Email" labels
        fig, ax = plt.subplots()
        ax.pie(student_count[:-1],radius=1, labels= labels[2:-1],autopct=lambda p:'{:.0f}%'.format(p))
        ax.set_title('weights of course activitiese')
        plt.savefig('./pie_chart.png')
        self.pdf_image('./pie_chart.png')
        
        
    def student_grades(self,data,specific_data,labels2):
        '''
        bar chart of the student grades in the course activates as a fraction of the total grade for each activity
        save the chart as image to add to pdf file
        '''
        student_count =  self.weight(data,labels[2:])  
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
        
        
    def rank(self,specific_data,data,coulmn_number):
        '''
        A chart showing the student his/her rank within the whole class
        
        '''
        student_info = specific_data[labels[-1]].iloc[0]#total geades
        whole_data = np.sort(data[labels[-1]][1:])
        rank_number = np.where(whole_data  == student_info)#return array have the student rank number
        student_count= np.arange(coulmn_number)
        width = 0.7
        fig, ax = plt.subplots()
        ax.bar(student_count,whole_data, width, color = "blue")
        ax.bar(student_count[rank_number],student_info, width,  color = "red")
        chart_label=[]
        for i in range(len(student_count)):
            if i != rank_number[0][0]:
               chart_label.append(" ")
            else:
               chart_label.append("you")
        plt.xticks(np.arange(len(student_count))) 
        ax.set_xticklabels(chart_label, rotation='vertical', fontsize=12)  
        ax.set_ylabel('Grades')
        ax.set_title('whole class')
        ax.legend()
        fig.tight_layout()
        plt.savefig('./rank.png')
        self.pdf_image('./rank.png')
        
   
                
                 
         




df = pd.read_excel("grades.xlsx")#read data from excel file
labels = ["Name","Email","HW1","HW2","First","Second","Final","Total Grade"]#take the main labels from the excel file
    
def grades(data,labels):
    '''    
    #1 Student grades in each of the course activities 
    (e.g., First, Second, HW1, Final, etc.)
    '''
    students_data = data[labels]#only the student data
    names = students_data[labels[0]]#list for all students name,labels[0]== "Names"
    names = [names[i] for i in range(len(names)) if pd.isnull(names[i]) == False ]#check if the name value is nan do not analyze
    for i in range(len(names)):#generate pdf file for all student
        student_information = students_data[students_data["Name"] == names[i]]#Information for each student individually
        pdf = PDF()
        pdf.add_page()
        pdf.add_information(labels,student_information)#1 Student grades in each of the course activities
        pdf.miss_activites(student_information, labels)#2 Course activities that the student miss or did not submit
        pdf.course_weight(df,labels)#3A pie chart showing the weights of course
        pdf.student_grades(data,student_information,labels[2:])#4 A graphical representation (bar chart) of the student grades i
        pdf.rank(student_information,students_data,len(names))#5 A chart showing the student his/her rank within the whole class 
        pdf.output(names[i]+".pdf", 'F')#generate the pdf files the file name is the student name 
            
grades(df,labels)            