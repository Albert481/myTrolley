from flask import Flask, render_template, request, flash, redirect, url_for
from wtforms import Form, StringField, TextAreaField, RadioField, SelectField, validators
import firebase_admin
from firebase_admin import credentials, db, storage

cred = credentials.Certificate('cred/smarttrolley-c024a-firebase-adminsdk-y9xqv-d051733405.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smarttrolley-c024a.firebaseio.com/'
})

root = db.reference()

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scanner')
def scanner():
    trolleys = root.child('trolleys').get()
    form = ScannerForm(request.form)
    name = form.trolleyid.data
    for trolleyid in trolleys:
        eachtrolley = trolleys[trolleyid]

        if eachtrolley['status'] == 'A':
            if name == eachtrolley:
                flash('Trolley unlocked', 'success')
            else:
                flash('Trolley ID not in database', 'danger')

        elif eachtrolley['status'] == 'B':
            flash('Trolley needs repair', 'danger')

    return render_template('scanner.html')

class ScannerForm(Form):
    trolleyid = StringField('Please enter Trolley ID:', [validators.Length(min=1, max=150), validators.number_range(min=0000, max=9999), validators.DataRequired()])

@app.route('/ourproduct')
def ourproduct():
    return render_template('ourproduct.html')

@app.route('/popularitem')
def popularitem():
    return render_template('popularitem.html')

@app.route('/healthyrecipe')
def healthyrecipe():
    return render_template('healthyrecipe.html')

@app.route('/recipe1')
def recipe1():
    return render_template('recipe_orange_apple_pear_juice.html')

@app.route('/recipe2')
def recipe2():
    return render_template('recipe_creamy_banana_pudding.html')

@app.route('/recipe3')
def recipe3():
    return render_template('recipe_lettuce_cumber_tomato_salad.html')

@app.route('/recipe4')
def recipe4():
    return render_template('recipe_crunchy_carrot_apple_salad.html')

@app.route('/healthevent')
def healthevent():
    return render_template('healthevent.html')

@app.route('/search')
def search():
    return render_template('search.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/modifyuser')
def modifyuser():
    return render_template('modifyuser.html')

@app.route('/credit')
def creditpointsystem():
    return render_template('creditpointsystem.html')

@app.route('/reward')
def reward():
    return render_template('rewardsystem.html')

@app.route('/help')
def help():
    return render_template('help.html')

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run()

