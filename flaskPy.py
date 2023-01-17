from flask import Flask,render_template,redirect,url_for
import pyodbc

## for vscode, type python flaskPy.py in terminal to run at 5221 port
# 1) pytest tests/flaskTest.py to run test script
# python -m pytest tests/flaskTest.py if 1) doesn't work
# pytest -s prints console

app = Flask(__name__)

# Specifying the ODBC driver, server name, database, etc. directly
cnxn = pyodbc.connect(
    'DRIVER={ODBC Driver 17 for SQL Server}; \
        SERVER=(localdb)\MSSQLLocalDB; \
            DATABASE=DevOps_TeamTwo_2022; \
            Trusted_Connection=yes;')

# Create a cursor from the connection
cursor = cnxn.cursor()


s = "SELECT StudentID, Name,Preference, \
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
