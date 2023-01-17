from flask import Flask,render_template,redirect,url_for
import pyodbc

## for vscode, type python flaskPy.py in terminal to run at 5221 port
# 1) pytest tests/flaskTest.py to run test script
# python -m pytest tests/flaskTest.py if 1) doesn't work
# pytest -s prints console

app = Flask(__name__)

# Specifying the ODBC driver, server name, database, etc. directly


# Use this for local sql database
"""
cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server}; \
        SERVER=(localdb)\MSSQLLocalDB; \
            DATABASE=DevOps_TeamTwo_2022; \
            Trusted_Connection=yes;')
"""
# use this for github action collection database
cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server}; \
        SERVER=(localdb)\MSSQLLocalDB; \
            DATABASE=tempdb; \
            UID=sa; \
            PWD=dbatools.I0;')

# Create a cursor from the connection
cursor = cnxn.cursor()

table_List = ['Internship_Student_Data','Internship_Company_Data','Internship_Information_Data']

toCreate = []

for i in table_List:
    if cursor.tables(table=i).fetchone(): 
        print("yes table: ",i)
    else:
        toCreate.append(i)      

s = "SELECT StudentID, Name,Preference, \
    Status FROM Internship_Student_Data; \
        SELECT ID, Company_Name,Job_Role \
            FROM Internship_Company_Data;"

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
s = "SELECT StudentID, Name,Preference, \
    Status FROM Internship_Student_Data;"  
""" 
           
s = filter(None, s.split(';'))

for i in s:
    cursor.execute(i.strip() + ';')
    for row in cursor:
        print(row)

#cursor.execute('SELECT * FROM Internship_Student_Data')
#cursor_student.execute('SELECT StudentID, Name,Preference, \
#    Status FROM Internship_Student_Data')

#cursor_company.execute('SELECT ID, Company_Name,Job_Role, \
#    Status FROM Internship_Company_Data')


#for row in cursor_student:
#    print(row)

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
