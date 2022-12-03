from flask import Flask, request, render_template, g, flash, abort, url_for, redirect, make_response,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ad.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'zxcv124'
db = SQLAlchemy(app)


class DBF(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tm = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return 'DBF %r' % self.id


@app.route('/login', methods=['POST', 'GET'])
def login():  # put application's code here
    if not session:
        if request.method == 'POST':
            session['username'] = request.form['username']
            return redirect(url_for('get_ad'))
        else:
            return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
        '''
    else:
        return redirect(url_for('get_ad'))


@app.route('/')
def redirect_all():
    return redirect(url_for('login'))


@app.route('/all', methods=['POST', 'GET'])
def get_ad():  # put application's code here
    """Вызов объявления"""
    gad = DBF.query.order_by(DBF.tm.desc()).all()  # не удалять
    return render_template("all.html", gad=gad)  # е удалять


@app.route('/all/<int:id>')
def detail(id):  # put application's code here
    """подробный вывод объявления"""
    gad_detail = DBF.query.get(id)
    return render_template("ad_detail.html", gad_detail=gad_detail)


@app.route('/all/<int:id>/delete')
def del_ad(id):  # put application's code here
    """Удаление объявлений"""
    gad_detail = DBF.query.get_or_404(id)
    gad_detail.username = session['username']
    if gad_detail.username == session['username']:
        return "Возникла ошибка это не ваше объявление"
    else:
        try:
            db.session.delete(gad_detail)
            db.session.commit()
            return redirect('/all')
        except:
            return "Возникла ошибка"


@app.route('/all/<int:id>/update', methods=['POST', 'GET'])
def update_ad(id):  # put application's code here
    """Изменение объявления"""
    gad_detail = DBF.query.get(id)
    if request.method == "POST":
        gad_detail.username = session['username']
        gad_detail.title = request.form['title']
        gad_detail.content = request.form['content']
        try:
            db.session.commit()
            return redirect('/all')
        except:
            return "Возникла ошибка"
    else:
        if gad_detail.username != session['username']:
            return "Возникла ошибка это не ваше объявление"
        else:
            return render_template("update_ad.html", gad_detail=gad_detail)


@app.route('/create_ad', methods=['POST', 'GET'])
def create_ad():  # put application's code here
    """Создание объявления"""
    if request.method == "POST":
        username = session['username']
        title = request.form['title']
        content = request.form['content']


        ad = DBF(title=title, content=content, username=username)

        try:
            db.session.add(ad)
            db.session.commit()
            return redirect('/all')
        except:
            return "Возникла ошибка"
    else:
        return render_template("create_ad.html")


if __name__ == '__main__':
    app.run()
