from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, SelectMultipleField, StringField, PasswordField, validators, RadioField, SelectField, \
    ValidationError, FileField, SubmitField, TextAreaField, DateField
import firebase_admin
from firebase_admin import credentials, db, storage
import signup as sp
import trolleys as tr
import event as ev
import recipe as recs
import popularitem as pop
import product as prodt
import userFeedback as uf

# import user_comment as co

cred = credentials.Certificate('cred/smarttrolley-c024a-firebase-adminsdk-y9xqv-d051733405.json')
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://smarttrolley-c024a.firebaseio.com/'
})

root = db.reference()

troll = db.reference('trolleys')
events = db.reference('events')
popitem = db.reference('popularitems')
recipes = db.reference('recipes')
pdt = db.reference('products')
pdt_fruit = db.reference('fruits')
pdt_veg = db.reference('vegetables')

user_ref = db.reference('userbase')

email_email = db.reference('email')

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
    # Enter Trolley ID
    trolleyid = StringField('Please enter Trolley ID:', [validators.Length(min=4, max=4), validators.DataRequired()])
    # Report
    reporttype = RadioField('Report Type', choices=[('faulty', 'Faulty Trolley'), ('misuse', 'Trolley Misuse')],
                            default='faulty')
    name = StringField('Please enter Trolley ID:', [validators.Length(min=4, max=4), validators.DataRequired()])
    faulty = SelectMultipleField('Select', [validators.DataRequired(), RequiredIf(reporttype='faulty')],
                                 choices=[('', 'Select'), ('DW', 'Damaged Wheel'), ('DL', 'Damaged Lock'),
                                          ('DQ', 'Damaged QR')], default='')
    location = StringField('Enter location:', [validators.DataRequired(), RequiredIf(reporttype='misuse')])
    comments = TextAreaField('Additional comments:')
    unlocksubmit = SubmitField('Submit')

class ReportForm(Form):
    # Enter Trolley ID
    trolleyid = StringField('Please enter Trolley ID:', [validators.Length(min=4, max=4), validators.DataRequired()])
    # Report
    reporttype = RadioField('Report Type', choices=[('faulty', 'Faulty Trolley'), ('misuse', 'Trolley Misuse')],
                            default='faulty')
    name = StringField('Please enter Trolley ID:', [validators.Length(min=4, max=4), validators.DataRequired()])
    faulty = SelectMultipleField('Select', [validators.DataRequired(), RequiredIf(reporttype='faulty')],
                                 choices=[('', 'Select'), ('DW', 'Damaged Wheel'), ('DL', 'Damaged Lock'),
                                          ('DQ', 'Damaged QR')], default='')
    location = StringField('Enter location:', [validators.DataRequired(), RequiredIf(reporttype='misuse')])
    comments = TextAreaField('Additional comments:')
    reportsubmit = SubmitField('Submit')


@app.route('/scanner', methods=['GET', 'POST'])
def scanner():
    trolleys = troll.get()
    form = ScannerForm(request.form)
    reportform = ReportForm(request.form)
    calledname = form.trolleyid.data
    found = False
    if request.method == 'POST':
        # If Enter Trolley ID has data:
        if request.form['action'] == 'Unlock':
            # Iterate through the database trolleys
            for trolleyid in trolleys.items():
                if trolleyid[1]['name'] == calledname:
                    # If status is empty in database
                    if trolleyid[1]['status'] == '':
                        flash('Trolley unlocked!', 'success')
                        found = True
                        break
                    # If trolley has been reported, and flagged by 3 users or more
                    elif trolleyid[1]['status'] != '' and trolleyid[1]['flag_count'] >= 3:
                        flash('Trolley needs repair, please find another trolley', 'danger')
                        found = True
                        break
                    # If trolley has been reported once, twice.
                    elif trolleyid[1]['status'] != '':
                        flash('Trolley unlocked! If faulty, please report!', 'success')
                        found = True
                        break
            # If trolley is not in database
            if found == False:
                flash('Trolley ID not in database', 'danger')

        # If report button has data:
        elif request.form['action'] == 'Submit':
            name = reportform.trolleyid.data
            reporttype = reportform.reporttype.data
            fault = reportform.faulty.data
            comments = reportform.comments.data
            location = reportform.location.data
            valid = False
            for trolleyid in trolleys.items():
                if trolleyid[1]['name'] == name:
                    if reporttype == 'faulty':
                        flag_count = int(trolleyid[1]['flag_count'])
                        flag_count += 1
                        reportfaulty = tr.ReportF(fault, flag_count, comments)
                        report_db = troll.child(trolleyid[0])
                        report_db.update({
                            'flag_count': reportfaulty.get_count(),
                            'status': reportfaulty.get_fault(),
                            'comments': reportfaulty.get_comments(),
                        })
                        flash('Success: Trolley fault reported', 'success')
                        valid = True
                    if reporttype == 'misuse':
                        reportloc = tr.ReportL(location, comments)
                        report_db = troll.child(trolleyid[0])
                        report_db.update({
                            'location': reportloc.get_location(),
                            'comments': reportloc.get_comments()
                        })
                        flash('Report Success: Trolley misuse reported', 'success')
                        valid = True
            if valid == False:
                flash('Report Failed: Trolley ID does not exist', 'danger')
            return redirect(url_for('scanner'))
        else:
            flash('Do not leave blanks', 'danger')
    return render_template('scanner.html', form=form, reportform=reportform)


class AdminForm(Form):
    trolleynumbers = StringField('Enter number of new trolleys to add to database:',
                                 [validators.NumberRange(min=1, max=2)])
    trolleyid = StringField('Please enter Trolley ID:',
                            [validators.Length(min=1, max=4), validators.number_range(min=1000, max=9999),
                             validators.DataRequired()])
    password = PasswordField('Enter secret code:')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    trolleys = troll.get()
    form = AdminForm(request.form)
    foundlist = []
    attentionlist = []
    trolleynumbers = form.trolleynumbers.data
    calledname = form.trolleyid.data
    tnames = 0
    tfaults = 0
    tmisused = 0

    # Statistics function
    for trolleyid in trolleys.items():
        tnames += 1
        if int(trolleyid[1]['flag_count']) >= 3:
            tfaults += 1
        if trolleyid[1]['location'] != "":
            tmisused += 1

    # Attention function
    for trolleyid in trolleys.items():
        if int(trolleyid[1]['flag_count']) >= 3:
            attention = tr.FindTrolley(trolleyid[1]['name'], trolleyid[1]['status'], trolleyid[1]['flag_count'],
                                       trolleyid[1]['location'], trolleyid[1]['comments'])
            attentionlist.append(attention)

    if request.method == 'POST':
        # Add New
        if form.trolleynumbers.data != '':
            namelist = []
            for i in range(int(trolleynumbers)):
                for trolleyid in trolleys.items():
                    number = int(trolleyid[1]['name'])
                    namelist.append(number)
                namelist.sort()
                maxname = int(namelist[-1:][0])
                maxname += 1
                namelist.append(maxname)
                maxname = str(maxname)
                newtroll_db = root.child('trolleys')
                newtroll_db.push({
                    'name': maxname,
                    'flag_count': '0',
                    'status': '',
                    'comments': '',
                    'location': ''
                })
            flash('Add Sucesss: New Trolley ID(s) has been added', 'success')

        # Find Trolley
        if form.trolleyid.data != '':
            found = False
            for trolleyid in trolleys.items():
                if trolleyid[1]['name'] == calledname:
                    findtrolley = tr.FindTrolley(trolleyid[1]['name'], trolleyid[1]['status'],
                                                 trolleyid[1]['flag_count'], trolleyid[1]['location'],
                                                 trolleyid[1]['comments'])
                    foundlist.append(findtrolley)
                    found = True
            if found == False:
                flash('Trolley does not exist in database', 'danger')

    else:
        print('Validation failed')

    return render_template('admintest.html', form=form, eachtrolley=foundlist, totnames=tnames, totfaults=tfaults,
                           totmisused=tmisused, attention=attentionlist)


@app.route('/ourproduct')
def ourproduct():
    pfruit = pdt_fruit.get()
    pfruitlist = []
    for fruit_id in pfruit:
        eachfruit = pfruit[fruit_id]
        fruitBase = prodt.Product(eachfruit['name'], eachfruit['category'], eachfruit['price'], eachfruit['origin'],
                                  eachfruit['image_name'])
        pfruitlist.append(fruitBase)

    pveg = pdt_veg.get()
    pveglist = []
    for veg_id in pveg:
        eachveg = pveg[veg_id]
        vegBase = prodt.Product(eachveg['name'], eachveg['category'], eachveg['price'], eachveg['origin'],
                                eachveg['image_name'])
        pveglist.append(vegBase)

    return render_template('ourproduct.html', pfruit_list=pfruitlist, pveg_list=pveglist)


@app.route('/popularitem')
def popularitem():
    popular = popitem.get()
    poplist = []
    for pop_id in popular:
        eachpop = popular[pop_id]
        popBase = pop.PopularItem(eachpop['name'], eachpop['quantity'])
        poplist.append(popBase)
        print(popBase)

    return render_template('popularitem.html', pop_list=poplist)


@app.route('/healthyrecipe') #main recipe page
def healthyrecipe():
    rec = recipes.get()
    recipelist = []
    for recipe_id in rec:
        eachrecipe = rec[recipe_id]
        recipeBase = recs.Recipe(eachrecipe['recipeName'], eachrecipe['image'], eachrecipe['serving'],
                                 eachrecipe['cooktime'], eachrecipe['ingredient'], eachrecipe['method'],
                                 eachrecipe['link'], recipe_id)
        recipelist.append(recipeBase)

    return render_template('healthyrecipe.html', recipe_list=recipelist)


@app.route('/viewrecipe/<string:id>/', methods=['GET', 'POST']) #stop here 20180109 #orginally is /recipe1
def viewrecipe(id):
    #mag_db = root.child('recipes/' + id)
    rec = recipes.get()
    #recipelist = []
    recipetoview = rec[id]

    # for recipe_id in rec:
    #     eachrecipe = rec[recipe_id]
    #     recipeBase = recs.Recipe(eachrecipe['recipeName'], eachrecipe['image'], eachrecipe['serving'],
    #                              eachrecipe['cooktime'], eachrecipe['ingredient'], eachrecipe['method'],
    #                              eachrecipe['link'])
    #     recipelist.append(recipeBase)
    return render_template('viewrecipe.html', recipe_toview=recipetoview) #stop here 20180109


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
    event = events.get()
    list = []
    for event_id in event:
        eachevent = event[event_id]
        eventBase = ev.Event(eachevent['event_name'], eachevent['event_startDate'], eachevent['event_endDate'],
                             eachevent['image'], eachevent['link'])
        list.append(eventBase)

    return render_template('healthevent.html', event_list=list)


@app.route('/search') #stop here 20180109
def search():
    items = root.child('products').get()
    list = []  # create a list to store all the publication objects
    for itemid in items:
        eachitem = items[itemid]
        item = prodt.Product(eachitem['name'], eachitem['category'], eachitem['price'],
                        eachitem['origin'], eachitem['image_name'])

        item.set_itemid(itemid)
        #print(item.get_itemid())
        list.append(item)

    return render_template('search.html', item_list=list) #stop here 20180109


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignupForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data

        user = sp.Users(username, email, password)
        user_db = root.child('userbase')
        user_db.push({
            'username': user.get_username(),
            'email': user.get_email(),
            'password': user.get_password(),
        })

        flash('You have created an account with us', 'success')

        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


def validity_signup(form, field):
    userbase = user_ref.get()
    list = []


# for signup in userbase:
#   eachentry = userbase[signup]
#   entrybase = sp.Users(eachentry['username'], eachentry['email'], eachentry['password'])
#   list.append(entrybase)
#   if signup[1]['username'] == field.data:
#       raise ValidationError('Username has already been used')
#   elif signup[1]['email'] == field.data:
#       raise ValidationError('Email has already been used')

class SignupForm(Form):
    username = StringField('Username', [validators.Length(min=6, max=10), validators.DataRequired(), validity_signup])
    email = StringField('Email Address', [validators.Length(min=6, max=30), validators.DataRequired(), validity_signup])
    password = PasswordField('Password', [validators.Length(min=6, max=50), validators.DataRequired()])


class LoginForm(Form):
    username = StringField('Username:', [validators.DataRequired()])
    password = PasswordField('Password:', [validators.DataRequired()])


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():

        username = form.username.data
        password = form.password.data
        userbase = user_ref.get()
        for user in userbase.items():
            if user[1]['username'] == username and user[1]['password'] == password:
                session['user_data'] = user[1]
                session['logged_in'] = True
                session['logged_out'] = True
                session['id'] = username
                session['key'] = user[0]
                return redirect(url_for('myaccount'))
        flash('Login is not valid!', 'danger')
        return render_template('login.html', form=form)

    elif request.method == 'POST' and form.validate() == False:
        flash('Please enter your details', 'danger')
        return render_template('login.html', form=form)

    return render_template('login.html', form=form)


@app.route('/myaccount')
def myaccount():
    return render_template('myaccount.html')


@app.route('/logout')
def logout():
    session.clear()
    flash('You were logged out', 'success')
    return redirect(url_for('login'))


class AccountForm(Form):
    email = StringField('New Email', [validators.Length(min=6, max=30)])
    password = PasswordField('New Password (Optional)', [validators.Length(min=6, max=50)])


@app.route('/modify', methods=['GET', 'POST'])
def modifyuser():
    form = AccountForm(request.form)
    if request.method == 'POST' and form.validate():
        username = form.username.data
        password = form.password.data
        user = sp.Users(username, email, password)

        user_db = root.child('modify/' + id)
        user_db.set({
            'username': user.get_username(),
            'email': user.get_type(),
            'password': user.get_category(),
        })

        flash('Profile Updated Sucessfully.', 'success')

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


@app.route('/faq')
def faq():
    return render_template('faq.html')


# @app.route('/email')
# def email():
#    return render_template('email.html')

class EmailForm(Form):
    name = StringField('Name:', [validators.Length(min=1, max=100, message="Please enter your name"),
                                 validators.DataRequired()])
    user_email = StringField('Email:', [validators.Email(), validators.DataRequired()])
    feedback = StringField('Feedback:', [validators.Length(min=1, max=99999, message="Please enter your feedback"),
                                         validators.DataRequired()])


@app.route('/email', methods=["GET", "POST"])
def email():
    form = EmailForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        user_email = form.user_email.data
        feedback = form.feedback.data
        eEmail = uf.userFeedback(name, user_email, feedback)

        eEmail_db = root.child('email')
        eEmail_db.push({
            'name': eEmail.get_email_name(),
            'email': eEmail.get_user_email(),
            'feedback': eEmail.get_email_comment(),
        })
        flash('Thanks for emailing')

        return render_template('email.html', form=form)

    return render_template('email.html', form=form)

    # em_ref = db.reference('email')
    # print(em_ref.get())
#class ForumCommentForm(Form):


@app.route('/forum')#, methods=["GET", "POST"])
def forum():
    #form = ForumCommentForm(request.form)
    #if request.method == "POST" and form.validate():

    return render_template('forum.html')


@app.route('/workout')
def workout():
    return render_template('workout.html')


if __name__ == '__main__':
    app.secret_key = 'secret123'
    app.run(port='80')
