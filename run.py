from flask import Flask, render_template, request, flash, redirect, url_for
from wtforms import Form, StringField, TextAreaField, RadioField, BooleanField, validators, SelectMultipleField, DateTimeField, PasswordField
import firebase_admin
from firebase_admin import credentials, db, storage
import scanner as scan

cred = credentials.Certificate('cred/smarttrolley-c024a-firebase-adminsdk-y9xqv-d051733405.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smarttrolley-c024a.firebaseio.com/'
})

root = db.reference()

troll = db.reference('trolleys')

app = Flask(__name__)
app.config['SECRET KEY'] = 'secret123'

@app.route('/')
def home():
    return render_template('index.html')

class RequiredIf(object):

    def __init__(self, *args, **kwargs):
        self.conditions = kwargs

    def __call__(self, form, field):
        for name, data in self.conditions.items():
            if name not in form._fields:
                validators.Optional()(field)
            else:
                condition_field = form._fields.get(name)
                if condition_field.data == data:
                    validators.DataRequired().__call__(form, field)
                else:
                    validators.Optional().__call__(form, field)

class ScannerForm(Form):
    #Enter Trolley ID
    trolleyid = StringField('Please enter Trolley ID:', [validators.Length(min=1, max=150), validators.number_range(min=0000, max=9999), validators.DataRequired()])
    #Report
    reporttype = RadioField('Report Type', choices=[('faulty', 'Faulty Trolley'), ('misuse', 'Trolley Misuse')], default='faulty')
    name = StringField('Please enter Trolley ID:', [validators.Length(min=1, max=150), validators.number_range(min=0000, max=9999), validators.DataRequired()])
    faulty = SelectMultipleField('Select', [validators.DataRequired(), RequiredIf(reporttype='faulty')], choices=[('', 'Select'), ('DW', 'Damaged Wheel'), ('DL', 'Damaged Lock'), ('DQ', 'Damaged QR')], default='')
    location = StringField('Enter location:', [validators.DataRequired(), RequiredIf(reporttype='misuse')])
    comment = TextAreaField('Additional comments:')

@app.route('/scanner', methods=['GET','POST'])
def scanner():
    trolleys = troll.get()
    form = ScannerForm(request.form)
    calledname = form.trolleyid.data
    found = False
    if request.method == 'POST':
        #If Enter Trolley ID has data:
        if form.trolleyid.data != '':
            #Iterate through the database trolleys
            for trolleyid in trolleys.items():
                if trolleyid[1]['name'] == calledname:
                    #If status is empty in database
                    if trolleyid[1]['status'] == '':
                        flash('Trolley unlocked', 'success')
                        print('Trolley unlocked')
                        found = True
                        break
                    #If trolley has been reported, and flagged by 3 users or more
                    elif trolleyid[1]['status'] != '' and trolleyid[1]['flag_count'] >=3:
                        flash('Trolley needs repair', 'danger')
                        print('Trolley needs repair, please find another trolley')
                        found = True
                        break
                    #If trolley has been reported once, twice.
                    elif trolleyid[1]['status'] != '':
                        flash('Trolley may need repair', 'danger')
                        print('Trolley may need repair, trolley unlocked, if not working, please report')
                        found = True
                        break
            #If trolley is not in database
            if found == False:
                flash('Trolley ID not in database', 'danger')
                print('Trolley ID not in database')

        #If report button has data:
        elif form.name.data != '':
            name = form.name.data
            fault = form.faulty.data
            comment = form.comment.data
            location = form.location.data
            for trolleyid in trolleys.items():
                if trolleyid[1]['name'] == name:
                    flag_count = (trolleyid[1]['flag_count'])
                    flag_count += 1
                    reportfaulty = scan.Reports(fault, comment, flag_count, location)
                    report_db = troll.child(trolleyid[0])
                    report_db.update({
                    'flag_count': reportfaulty.get_count(),
                    'status': reportfaulty.get_fault(),
                    'comments': reportfaulty.get_comment(),
                    'location': reportfaulty.get_location()
                    })
            flash('You have successfully filed a report', 'success')
            print('Successully reported')
            return redirect(url_for('scanner'))
        else:
            print('What to do')
            pass
    return render_template('scanner.html', form=form)

@app.route('/admin', methods=['GET','POST'])
def admin():
    namelist = []
    trolleys = troll.get()
    form = ScannerForm(request.form)
    if request.method == 'POST':
        for trolleyid in trolleys.items():
            number = int(trolleyid[1]['name'])
            namelist.append(number)
        namelist.sort()
        maxname = int(namelist[-1:][0])
        maxname += 1
        maxname = str(maxname)
        print(maxname)
        report_db = root.child('trolleys')
        report_db.push({
            'name': maxname,
            'flag_count': '0',
            'status': '',
            'comments': '',
            'location': ''
        })
    return render_template('admin.html', form=form)

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

class Signupform(Form):
    username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    birthday = DateTimeField('Your Birthday', format='%d/%m/%y')
    password = PasswordField()
    accept_rules = BooleanField('I accept the site rules', [validators.InputRequired()])

    def register(request):
        form = Signupform(request.POST)
        if request.method == 'POST' and form.validate():
            user = Signupform()
            user.username = form.username.data
            user.email = form.email.data
            user.save()
            redirect('register')
        return render_template('modifyuser.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

class LoginForm(Form):
    username = StringField('username')
    password = PasswordField('password')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/modifyuser')
def modifyuser():
    return render_template('modifyuser.html')

class ProfileForm():

    def edit_profile(request):
        user = request.current_user
        form = ProfileForm(request.POST, user)
        if request.method == 'POST' and form.validate():
            form.populate_obj(user)
            user.save()
            redirect('edit_profile')
        return render_template('edit_profile.html', form=form)

@app.route('/credit')
def creditpointsystem():
    return render_template('creditpointsystem.html')

@app.route('/reward')
def reward():
    return render_template('rewardsystem.html')

@app.route('/help')
def help():
    return render_template('help.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/email')
def email():
    return render_template('email.html')

@app.route('/feedback')
def feedback():
    return render_template('feedback.html')

if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(debug=True)

