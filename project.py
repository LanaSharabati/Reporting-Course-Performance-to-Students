import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF



class PDF(FPDF):
    def __init__(self):
        super().__init__()
    # def header(self):
    #     self.set_font('Arial', '', 12)
    #     self.cell(0, 10, 'Reporting Course Performance to Students', 1, 1, 'C')
   


def pdf_tabel(label,data,report_name):
    pdf = PDF() # Instance of custom class
    pdf.add_page()
    # Table Header
    pdf.set_font('Arial','', 10)
    pdf.cell(0, 10, 'Reporting Course Performance to Students', 1, 1, 'C')
    pdf.cell(w=60, h=10, txt=" ",ln=1, align='C')
    for i in range(len(label)):
        pdf.set_font('Arial', 'B', 10)
        pdf.cell(w=25, h=5, txt=label[i]+":", ln=0)
        pdf.set_font('Arial', '', 10)
        pdf.cell(w=35, h=5, txt=str(data[label[i]].iloc[0]),  ln=1)
    miss = miss_activites(data,label)     
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(w=10, h=20, txt=" Course activities that the student miss or did not submit :", ln=0) 
    if len(miss) != 0:
        pdf.cell(w=10, h=30, txt=str(miss),ln=1)
    else:
        pdf.cell(w=10, h=30, txt="nothing",ln=1)
        
        
    pdf.image('./pie_chart.png', x = 10, y = None, w = 120, h = 0, type = 'PNG') 
    pdf.image('./bar chart of the student grades.png', x = 10, y = None, w = 120, h = 0, type = 'PNG')
    pdf.image('./rank.png', x = 10, y = None, w = 120, h = 0, type = 'PNG')
    
    pdf.output(report_name+".pdf", 'F')
    
def miss_activites(data,labels):
    miss =[]
    for i in range(len(labels)):
        if str(data[labels[i]].iloc[0]) == "nan":
            miss.append(labels[i])
    return miss
            
    
def grades(data,labels):
    '''    
    #1 Student grades in each of the course activities 
    (e.g., First, Second, HW1, Final, etc.)
    '''
    student_data = data[labels]
    names = student_data["Name"]
    for i in range(len(names)):
        if pd.isnull(names[i]) == False:
            specific_data= student_data[student_data["Name"] == names[i]]
            student_grades(data,specific_data,labels[2:])
            rank(specific_data)
            pdf_tabel(labels,specific_data,names[i])
           
               
def course_weight(data,labels):
    student_count = weight(data)  
    total = sum(student_count)
    fig, ax = plt.subplots()
    ax.pie(student_count[:-1],radius=1, labels= labels[2:-1],autopct=lambda p: '{:.0f}%'.format(p * total / 100))
    ax.set_title('weights of course activitiese')
    plt.savefig('./pie_chart.png')
    
def weight(data):
    x = data[data["Rubric"]=="Weight"]
    student_count =[]
    labels2 = labels[2:]
    for i in range(len(labels2)):
        student_count.append(x[labels2[i]].iloc[0])
    return student_count
    
def student_grades(data,specific_data,labels2):
    student_count = weight(data) 
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
    
def rank(specific_data):
    s = specific_data[labels[-1]].iloc[0]
    male_count = np.sort(student_data[labels[-1]][1:])
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
    


df = pd.read_excel("grades.xlsx")
labels = ["Name","Email","HW1","HW2","First","Second","Final","Total Grade"]
student_data = df[labels]
course_weight(df,labels)
grades(df,labels)


