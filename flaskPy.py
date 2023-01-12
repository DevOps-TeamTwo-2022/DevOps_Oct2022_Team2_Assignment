from flask import Flask,render_template,redirect,url_for

# for vscode, type python flaskPy.py in terminal to run at 5221 port

app = Flask(__name__)

@app.route("/")
def redirectToMain():
    return redirect(url_for("hello_world"))

@app.route("/main")
def hello_world():
    helloVar = "Hello world"
    return render_template("index.html",helloVar=helloVar)


if __name__ == '__main__':
    app.run(debug=True,port=5221,host="localhost")