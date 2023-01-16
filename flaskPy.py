from flask import Flask,render_template,redirect,url_for

## for vscode, type python flaskPy.py in terminal to run at 5221 port
# 1) pytest tests/flaskTest.py to run test script
# python -m pytest tests/flaskTest.py if 1) doesn't work
# pytest -s prints console

app = Flask(__name__)

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
    return render_template("Match_Student.html",helloVar_Match=helloVar_Match)


if __name__ == '__main__':
    app.run(debug=True,port=5221,host="localhost")