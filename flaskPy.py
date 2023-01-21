from flask import Flask,session,render_template,request,redirect,url_for
import pyodbc
import logging

## for vscode, type python flaskPy.py in terminal to run at 5221 port
# 1) pytest tests/flaskTest.py to run test script
# python -m pytest tests/flaskTest.py if 1) doesn't work
# pytest -s prints console
# test comment for tags 2

app = Flask(__name__)

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
                UID=sa; \
                PWD=dbatools.I0;',autocommit = True)

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
    if request.method == 'GET':
        
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
                    UID=sa; \
                    PWD=dbatools.I0;',autocommit = True)

        
        studentList,companyList,informationList = checkDatabase()
        
        aList1 = request.form.getlist('companySelected[]')
        aList2 = request.form.getlist('assignmentSelected[]')
        aList3 = request.form.getlist('studentSelected[]')
        
        app.logger.info('testing info log companySelected: ', aList1)
        app.logger.info('testing info log assignmentSelected: ', aList2)
        app.logger.info('testing info log studentSelected: ', aList3)
        
        cursor = cnxn.cursor()
        
        for i in range(len(aList1)):
            
            if aList1[i] != "Unassigned":
                
                found = False

                for j in informationList:
                    for StudentID in j.keys():
                        if aList3[i] == j[StudentID]:
                            found = True
                            for k in studentList:
                                for StudentID in k.keys():
                                    if aList3[i] == k[StudentID]:
                                        cursor.execute("UPDATE dbo.Internship_Student_Data SET Status = ? WHERE StudentID = ?", aList2[i], aList3[i])   
                
                if found == False:
                    if aList2[i] == "Unassigned":
                        app.logger.info('HOW MANY EXECUTIONS:')
                        aList2[i] = "Pending confirmation"
                        cursor.execute("UPDATE dbo.Internship_Student_Data SET Status = ? WHERE StudentID = ?", aList2[i], aList3[i])
                        cursor.execute("INSERT INTO dbo.Internship_Information_Data (StudentID,ID) VALUES (?,?)", aList3[i], aList1[i])
                    else:
                        app.logger.info('HOW MANY EXECUTIONS else:')   
                        cursor.execute("UPDATE dbo.Internship_Student_Data SET Status = ? WHERE StudentID = ?", aList2[i], aList3[i])
                        cursor.execute("INSERT INTO dbo.Internship_Information_Data (StudentID,ID) VALUES (?,?)", aList3[i], aList1[i]) 
            
            elif aList1[i] == "Unassigned":
                app.logger.info('testing info log: ', "step1")
                for l in informationList:
                    for StudentID in l.keys():
                        if aList3[i] == l[StudentID]:
                            cursor.execute("UPDATE dbo.Internship_Student_Data SET Status = ? WHERE StudentID = ?", "Unassigned", aList3[i])
                            cursor.execute("DELETE FROM dbo.Internship_Information_Data WHERE StudentID = ?", aList3[i])                         
                               
        cnxn.close()
                        
        return redirect(url_for("matchFile")) 
    
if __name__ == '__main__':
    app.run(debug=True,port=5221,host="localhost")
      