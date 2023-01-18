from flask import Flask,render_template,redirect,url_for
import pyodbc

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
# use this for github action collection database
cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server}; \
        SERVER=(localdb)\MSSQLLocalDB; \
            DATABASE=tempdb; \
            UID=sa; \
            PWD=dbatools.I0;',autocommit = True)
"""

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

createTableQuery =  "CREATE TABLE Internship_Student_Data(StudentID varchar(10) NOT NULL PRIMARY KEY CLUSTERED,Name varchar(255) NOT NULL,Preference varchar(255) NOT NULL,Status varchar(11) NOT NULL); \
            CREATE TABLE Internship_Company_Data (ID INT IDENTITY(1,1) NOT NULL PRIMARY KEY CLUSTERED,Company_Name varchar(255) NOT NULL,Job_Role varchar(255) NOT NULL,Company_Contact varchar(255) NOT NULL,Email varchar(255) NOT NULL); \
            CREATE TABLE Internship_Information_Data (StudentID varchar(10) not null primary key foreign key references Internship_Student_Data(StudentID),ID INT not null foreign key references Internship_Company_Data(ID));"          

if toCreate == True:
    
    createTableQuery = filter(None, createTableQuery.split(';'))  
      
    for i in createTableQuery:
        my_data_2 = cursor.execute(i.strip() + ';')    

selectQuery = "SELECT * FROM Internship_Student_Data; \
    SELECT * FROM Internship_Company_Data; \
        SELECT * FROM Internship_Information_Data;" 
               
selectQuery = filter(None, selectQuery.split(';'))

studentList = []
companyList = []
informationList = []

for i in selectQuery:
    cursor.execute(i.strip() + ';')
    if "Internship_Student_Data" in i:
        records = cursor.fetchall()
        
        for row in records:
            studentList.append({"StudentID":row[0],
                                "Name":row[1],
                                "Preference":row[2],
                                "Status":row[3]})
        
    elif "Internship_Company_Data":
        records = cursor.fetchall()
 
        for row in records:
            companyList.append({"ID":row[0],
                                "Company_Name":row[1],
                                "Company_Contact":row[2],
                                "Status":row[3],
                                "Email":row[4]})
                    
    elif "Internship_Information_Data":
        records = cursor.fetchall() 

        for row in records:
            informationList.append({"StudentID":row[0],
                                "ID":row[1]})

cnxn.close()

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
    return render_template("Match_Student.html",
                           studentList=studentList,
                           companyList=companyList,
                           informationList=informationList)

if __name__ == '__main__':
    app.run(debug=True,port=5221,host="localhost")
