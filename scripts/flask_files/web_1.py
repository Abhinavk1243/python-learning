from flask import Flask, redirect, url_for, render_template, request
from werkzeug.utils import redirect
app = Flask(__name__)

@app.route('/success/<name>')
def success(name):
       return 'welcome %s' % name


@app.route('/')
def index():
   return render_template('login.html')
"""
@app.route('/login',methods = ['POST', 'GET']) 
def login(): 
   if request.method == 'POST' and request.form['uname'] == 'admin' :
      return redirect(url_for('success'))
   else:
      return redirect(url_for('index'))


""" 

@app.route('/login',methods=["POST"])
def login_form():
    if request.method==["POST"]:
        user=request.form["nm"]
        return redirect(url_for('success',name = user))

    else:
        user = request.args.get('nm')
        return redirect(url_for('success',name = user))

"""@app.route('/success/<name>')
def success(name):
   return "logged in successfully : %s" %name"""
   

if __name__ == '__main__':
   app.run(debug = True)
