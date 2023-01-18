from flask import Flask,render_template,redirect,url_for
import pyodbc
import re

## for vscode, type python flaskPy.py in terminal to run at 5221 port
# 1) pytest tests/flaskTest.py to run test script
# python -m pytest tests/flaskTest.py if 1) doesn't work
# pytest -s prints console

app = Flask(__name__)

# Specifying the ODBC driver, server name, database, etc. directly


# Use this for local sql database

cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server}; \
        SERVER=(localdb)\MSSQLLocalDB; \
            DATABASE=DevOps_TeamTwo_2022; \
            Trusted_Connection=yes;',autocommit = True)

"""
# IMPORTANT! use this for github action container database
cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server}; \
        SERVER=(localdb)\MSSQLLocalDB; \
            DATABASE=tempdb; \
            UID=sa; \
            PWD=dbatools.I0;',autocommit = True)
"""

# Create a cursor from the connection
cursor = cnxn.cursor()

# If table does not exist in database, store in toCreate
# Then create the table later on
table_List = ['Internship_Student_Data','Internship_Company_Data','Internship_Information_Data']

toCreate = []

for i in table_List:
    if cursor.tables(table=i).fetchone(): 
        print("Tables that exists: ",i)
    else:
        print("Tables that don't exist: ",i)
        toCreate.append(i)      

s = "SELECT StudentID, Name,Preference, \
    Status FROM Internship_Student_Data; \
        SELECT ID, Company_Name,Job_Role \
            FROM Internship_Company_Data; \
            SELECT StudentID, ID \
            FROM Internship_Information_Data;"

# FOR LOCAL USE! DO NOT DELETE! START
        
for i in toCreate:
    if i == "Internship_Student_Data":
        s = "CREATE TABLE Internship_Student_Data(StudentID varchar(10) NOT NULL PRIMARY KEY CLUSTERED,Name varchar(255) NOT NULL,Preference varchar(255) NOT NULL,Status varchar(11) NOT NULL); \
            CREATE TABLE Internship_Company_Data (ID INT IDENTITY(1,1) NOT NULL PRIMARY KEY CLUSTERED,Company_Name varchar(255) NOT NULL,Job_Role varchar(255) NOT NULL,Company_Contact varchar(255) NOT NULL,Email varchar(255) NOT NULL); \
            CREATE TABLE Internship_Information_Data (StudentID varchar(10) not null primary key foreign key references Internship_Student_Data(StudentID),ID INT not null foreign key references Internship_Company_Data(ID)); \
            INSERT INTO Internship_Student_Data VALUES ('S12345670A', 'Student 1','Software Development','Unassigned'); \
            INSERT INTO Internship_Student_Data VALUES ('S12345671B', 'Student 2','System Development','Unassigned'); \
            INSERT INTO Internship_Company_Data (Company_Name, Job_Role, Company_Contact, Email) VALUES ('Company A', 'Software Developer','Mr A','devopsTeam2Company1'); \
            INSERT INTO Internship_Information_Data VALUES ('S12345670A', 1); \
            SELECT StudentID, Name,Preference, \
            Status FROM Internship_Student_Data; \
            SELECT ID, Company_Name,Job_Role \
            FROM Internship_Company_Data; \
            SELECT StudentID, ID \
            FROM Internship_Information_Data;"  

# FOR LOCAL USE! DO NOT DELETE! END

# For github action container use DO NOT DELETE
"""
for i in toCreate:
    if i == "Internship_Student_Data":
        s = "CREATE TABLE Internship_Student_Data(StudentID varchar(10) NOT NULL PRIMARY KEY CLUSTERED,Name varchar(255) NOT NULL,Preference varchar(255) NOT NULL,Status varchar(11) NOT NULL); \
            CREATE TABLE Internship_Company_Data (ID INT IDENTITY(1,1) NOT NULL PRIMARY KEY CLUSTERED,Company_Name varchar(255) NOT NULL,Job_Role varchar(255) NOT NULL,Company_Contact varchar(255) NOT NULL,Email varchar(255) NOT NULL); \
            CREATE TABLE Internship_Information_Data (StudentID varchar(10) not null primary key foreign key references Internship_Student_Data(StudentID),ID INT not null foreign key references Internship_Company_Data(ID)); \
            SELECT StudentID, Name,Preference, \
            Status FROM Internship_Student_Data; \
            SELECT ID, Company_Name,Job_Role \
            FROM Internship_Company_Data;" 
"""  
# For github action container use DO NOT DELETE  
    
s = filter(None, s.split(';'))

studentList = []
companyList = []
informationList = []

def addToList(row):
    tempStr = str(row)
    newTempStr = re.sub('[^.,a-zA-Z0-9 \n\.]', '', tempStr)
    
    tempList = newTempStr.split(',')
       
    return tempList

for i in s:
    cursor.execute(i.strip() + ';')
    if "Internship_Student_Data" in i:
        for row in cursor:
            studentList.append(addToList(row))
            
    elif "Internship_Company_Data" in i:
        for row in cursor:
            companyList.append(addToList(row))
            
    elif "Internship_Information_Data" in i:
        for row in cursor:
            informationList.append(addToList(row))

print("student: ",studentList)
print("company: ",companyList)
print("information: ",informationList)

# Redirect http://localhost:5221/ to http://localhost:5221/main
@app.route("/")
def redirectToMain():
    return redirect(url_for("mainFile"))

# {{helloVar}} in index gets its value from here
@app.route("/Main")
def mainFile():
    helloVar = "Hello world"
    return render_template("index.html",helloVar=helloVar)

@app.route("/Match_Student")
def matchFile():
    helloVar_Match = "Hello world Match"
    return render_template("Match_Student.html",
                           helloVar_Match=helloVar_Match)

if __name__ == '__main__':
    app.run(debug=True,port=5221,host="localhost")
