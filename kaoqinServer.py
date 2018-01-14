# coding=utf-8
from flask import Flask, request, flash,session, url_for, render_template,redirect
from  util.funLib import interfaceKaoqin

app = Flask(__name__)


@app.route('/',methods=['GET', 'POST'])
# @app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        print request.form['username']
        rao = interfaceKaoqin(userName=request.form['username'], passWord=request.form['password']);
        try:
            kaoqinList = rao.getKaoqinData()

            return render_template('kaoqin.html', kaoqinList=kaoqinList)
        except:
            return  "请检查账号密码，刷新页面再来一次"
    return render_template('login.html', error=error)
@app.route('/getKaoQinData', methods=['GET', 'POST'])
def getKaoQinData():
    print request.form['username']
    rao = interfaceKaoqin(userName=request.form['username'], passWord=request.form['password']);
    kaoqinList = rao.getKaoqinData()




if __name__ == '__main__':
    app.run(debug=True)
