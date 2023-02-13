from flask import Flask,session,render_template,request,redirect,url_for
from flask import Flask, render_template, request, send_from_directory
from werkzeug.utils import secure_filename as application
## import pandas as pd
import os
import pyodbc
import logging
import win32com.client

## for vscode, type python flaskPy.py in terminal to run at 5dum21 port
# 1) pytest tests/flaskTest.py to run test script
# python -m pytest tests/flaskTest.py if 1) doesn't work
# pytest -s prints console
# test comment for tags 2

app = Flask(__name__)

app.secret_key = 'DevOps_Oct2022_Team2_Assignment'
app.config['UPLOAD_FOLDER'] = 'uploads/'
ALLOWED_EXTENSIONS = {'xlsx'}

# Specifying the ODBC driver, server name, database, etc. directly

def checkDatabase():
    # Use this for local sql database
    """
    cnxn = pyodbc.connect(    
        'DRIVER={ODBC Driver 17 for SQL Server}; \
            SERVER=(localdb)\MSSQLLocalDB; \
                DATABASE=DevOps_TeamTwo_2022; \
                Trusted_Connection=yes;',autocommit = True)

    """
    # use this for github action collection database
    cnxn = pyodbc.connect(
        'DRIVER={ODBC Driver 17 for SQL Server}; \
            SERVER=(localdb)\MSSQLLocalDB; \
                DATABASE=tempdb; \
                Trusted_Connection=yes;',autocommit = True)
    
    
    # Create a cursor from the connection
    cursor = cnxn.cursor()

    table_List = ['Internship_Student_Data',
                'Internship_Company_Data',
                'Internship_Information_Data']

    toCreate = False

    for i in table_List:
        if cursor.tables(table=i).fetchone(): 
            print("yes table: ",i)
        else:
            print("Doesn't exist: ",i)
            toCreate = True                 

    createTableQuery =  "CREATE TABLE Internship_Student_Data(StudentID varchar(10) NOT NULL PRIMARY KEY CLUSTERED,Name varchar(255) NOT NULL,Preference varchar(255) NOT NULL,Status varchar(255) NOT NULL); \
                CREATE TABLE Internship_Company_Data (ID INT IDENTITY(1,1) NOT NULL PRIMARY KEY CLUSTERED,Company_Name varchar(255) NOT NULL,Job_Role varchar(255) NOT NULL,Company_Contact varchar(255) NOT NULL,Email varchar(255) NOT NULL); \
                CREATE TABLE Internship_Information_Data (StudentID varchar(10) not null primary key foreign key references Internship_Student_Data(StudentID),ID INT not null foreign key references Internship_Company_Data(ID));"          

    insertTableQuery = "INSERT INTO Internship_Student_Data VALUES ('S12345670A', 'Student 1','Software Development','Unassigned'); \
        INSERT INTO Internship_Student_Data VALUES ('S12345671B', 'Student 2','System Development','Unassigned'); \
            INSERT INTO Internship_Student_Data VALUES ('S12345672C', 'Student 3','Software Engineering, Development','Unassigned'); \
                INSERT INTO Internship_Student_Data VALUES ('S12345673D', 'Student 4','IOS and Android Development','Unassigned'); \
                    INSERT INTO Internship_Student_Data VALUES ('S12345674E', 'Student 5','Documents, QA Testing and Development','Unassigned'); \
                        INSERT INTO Internship_Student_Data VALUES ('S12345675F', 'Student 6','Software Engineering, Development','Unassigned'); \
                            INSERT INTO Internship_Student_Data VALUES ('S12345676G', 'Student 7','IOS and Android Development','Unassigned'); \
        INSERT INTO Internship_Company_Data (Company_Name, Job_Role, Company_Contact, Email) VALUES ('Company A', 'Software Developer','Mr A','devopsTeam2Company1');"
    
    if toCreate == True:
        
        createTableQuery = filter(None, createTableQuery.split(';'))
        insertTableQuery = filter(None, insertTableQuery.split(';'))    
        
        for i in createTableQuery:
            cursor.execute(i.strip() + ';')
        for j in insertTableQuery:
            cursor.execute(j.strip() + ';')    
                
    selectQuery = "SELECT * FROM Internship_Student_Data; \
        SELECT * FROM Internship_Company_Data; \
            SELECT * FROM Internship_Information_Data;" 
                
    selectQuery = filter(None, selectQuery.split(';'))

    studentList = []
    companyList = []
    informationList = []

    count = 0

    for i in selectQuery:
        cursor.execute(i.strip() + ';')
        
        if count == 0:
            count = count + 1
            records = cursor.fetchall()
            
            for row in records:
                studentList.append({"StudentID":row[0],
                                    "Name":row[1],
                                    "Preference":row[2],
                                    "Status":row[3]})            
        
        elif count == 1:
            count = count + 1
            records = cursor.fetchall()
    
            for row in records:
                companyList.append({"ID":row[0],
                                    "Company_Name":row[1],
                                    "Job_Role":row[2],
                                    "Company_Contact":row[3],
                                    "Email":row[4]})
                
        elif count == 2:
            count = count + 1                    
            records = cursor.fetchall() 

            for row in records:
                informationList.append({"StudentID":row[0],
                                    "ID":row[1]})
                            
    cnxn.close()
    
    count = 0
        
    return studentList, companyList, informationList
            
# Redirect http://localhost:5221/ to http://localhost:5221/main
@app.route("/")
def redirectToMain():
    return redirect(url_for("mainFile"))

# {{helloVar}} in index gets its value from here
@app.route("/Main")
def mainFile():
    helloVar = "Hello world"
    return render_template("index.html",helloVar=helloVar)

@app.route("/Match_Student", methods = ['GET','POST'])

def matchFile():
    
    #session.clear()
    
    if session.get('shown') == None:
        session['shown'] = 0
        
    elif session.get('update') == None:
        session['update'] = ""    

    elif session.get('updateNo') == None:
        session['updateNo'] = ""
            
    if request.method == 'GET':
        
        if session['shown'] == 0:
            session['update'] = ""
            session['updateNo'] = ""
        
        elif session['shown'] == 1:
            session['shown'] = 0
        
        studentList,companyList,informationList = checkDatabase()
        
        return render_template("Match_Student.html",
                           studentList=studentList,
                           companyList=companyList,
                           informationList=informationList)
        
    if request.method == 'POST':
        """
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server}; \
                SERVER=(localdb)\MSSQLLocalDB; \
                    DATABASE=DevOps_TeamTwo_2022; \
                        Trusted_Connection=yes;',autocommit = True)
           
        """
        # use this for github action collection database
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server}; \
                SERVER=(localdb)\MSSQLLocalDB; \
                    DATABASE=tempdb; \
                    Trusted_Connection=yes;',autocommit = True)
        
        
        studentList,companyList,informationList = checkDatabase()
        
        aList1 = request.form.getlist('companySelected[]')
        aList2 = request.form.getlist('assignmentSelected[]')
        aList3 = request.form.getlist('studentSelected[]')
        
        #app.logger.info('testing info log companySelected: ', aList1)
        
        cursor = cnxn.cursor()
        
        tableUpdatedOccured = False
        
        tempCountExecutes = 0
        
        a = []
        b = []
        d = []
        e = []
        
        for m in studentList:
            a.append([m.get(k) for k in ["StudentID"]])
            b.append([m.get(l) for l in ["Status"]])       
        
        for j in informationList:
            d.append([j.get(n) for n in ["StudentID"]])
            e.append([j.get(n) for n in ["ID"]])
            
        a = [item for sublist in a for item in sublist]
        b = [item for sublist in b for item in sublist]
        d = [item for sublist in d for item in sublist] 
        e = [str(item) for sublist in e for item in sublist]                   
        
        for i in range(len(aList1)):
            
            if aList1[i] != "Unassigned":
                
                found = False
                f = None
                
                #app.logger.info('d value here', d) 
                    
                if aList3[i] in d:
                    
                    found = True
                    f = d.index(aList3[i])
                    
                    if aList1[i] != e[f]: 
                        tableUpdatedOccured = True
                        tempCountExecutes = tempCountExecutes + 1                        
                        cursor.execute("UPDATE dbo.Internship_Information_Data SET ID = ? WHERE StudentID = ?", aList1[i], aList3[i])                        
                    
                    f = a.index(aList3[i])
                    f = b[f]
                    
                    if aList2[i] != f:
                        if aList2[i] == "Unassigned":
                            tableUpdatedOccured = True
                            tempCountExecutes = tempCountExecutes + 1                            
                            cursor.execute("UPDATE dbo.Internship_Student_Data SET Status = ? WHERE StudentID = ?", aList2[i], aList3[i])
                            cursor.execute("DELETE FROM dbo.Internship_Information_Data WHERE StudentID = ?", aList3[i])   
                        else:
                            tableUpdatedOccured = True
                            tempCountExecutes = tempCountExecutes + 1                                
                            cursor.execute("UPDATE dbo.Internship_Student_Data SET Status = ? WHERE StudentID = ?", aList2[i], aList3[i])        
                            
                if found == False:
                    if aList2[i] == "Unassigned":
                        aList2[i] = "Pending confirmation"
                        tableUpdatedOccured = True
                        tempCountExecutes = tempCountExecutes + 1
                        cursor.execute("UPDATE dbo.Internship_Student_Data SET Status = ? WHERE StudentID = ?", aList2[i], aList3[i])
                        cursor.execute("INSERT INTO dbo.Internship_Information_Data (StudentID,ID) VALUES (?,?)", aList3[i], aList1[i])
                    else:
                        tableUpdatedOccured = True
                        tempCountExecutes = tempCountExecutes + 1   
                        cursor.execute("UPDATE dbo.Internship_Student_Data SET Status = ? WHERE StudentID = ?", aList2[i], aList3[i])
                        cursor.execute("INSERT INTO dbo.Internship_Information_Data (StudentID,ID) VALUES (?,?)", aList3[i], aList1[i]) 
            
            elif aList1[i] == "Unassigned":
                for l in informationList:
                    for StudentID in l.keys():
                        if aList3[i] == l[StudentID]:
                            tableUpdatedOccured = True
                            tempCountExecutes = tempCountExecutes + 1
                            cursor.execute("UPDATE dbo.Internship_Student_Data SET Status = ? WHERE StudentID = ?", "Unassigned", aList3[i])
                            cursor.execute("DELETE FROM dbo.Internship_Information_Data WHERE StudentID = ?", aList3[i])                         
                               
        cnxn.close()
        
        if tableUpdatedOccured == False:
            session['updateNo'] = tempCountExecutes
            session['update'] = "tables updated"
            session['shown'] = 1
            
        elif tableUpdatedOccured == True:
            session['updateNo'] = tempCountExecutes
            session['update'] = "tables updated"
            session['shown'] = 1                
                    
        return redirect(url_for("matchFile")) 

@app.route("/Prepare_Email", methods = ['GET','POST'])
def prepareFile():
    
    #session.clear()
    
    if session.get('shown') == None:
        session['shown'] = 0
        
    elif session.get('update') == None:
        session['update'] = ""    

    elif session.get('updateNo') == None:
        session['updateNo'] = ""
            
    if request.method == 'GET':
        
        if session['shown'] == 0:
            session['update'] = ""
            session['updateNo'] = ""
        
        elif session['shown'] == 1:
            session['shown'] = 0
        
        studentList,companyList,informationList = checkDatabase()
        
        return render_template("Prepare_Email.html",
                           studentList=studentList,
                           companyList=companyList,
                           informationList=informationList)
        
    if request.method == 'POST':
        """
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server}; \
                SERVER=(localdb)\MSSQLLocalDB; \
                    DATABASE=DevOps_TeamTwo_2022; \
                        Trusted_Connection=yes;',autocommit = True)
           
        """
        # use this for github action collection database
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server}; \
                SERVER=(localdb)\MSSQLLocalDB; \
                    DATABASE=tempdb; \
                    Trusted_Connection=yes;',autocommit = True)
        
        
        studentList,companyList,informationList = checkDatabase()
        
        aList1 = request.form.getlist('companySelected[]')
        aList2 = request.form.getlist('assignmentSelected[]')
        aList3 = request.form.getlist('studentSelected[]')
        
        app.logger.info('testing info log companySelected: ', aList1)
        
      
        return redirect(url_for("prepareFile")) 


@app.route('/SendFile', methods=['POST']) 
def SendFile():

     #session.clear()
    
    if session.get('shown') == None:
        session['shown'] = 0
        
    elif session.get('update') == None:
        session['update'] = ""    

    elif session.get('updateNo') == None:
        session['updateNo'] = ""
            
    if request.method == 'GET':
        
        if session['shown'] == 0:
            session['update'] = ""
            session['updateNo'] = ""
        
        elif session['shown'] == 1:
            session['shown'] = 0
        
        studentList,companyList,informationList = checkDatabase()
        
        return render_template("SendFile.html",
                           studentList=studentList,
                           companyList=companyList,
                           informationList=informationList)
        
    if request.method == 'POST':
        """
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server}; \
                SERVER=(localdb)\MSSQLLocalDB; \
                    DATABASE=DevOps_TeamTwo_2022; \
                        Trusted_Connection=yes;',autocommit = True)
           
        """
        # use this for github action collection database
        cnxn = pyodbc.connect(
            'DRIVER={ODBC Driver 17 for SQL Server}; \
                SERVER=(localdb)\MSSQLLocalDB; \
                    DATABASE=tempdb; \
                    Trusted_Connection=yes;',autocommit = True)
        
        
        studentList,companyList,informationList = checkDatabase()
        
        aList1 = request.form.getlist('companySelected[]')
        aList2 = request.form.getlist('assignmentSelected[]')
        aList3 = request.form.getlist('studentSelected[]')
        
        app.logger.info('testing info log companySelected: ', aList1)
        outlook = win32com.client.Dispatch('outlook.application')
        mail = outlook.CreateItem(0)
        mail.To = 's10208093@connect.np.edu.sg'
        mail.Subject = 'Internship Response to Internship Request'
        mail.HTMLBody = '<h3>Dear <Company Contact></h3>'
        mail.Body = "Kindly find attached our students resume for the year semester Internship in response to your job description which you have submitted to us. We look forward to your favorable response and to working with your company for the upcoming internship period Internship Period."
       
        mail.Send()
        
        
        return redirect(url_for("SendFile")) 
       

@app.route("/settings", methods=["GET", "POST"])

def settings():
    if request.method == 'GET':
        # Code to retrieve current settings from the database
        current_settings = {}
        return render_template('settings.html', settings=current_settings)
    elif request.method == 'POST':
        # Code to update the database with the new values
        new_settings = request.form
        # update the database with the new_settings dictionary
        return redirect(url_for('index'))
    return render_template('settings.html')

@app.route('/')
def index():
    # Read the settings from database or file
    resume_directory = 'resume_dir'
    email_directory = 'email_dir'
    internship_period = '01/01/2021 to 31/12/2021'
    return render_template('indexsettings.html', resume_directory=resume_directory, email_directory=email_directory, internship_period=internship_period)

@app.route("/Upload_Data", methods=['POST', 'GET'])
def upload_data():
    if 'file' not in request.files:
        return render_template("Upload_data.html")
    file = request.files['student-file']
    df = pd.read_excel(file)

    # Connect to SQL Server database
    conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};' +
                          'SERVER=(localdb)\MSSQLLocalDB;' +
                          'DATABASE=DevOps_TeamTwo_2022;' +
                          'Trusted_Connection=yes;',
                          autocommit=True)
                
    cursor = conn.cursor()

    # Split data into Internship Student Data and Internship Company Data
    #student_data = df[df['Type'] == 'Student Data']
    #company_data = df[df['Type'] == 'Company Data']

    # Insert Internship Student Data into SQL Server
    for index, row in df.iterrows():
        query = f"INSERT INTO Internship_Student_Data (StudentId, StudentName, StudentPreference, Status) " \
                f"VALUES ('{row['StudentName']}', '{row['StudentID']}', '{row['StudentPreference']}', '{row['Status']}')"
        cursor.execute(query)

    # Insert Internship Company Data into SQL Server
    #for index, row in company_data.iterrows():
    #    query = f"INSERT INTO Internship_Company_Data (Company_Name, Job_Role, Company_Contact, Email) " \
    #            f"VALUES ('{row['Company_Name']}', '{row['Job_Role']}', '{row['Company_Contact']}', '{row['Email']})"
    #    cursor.execute(query)

    # Commit changes to the database
    conn.commit()

    return 'File uploaded and data stored in SQL Server database!'

if __name__ == '__main__':
    app.run(debug=True,port=5221,host="localhost")


