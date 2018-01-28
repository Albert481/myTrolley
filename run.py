from flask import Flask, render_template, request, flash, redirect, url_for, session
from wtforms import Form, SelectMultipleField, StringField, PasswordField, validators, RadioField, SelectField, \
    ValidationError, FileField, SubmitField, TextAreaField, DateField
import json
import firebase_admin
from firebase_admin import credentials, db, storage
import signup as sp
import trolleys as tr
import event as ev
import recipe as recs
import popularitem as pop
import product as prodt
import userFeedback as uf
import forumComment as fo
from Workout import Workout
from workoutWorkshop import workoutProgram

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

email_email = db.reference('response')
forum_forum = db.reference('forum')

workout = db.reference('workout')
workout_program = db.reference('workout_program')

app = Flask(__name__)
app.config['SECRET KEY'] = 'secret123'
app.secret_key = 'secret123'


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
    tnames = 0
    tfaults = 0
    tmisused = 0

    # Statistics function  implemented
    for trolleyid in trolleys.items():
        tnames += 1
        if int(trolleyid[1]['flag_count']) >= 3:
            tfaults += 1
        if trolleyid[1]['location'] != "":
            tmisused += 1

    # Attention function   not implemented
    for trolleyid in trolleys.items():
        if int(trolleyid[1]['flag_count']) >= 3:
            attention = tr.FindTrolley(trolleyid[1]['name'], trolleyid[1]['status'], trolleyid[1]['flag_count'],
                                       trolleyid[1]['location'], trolleyid[1]['comments'])
            attentionlist.append(attention)

    # Charts
    values = []

    values.append(tnames-tfaults)
    values.append(tfaults)
    return render_template('admin.html', form=form, eachtrolley=foundlist, totnames=tnames, totfaults=tfaults,
                           totmisused=tmisused, attention=attentionlist, values=values)


@app.route('/trolleys', methods=['GET', 'POST'])
def trolleys():
    trolleys = troll.get()
    form = AdminForm(request.form)
    trolleynumbers = form.trolleynumbers.data
    totaltrolleys = []

    if request.method == 'POST':
        # Add New Trolley
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

    # Trolleys Overview
    for trolleyid in trolleys.items():
        findtrolley = tr.FindTrolley(trolleyid[1]['name'], trolleyid[1]['status'],
                                     trolleyid[1]['flag_count'], trolleyid[1]['location'],
                                     trolleyid[1]['comments'])
        totaltrolleys.append(findtrolley)
    return render_template('trolleys.html', eachtrolley=totaltrolleys, form=form)


@app.route('/repair_trolley/<string:id>', methods=['POST'])
def repair_trolley(id):
    mag_db = root.child('trolleys/' + id)
    print(mag_db)
    flash('Trolley Repaired', 'success')

    return redirect(url_for('viewpublications'))

class ChangeAdmin(Form):
    username = StringField('Please enter Trolley ID:', render_kw={"placeholder": "Username"})
    adminlvl = RadioField('Admin Level', choices=[('admin0','0'), ('admin1', '1'), ('admin2', '2')])

@app.route('/accounts', methods=['GET', 'POST'])
def accounts():
    userbase = user_ref.get()
    totalaccounts = []
    form = ChangeAdmin(request.form)
    calledusername = form.username.data
    for user in userbase.items():
        finduser = sp.Admin(user[1]['username'], user[1]['email'], user[1]['admin'])
        totalaccounts.append(finduser)

    if request.method == 'POST':
        for username in userbase.items():
            if calledusername == username[1]['username']:
                admin = sp.Admin(username[1]['username'], username[1]['email'], username[1]['admin'])
                print(user_ref.child(username[0]))
                user_admin = user_ref.child(username[0])
                if form.adminlvl.data == 'admin0':
                    user_admin.update({
                        'admin': admin.set_admin('0'),
                    })
                elif form.adminlvl.data == 'admin1':
                    user_admin.update({
                        'admin': admin.set_admin('1'),
                    })
                elif form.adminlvl.data == 'admin2':
                    user_admin.update({
                        'admin': admin.set_admin('2'),
                    })
    return render_template('accounts.html', eachuser=totalaccounts, form=form)

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = ProductForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        category = form.protype.data
        price = form.price.data
        origin = form.origin.data
        image_name = form.image_name.data

        itemP = prodt.Product(name, category, price, origin, image_name)
        itemP_db = root.child('products')
        itemP_db.push({
                'name': itemP.get_name(),
                'category': itemP.get_category(),
                'price': itemP.get_price(),
                'origin': itemP.get_origin(),
                'image_name': itemP.get_image_name()

        })

        flash('Product Item Added Sucessfully.', 'success')

        return redirect(url_for('view_product'))


    return render_template('create_product.html', form=form)

@app.route('/delete_product/<string:id>', methods=['POST'])
def delete_product(id):
    itemP_db = root.child('products/' + id)
    itemP_db.delete()
    flash('Product Item Deleted Sucessfully.', 'success')

    return redirect(url_for('view_product'))

@app.route('/update_product/<string:id>/', methods=['GET', 'POST'])
def update_product(id):
    form = ProductForm(request.form)
    if request.method == 'POST' and form.validate():

        name = form.name.data
        category = form.protype.data
        price = form.price.data
        origin = form.origin.data
        image_name = form.image_name.data

        itemP = prodt.Product(name, category, price, origin, image_name)
        # create the product object
        itemP_db = root.child('products/' + id)
        itemP_db.set({
                'name': itemP.get_name(),
                'category': itemP.get_category(),
                'price': itemP.get_price(),
                'origin': itemP.get_origin(),
                'image_name': itemP.get_image_name()
        })

        flash('Product Item Updated Sucessfully.', 'success')

        return redirect(url_for('view_product'))
    else:
        url = 'products/' + id
        eachprod = root.child(url).get()

        uitem = prodt.Product(eachprod['name'], eachprod['category'], eachprod['price'],
                              eachprod['origin'], eachprod['image_name'])

        uitem.set_itemid(id)
        form.name.data = uitem.get_name()
        form.protype.data = uitem.get_category()
        form.price.data = uitem.get_price()
        form.origin.data = uitem.get_origin()
        form.image_name.data = uitem.get_image_name()

        return render_template('update_product.html', form=form)

@app.route('/view_product') #20180116
def view_product():
    vitems = root.child('products').get()
    list = []  # create a list to store all the product objects
    for itemid in vitems:
        eachitem = vitems[itemid]
        vitem = prodt.Product(eachitem['name'], eachitem['category'], eachitem['price'],
                        eachitem['origin'], eachitem['image_name'])

        vitem.set_itemid(itemid)
        list.append(vitem)

    return render_template('view_product.html', vitem_list=list)


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
    #poplist = []
    name=[]
    quantity=[]

    for pop_id in popular:
        eachpop = popular[pop_id]
        nameBase = eachpop['name']
        quantityBase = eachpop['quantity']
        name.append(nameBase)
        quantity.append(quantityBase)

    return render_template('popularitem.html', name_list=name, quantity_list=quantity)


@app.route('/healthyrecipe')  # main recipe page
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


@app.route('/viewrecipe/<string:id>/', methods=['GET', 'POST'])
def viewrecipe(id):
    # mag_db = root.child('recipes/' + id)
    rec = recipes.get()
    recipelist = []
    eachrecipe = rec[id]
    recipeBase = recs.Recipe(eachrecipe['recipeName'], eachrecipe['image'], eachrecipe['serving'],
                             eachrecipe['cooktime'], eachrecipe['ingredient'], eachrecipe['method'],
                             eachrecipe['link'], id)
    recipelist.append(recipeBase)

    return render_template('viewrecipe.html', recipe_toview=recipelist)


@app.route('/healthevent')
def healthevent():
    event = events.get()
    list = []
    for event_id in event:
        eachevent = event[event_id]
        eventBase = ev.Event(eachevent['event_name'], eachevent['event_startDate'], eachevent['event_endDate'],
                             eachevent['image'], eachevent['time'], eachevent['location'], eachevent['status'],
                             eachevent['description'], event_id)
        list.append(eventBase)

    return render_template('healthevent.html', event_list=list)


@app.route('/viewevent/<string:id>/', methods=['GET', 'POST'])
def viewevent(id):
    event = events.get()
    eventlist = []
    eachevent = event[id]
    eventBase = ev.Event(eachevent['event_name'], eachevent['event_startDate'], eachevent['event_endDate'],
                         eachevent['image'], eachevent['time'], eachevent['location'], eachevent['status'],
                         eachevent['description'], id)
    eventlist.append(eventBase)

    return render_template('viewevent.html', event_toview=eventlist)


@app.route('/search')
def search():
    items = root.child('products').get()
    list = []  # create a list to store all the publication objects
    for itemid in items:
        eachitem = items[itemid]
        item = prodt.Product(eachitem['name'], eachitem['category'], eachitem['price'],
                             eachitem['origin'], eachitem['image_name'])

        item.set_itemid(itemid)
        # print(item.get_itemid())
        list.append(item)

    return render_template('search.html', item_list=list)

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

class ProductForm(Form):
    name = StringField('Product Name', [
        validators.Length(min=1, max=150),
        validators.DataRequired()])
    protype = RadioField('Category', choices=[('Fruits', 'Fruits'), ('Vegetables', 'Vegetables')], default='Fruits')
    price = StringField('Price', [
        validators.Length(min=1, max=100),
        validators.DataRequired()])
    origin = StringField('Origin', [
        validators.Length(min=1, max=100),
        validators.DataRequired()])
    image_name = StringField('Image File', [
        validators.Length(min=1, max=100),
        validators.DataRequired()])



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
            'admin': 0
        })

        flash('You have created an account with us', 'success')

        return redirect(url_for('login'))

    return render_template('signup.html', form=form)


def validity_signup(form, field):
    userbase = user_ref.get()
    for user in userbase.items():
        if user[1]['username'] == field.data:
            raise ValidationError('Username has already been used')
        elif user[1]['email'] == field.data:
            raise ValidationError('Email has already been used')

class SignupForm(Form):
    username = StringField('Username', [validators.Length(min=6, max=10), validators.DataRequired(), validity_signup])
    email = StringField('Email Address', [validators.Length(min=6, max=30), validators.DataRequired(), validity_signup])
    password = PasswordField('Password', [validators.Length(min=6, max=50), validators.DataRequired()])


class LoginForm(Form):
    username = StringField('Username:', [validators.DataRequired()])
    password = PasswordField('Password:', [validators.DataRequired()])

#
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
                session['admin'] = user[1]['admin']

                return redirect(url_for('home'))
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


@app.route('/modifyuser', methods=['GET', 'POST'])
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


class EmailForm(Form):
    name = StringField('Name:', [validators.Length(min=1, max=100, message="Please enter your name"),
                                 validators.DataRequired()])
    user_email = StringField('Email:', [validators.Email(), validators.DataRequired()])
    feedback = TextAreaField('Feedback:', [validators.Length(min=1, max=99999, message="Please enter your feedback"),
                                         validators.DataRequired()])


@app.route('/email', methods=["GET", "POST"])
def email():
    form = EmailForm(request.form)
    if request.method == 'POST' and form.validate():
        name = form.name.data
        user_email = form.user_email.data
        feedback = form.feedback.data
        eEmail = uf.userFeedback(name, user_email, feedback)

        eEmail_db = root.child('response')
        eEmail_db.push({
            'name': eEmail.get_email_name(),
            'email': eEmail.get_user_email(),
            'feedback': eEmail.get_email_comment(),
        })
        flash('Your email has been sent!')

        return render_template('email.html', form=form)

    return render_template('email.html', form=form)

    # em_ref = db.reference('response')
    # print(em_ref.get())


class ForumCommentForm(Form):
    comment = TextAreaField('', [validators.Length(min=1, max=9999999, message='Please enter your comment'),
                                      validators.DataRequired()])


@app.route('/forum', methods=["GET", "POST"])
def forum():
    form = ForumCommentForm(request.form)
    if request.method == "POST" and form.validate():
        comment = form.comment.data
        fForum = fo.forumComment(comment)

        fForum_db = root.child('forum')
        fForum_db.push({
            'comment': fForum.get_comment(),
        })

        flash('Your comment has been sent!')

        return render_template('forum.html', form=form)

    return render_template('forum.html', form=form)


class WorkoutForm(Form):
    time_choices = [('10min', '0-10min'), ('20min', '0-20min'), ('30min', '0-30min')]
    time = SelectField('Time', choices=time_choices, default='10min')
    difficulty_level_choices = [('1', '1'), ('2', '2'), ('3', '3')]
    difficulty_level = RadioField('Difficulty Level', choices=difficulty_level_choices, default='1')
    body_focus_choices = [('core', 'Core'), ('whole_body', 'Total')]
    body_focus = SelectField('Body Focus', choices=body_focus_choices, default='core')


@app.route('/workout_type_1')
def workout_type_1():
    return render_template('workout_type_1.html')

@app.route('/workout_type_2')
def workout_type_2():
    return render_template('workout_type_2.html')

@app.route('/workout_type_3')
def workout_type_3():
    return render_template('workout_type_3.html')

@app.route('/workout_type_4')
def workout_type_4():
    return render_template('workout_type_4.html')

@app.route('/workout_type_5')
def workout_type_5():
    return render_template('workout_type_5.html')

@app.route('/workout_type_6')
def workout_type_6():
    return render_template('workout_type_6.html')

@app.route('/workout_type_7')
def workout_type_7():
    return render_template('workout_type_7.html')

@app.route('/workout_type_8')
def workout_type_8():
    return render_template('workout_type_8.html')

@app.route('/workout_type_9')
def workout_type_9():
    return render_template('workout_type_9.html')

@app.route('/workout_type_10')
def workout_type_10():
    return render_template('workout_type_10.html')

@app.route('/workout_type_11')
def workout_type_11():
    return render_template('workout_type_11.html')

@app.route('/workout_type_12')
def workout_type_12():
    return render_template('workout_type_12.html')

@app.route('/workout_type_13')
def workout_type_13():
    return render_template('workout_type_13.html')

@app.route('/workout_type_14')
def workout_type_14():
    return render_template('workout_type_14.html')

@app.route('/workout_type_15')
def workout_type_15():
    return render_template('workout_type_15.html')

@app.route('/workout_type_16')
def workout_type_16():
    return render_template('workout_type_16.html')

@app.route('/workout_type_17')
def workout_type_17():
    return render_template('workout_type_17.html')

@app.route('/workout_type_18')
def workout_type_18():
    return render_template('workout_type_18.html')

@app.route('/workout', methods=['GET', 'POST'])
def workout():
    form = WorkoutForm(request.form)
    if request.method == 'POST' and form.validate():
        time = form.time.data
        difficulty_level = form.difficulty_level.data
        body_focus = form.body_focus.data

        workout = Workout(time, difficulty_level, body_focus)

        workout_db = root.child('workout')
        workout_db.push({
            'time': workout.get_time(),
            'diff_level': workout.get_diff_level(),
            'body_focus': workout.get_body_focus()
        })

        workout_type_dest = ''
        #form2 = WorkoutTypeForm(request.form)

        if body_focus == 'core':
            if time == '10min':
                if difficulty_level == '1':
                    workout_type_dest = 'workout_type_1'
                    #form2.videolink1 = 'some video link ...'
                    #form2.duration = 'some value'
                    #form2.calorieburn = 'some value'
                elif difficulty_level == '2':
                    workout_type_dest = 'workout_type_2'
                elif difficulty_level == '3':
                    workout_type_dest = 'workout_type_3'
            elif time == '20min':
                if difficulty_level == '1':
                    workout_type_dest = 'workout_type_4'
                elif difficulty_level == '2':
                    workout_type_dest = 'workout_type_5'
                elif difficulty_level == '3':
                    workout_type_dest = 'workout_type_6'
            elif time == '30min':
                if difficulty_level == '1':
                    workout_type_dest = 'workout_type_7'
                elif difficulty_level == '2':
                    workout_type_dest = 'workout_type_8'
                elif difficulty_level == '3':
                    workout_type_dest = 'workout_type_9'

        elif body_focus == 'whole_body':
            if time == '10min':
                if difficulty_level == '1':
                    workout_type_dest = 'workout_type_10'
                elif difficulty_level == '2':
                    workout_type_dest = 'workout_type_11'
                elif difficulty_level == '3':
                    workout_type_dest = 'workout_type_12'
            elif time == '20min':
                if difficulty_level == '1':
                    workout_type_dest = 'workout_type_13'
                elif difficulty_level == '2':
                    workout_type_dest = 'workout_type_14'
                elif difficulty_level == '3':
                    workout_type_dest = 'workout_type_15'
            elif time == '30min':
                if difficulty_level == '1':
                    workout_type_dest = 'workout_type_16'
                elif difficulty_level == '2':
                    workout_type_dest = 'workout_type_17'
                elif difficulty_level == '3':
                    workout_type_dest = 'workout_type_18'

        return redirect(url_for(workout_type_dest))
        #return redirect(url_for(workout_type_dest), form=form2)

    return render_template('workout.html', form=form)

class ProgramRegistrationForm(Form):
    weight = StringField('Weight', [validators.DataRequired()])
    height = StringField('Height', [validators.DataRequired()])
    medical_condition_choices = [('no','No'),('asthma', 'Asthma'), ('high blood pressure', 'High Blood Pressure')]
    medical_condition = SelectField('Do you have any medical conditions?', [validators.DataRequired()], choices=medical_condition_choices)
    allergy_choices= [('milk','Milk'),('peanuts','Peanuts'),('soy','Soy')]
    allergy = SelectField('Do you have any food allergies?', [validators.DataRequired()], choices=allergy_choices)

@app.route('/workoutProgram', methods=['GET', 'POST'])
def workout_program():
    form = ProgramRegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        weight = form.weight.data
        height = form.height.data
        medical_condition = form.medical_condition.data
        allergy = form.allergy.data

        workout_program = workoutProgram(weight,height,medical_condition, allergy)

        workout_program_db = root.child('workout_program')
        workout_program_db.push({
            'weight': workout_program.get_weight(),
            'height': workout_program.get_height(),
            'medical_condition': workout_program.get_medical_condition(),
            'allergy': workout_program.get_allergy()
        })

        flash('Thank you! The form was submitted successfully.', 'success')

    return render_template('workshop_form.html', form=form)

if __name__ == '__main__':
    app.run()
