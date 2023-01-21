import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from fpdf import FPDF #pip install fpdf
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders


class student:
    def __init__(self,data,label):
        self.labels = label
        self.weight_label = label[2:]
        self.data = data
        self.students_data = data[label]#only the student data
        self.names = [self.students_data[label[0]][i] for i in range(len(self.students_data[label[0]])) if pd.isnull(self.students_data[label[0]][i]) == False ]#check if the name value is nan do not analyze
        self.weight = self.weight()
        self.emails = [self.students_data[label[1]][i] for i in range(len(self.students_data[label[0]])) if pd.isnull(self.students_data[label[0]][i]) == False ]
        
        #["Name","Email","HW1","HW2","First","Second","Final","Total Grade"]
        
    def get_weight_label(self):
        return self.weight_label
    def get_names(self):
        return self.names
    def get_students_data(self):
        return self.students_data
    def get_weight(self):
        return self.weight
    def get_emails(self):
        return  [self.students_data[self.labels[1]][i] for i in range(len(self.students_data[self.labels[0]])) if pd.isnull(self.students_data[self.labels[0]][i]) == False ]
    def get_HW1(self):
        return  [self.students_data[self.labels[2]][i] for i in range(len(self.students_data[self.labels[0]])) if pd.isnull(self.students_data[self.labels[0]][i]) == False ]
    
    def set_weight_label(self ,wl):
        self.weight_label = wl
    def set_names(self , n):
        self.names = n
    def set_single_names(self , n,i):
        self.students_data[self.labels[0]][i] = n    
    def set_students_data(self , sd):
        self.students_data = sd
    def set_weight(self , w):
        self.weight = w
    def set_emails(self , e):
        self.emails = e     
    def set_single_emails(self , e,i):
        self.students_data[self.labels[1]][i] = e 
    def set_single_HW1(self , H1,i):
        self.students_data[self.labels[2]][i] = H1     
    
        
    
    def specific_student(self,student_number):
        return self.students_data[self.students_data["Name"] == self.names[student_number]]
    
    
    def submit_list(self,student_number):
        '''
        return information for single student 
        
        '''
        data = self.specific_student(student_number)
        student_information = []
        for i in range(len(self.labels)):
            if pd.isnull(data[self.labels[i]].iloc[0]) == False:
                student_information.append(data[self.labels[i]].iloc[0])
            else:
                student_information.append("not submit") 
        return student_information
                    
                    
    
    def weight(self):
        '''
        return list of wight for given labels
        '''
        rubric = self.data[self.data["Rubric"]=="Weight"]
        weight_value =[]
        for i in range(len(self.weight_label)):
             weight_value.append(rubric[self.weight_label[i]].iloc[0])
        return weight_value 
    
    
    def miss_activites(self,s_number):
        '''
        add the student miss activetes if he miss 

        '''
        data = self.submit_list(s_number)
      
        miss =[]
        for i in range(len(self.labels)):
            # if pd.isnull(data[self.labels[i]].iloc[0]) == False:
            if data[i] == "not submit":
                miss.append(self.labels[i])
        if len(miss) != 0:
            return miss
        else:
            return "all submit"
      
            
    def course_weight(self):
          '''
          A pie chart showing the weights of course activities
          then save as image to add in pdf file

          '''
          student_count = self.weight
          print(student_count)
          fig, ax = plt.subplots()
          ax.pie(student_count[:-1],radius=1, labels= self.labels[2:-1],autopct=lambda p:'{:.0f}%'.format(p))
          ax.set_title('weights of course activitiese')
          plt.savefig('./pie_chart.png')
          return './pie_chart.png'
          
          
    def student_grades(self,number):
        '''
        bar chart of the student grades in the course activates as a fraction of the total grade for each activity
        save the chart as image to add to pdf file
        '''
        student_count =  self.weight
        specific_data = self.specific_student(number)
        actual_count = specific_data.iloc[0].iloc[2:]
        x = np.arange(len(self.weight_label))
        width = 0.3
        fig, ax = plt.subplots()
        ax.bar(x, student_count, width, label='Full grade', color = "red")
        width = 0.2
        ax.bar(x, actual_count, width, label='your grade' , color = "blue")
        ax.set_ylabel('PPU Students')
        ax.set_title('Students per College')
        ax.set_xticks(x)
        ax.set_xticklabels(self.weight_label, rotation='vertical')
        ax.legend()
        fig.tight_layout()
        plt.savefig('./bar chart of the student grades.png')   
        return './bar chart of the student grades.png'
         
  
    def rank(self,number):
         '''
         A chart showing the student his/her rank within the whole class
         
         '''
         specific_data = self.specific_student(number)
         student_info = specific_data[self.labels[-1]].iloc[0]#total geades
         whole_data = np.sort(self.data[self.labels[-1]][1:])
         rank_number = np.where(whole_data  == student_info)#return array have the student rank number
         student_count= np.arange(len(self.names))
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
         return './rank.png'
  
    
class PDF(FPDF):           
    def header(self):
        self.set_font('Arial','', 26)
        self.set_fill_color(r= 192, g= 192, b = 192)
        self.cell(0, 10, 'Reporting Course Performance to Students', 1, 1, 'C',fill=True)
        self.cell(w=60, h=10, txt=" ",ln=1, align='C')
         
    def pdf_tabel(self,column1,column2):
        for i in range(len(column1)):
            self.set_font('Arial', 'B', 12)
            self.cell(w=30, h=5, txt=column1[i]+":", ln=0)
            self.set_font('Arial', '', 12)
            self.cell(w=35, h=5, txt=str(column2[i]),  ln=1)
           
    def titel(self,titel):
        self.set_font('Arial', 'B', 12)
        self.cell(w=10, h=20, txt= titel, ln=0) 
        
    def pdf_items(self,item):
        self.set_font('Arial', '', 12)
        self.cell(w=10, h=30, txt=str(item),ln=1)
                  
    def pdf_image(self,url):
        '''
        add image to pdf file

        '''
        self.image(url, x = 10, y = None, w = 130, h = 0, type = 'PNG')
          
        
   
class email:
    def __init__(self,email):
        self.receve_email = email
        self.smtp_port = 587
        self.smtp_server = "smtp.gmail.com"
        self.send_email = 'lanalolosh99@gmail.com'
        self.pswd =  "wexzaqbvxuteeogl" 
        self.subject = "email from lana sharabati using python"
    
    def send_emails(self,file_name):
        msg = MIMEMultipart()
        msg['From'] = self.send_email
        msg['To'] = self.receve_email
        msg['Subject'] = self.subject   
        filename = file_name
        attachment= open(filename, 'rb')  # r for read and b for binary
        attachment_package = MIMEBase('application', 'octet-stream')
        attachment_package.set_payload((attachment).read())
        encoders.encode_base64(attachment_package)
        attachment_package.add_header('Content-Disposition', "attachment; filename= " + filename)
        msg.attach(attachment_package)
        text = msg.as_string()
        TIE_server = smtplib.SMTP(self.smtp_server, self.smtp_port)
        TIE_server.starttls()
        TIE_server.login(self.send_email, self.pswd)
        TIE_server.sendmail(self.send_email, self.receve_email, text)
        # Close the port
        TIE_server.quit()
        
    
def main():
    
    data = pd.read_excel("grades.xlsx")#read data from excel file
    labels = ["Name","Email","HW1","HW2","First","Second","Final","Total Grade"]#take the main labels from the excel file
    info = student(data, labels)
    names = info.get_names()
    weight_chart = info.course_weight()
    
    info.set_single_emails("161015@ppu.edu.ps", 2)
    emails = info.get_emails()
    
    for i in range(len(names)):#generate pdf file for all student
        #Information for each student individually
        # student_information = students_data[students_data["Name"] == names[i]]
        pdf = PDF()
        pdf.add_page()
        #1 Student grades in each of the course activities
        pdf.pdf_tabel(labels,info.submit_list(i))
        #2 Course activities that the student miss or did not submit
        pdf.titel(" Course activities that the student miss or did not submit :")
        pdf.pdf_items(info.miss_activites(i))
        #3A pie chart showing the weights of course
        pdf.pdf_image( weight_chart)
        #4 A graphical representation (bar chart) of the student grades i
        pdf.pdf_image(info.student_grades(i))
        #5 A chart showing the student his/her rank within the whole class
        pdf.pdf_image(info.rank(i))
        #generate the pdf files the file name is the student name 
        pdf.output(names[i]+".pdf", 'F')
        send = email(emails[i])
        send.send_emails(names[i]+".pdf")
        
            
main()              