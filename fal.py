from flask import Flask, render_template, jsonify, template_rendered
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, \
	UserMixin, RoleMixin, login_required, datastore
from flask_security.utils import encrypt_password
from flask_security.decorators import roles_accepted
from flask_security.forms import LoginForm, RegisterForm
from wtforms import StringField
from wtforms.validators import InputRequired, DataRequired
from wtforms.fields import SelectField, RadioField
from flask_security.core import current_user
from flask_security.signals import user_registered
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from flask_wtf import FlaskForm

debug = False
app = Flask(__name__)
if debug:
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:qwerty@localhost/sql_alchemy'
else:
	app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://leapskills:qwerty123456@aa1uktgh5pd3lf4.c6ht4o5zh8hw.ap-south-1.rds.amazonaws.com/ebdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'blahblahbooh'
app.config['SECURITY_PASSWORD_HASH'] = "sha512_crypt"
app.config['SECURITY_PASSWORD_SALT'] = 'abcracadabrav'
app.config['SECURITY_UNAUTHORIZED_VIEW'] = False
app.config['SECURITY_USER_IDENTITY_ATTRIBUTES'] = 'leap_id, email, mobile_number'
app.config['SECURITY_TRACKABLE'] = True
app.config['SECURITY_REGISTERABLE'] = True
app.config['SECURITY_SEND_REGISTER_EMAIL'] = False
app.config['SECURITY_LOGIN_USER_TEMPLATE'] = 'security/login_user.html'
app.config['SECURITY_REGISTER_USER_TEMPLATE'] = 'security/register_user.html'



# Create database connection object
db = SQLAlchemy(app)

# Define models
roles_users = db.Table('roles_users',
		db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
		db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))

# code_creater = db.Table('code_creater',
#         db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
#         db.Column('access_code_id', db.Integer(), db.ForeignKey('access_code.id')))

class Role(db.Model, RoleMixin):
	id = db.Column(db.Integer(), primary_key=True)
	name = db.Column(db.String(80), unique=True)
	description = db.Column(db.String(255))

class Access_code(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	code = db.Column(db.String(50), unique=True)
	pm_id = db.Column(db.Integer, db.ForeignKey('user.id'),
		nullable=False)

class Center(db.Model):
	id = db.Column(db.Integer(), primary_key = True)
	name = db.Column(db.String(255))
	status = db.Column(db.Boolean())
	pm_id = db.Column(db.Integer, db.ForeignKey('user.id'),
		nullable=False)

class College(db.Model):
	id = db.Column(db.Integer(), primary_key = True)
	name = db.Column(db.String(255))
	address = db.Column(db.String(255))
	contact_person = db.Column(db.String(100))
	contact_number = db.Column(db.String(100))
	status = db.Column(db.Boolean())
		

class Svar(db.Model):
	id = db.Column(db.Integer(), primary_key = True)
	svar = db.Column(db.String(255))
	student_id = db.Column(db.Integer, db.ForeignKey('user.id'),
		nullable=False)

class Attendance(db.Model):
	id = db.Column(db.Integer(), primary_key = True)
	student_id = db.Column(db.Integer())
	present = db.Column(db.Boolean())
	date = db.Column(db.String(100))
	timestamp = db.Column(db.Integer())
	
	type = db.Column(db.String(50))
	session = db.Column(db.String(100))

class Session(db.Model):
	id = db.Column(db.Integer(), primary_key = True)
	batch_id = db.Column(db.Integer())
	name = db.Column(db.String(255))
	session_seq = db.Column(db.Integer())
	

class App_hello_english(db.Model):
	id = db.Column(db.Integer(), primary_key = True)
	app_id = db.Column(db.String(255))
	app_password = db.Column(db.String(255))
	student_id = db.Column(db.Integer, db.ForeignKey('user.id'),
		nullable=False)

class Batch(db.Model):
	id = db.Column(db.Integer(), primary_key=True)
	timing = db.Column(db.String(50))
	name = db.Column(db.String(50))
	start_date = db.Column(db.String(50))
	end_date = db.Column(db.String(50))
	cefr_level = db.Column(db.Integer())
	center_id = db.Column(db.Integer())
	trainer_id = db.Column(db.Integer, db.ForeignKey('user.id'),
		nullable=False)

class User(db.Model, UserMixin):
	id = db.Column(db.Integer, primary_key=True)
	email = db.Column(db.String(255))
	password = db.Column(db.String(255))
	active = db.Column(db.Boolean())
	confirmed_at = db.Column(db.DateTime())
	first_name = db.Column(db.String(255), nullable=False)
	last_name = db.Column(db.String(255))
	home_town = db.Column(db.String(255))
	district = db.Column(db.String(255))
	access_code = db.Column(db.String(50))
	dob = db.Column(db.String(50))
	gender = db.Column(db.String(50))
	caste = db.Column(db.String(50))
	linkedin_url = db.Column(db.String(255))
	resume_url = db.Column(db.String(255))
	father_name = db.Column(db.String(255))
	mother_name = db.Column(db.String(255))
	family_income = db.Column(db.String(50))
	aadhar_card = db.Column(db.String(50))
	college_name = db.Column(db.String(50))
	stream = db.Column(db.String(50))
	college_roll_number = db.Column(db.String(50))
	college_year = db.Column(db.String(50))
	section = db.Column(db.String(50))
	batch_id = db.Column(db.String(50))
	leap_id = db.Column(db.String(50))
	mobile_number = db.Column(db.String(50))
	last_login_at = db.Column(db.DateTime())
	current_login_at = db.Column(db.DateTime())
	last_login_ip = db.Column(db.String(255))
	current_login_ip = db.Column(db.String(255))
	login_count = db.Column(db.Integer())
	program_status = db.Column(db.String(50))
	pre_assesment_id = db.relationship('Svar', backref = 'student_pre', lazy = True)
	post_assesment_id = db.relationship('Svar', backref = 'student_post', lazy = True)
	hello_english_id = db.relationship('App_hello_english', backref = 'student_he', lazy = True)
	placement_status = db.Column(db.String(50))
	class_10_percentage = db.Column(db.String(50))
	class_12_percentage = db.Column(db.String(50))
	medium_of_instruction = db.Column(db.String(50))
	graduate_parents = db.Column(db.String(50))
	roles = db.relationship('Role', secondary = roles_users,
							backref = db.backref('users', lazy ='dynamic'))
	access_code_pm = db.relationship('Access_code', backref = 'pm_code', lazy = True)
	batch_alloted_trainer = db.relationship('Batch', backref = 'trainer_batch', lazy = True)
	center_alloted_pm = db.relationship('Center', backref = 'pm_center', lazy = True)

class ExtendedLoginForm(LoginForm):
	email = StringField('Leap Id', [InputRequired()])
	password = StringField('Date of Birth', [InputRequired()])


def college_query():
	choices = [(str(c.id),c.name) for c in College.query.filter_by(status=True).order_by('id').all()]
	return choices

def batch_query():
	choices = [(str(c.id),c.name) for c in Batch.query.filter_by(trainer_id=current_user.id).order_by('id').all()]


class ExtendedRegisterForm(RegisterForm):
	first_name = StringField('First Name', [InputRequired()])
	last_name = StringField('Last Name')
	password = StringField('Date of Birth(Password)')
	password_confirm = StringField('Confirm Date of Birth(Password)')
	gender = RadioField('Gender', choices=[('0','Male'),('1','Female'),('2','Others')])
	email = StringField('Email')
	mobile_number = StringField('Mobile Number', [InputRequired()])
	home_town = StringField('Home Town')
	district = StringField('District')
	college_name = SelectField('College Name', choices=college_query())
	college_roll_number = StringField('College Roll Number')
	stream = SelectField('Stream', choices= [('1','B.Sc'),('2','B.A'),('3','B.Ed'),('4','B.Pharma'),('5','BHM'),('6','B.Tech')])
	college_year = SelectField('College Year', choices= [('1','1st'),('2', '2nd'),('3', '3rd'),('4', '4th')])




# Setup Flask-Security
user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore, login_form=ExtendedLoginForm, register_form=ExtendedRegisterForm)

# Create a user to test with
# @app.before_first_request
# def create_user():
#     db.create_all()
#     user_datastore.create_user(leap_id='LS180000090', password=encrypt_password('qwerty'),first_name='Trainer', last_name='Trainer')
#     db.session.commit()


# Views
@app.route('/')
@login_required
@roles_accepted()
def home():
	role = current_user.roles[0].name
	if role == 'student':
		return render_template('student_index.html', current_user=current_user)
	if role == 'pm':
		return render_template('pm_index.html', current_user=current_user)
	if role == 'trainer':
		return render_template('trainer_index.html', current_user=current_user)
	if role == 'admin':
		return render_template('admin_index.html', current_user=current_user)


@app.route('/trainer_batch')
@login_required
@roles_accepted('trainer')
def get_all_batches():
	choices = [(str(c.id),c.name) for c in Batch.query.filter_by(trainer_id=current_user.id).order_by('id').all()]
	return choices

@app.route('/batch_student/<int:id>')
@login_required
@roles_accepted('trainer')
def get_all_students_by_batch(id):
	choices = [(str(c.id),c.first_name,c.last_name,c.leap_id) for c in User.query.filter_by(batch_id=str(id)).order_by('id').all()]
	print(choices)
	return choices

# @app.route('/create_trainer')
# @app.before_first_request
# def crt():
# 	user_datastore.create_user(leap_id='LS180000090', password=encrypt_password('qwerty'),first_name='Trainer', last_name='Trainer')
# 	db.session.commit()


def leap_id_gen(id):
	num = format(id, "06d")
	l_id = "LS18" + num
	return l_id

def user_registered_sighandler(sender, **extra):
	user  = extra.get('user')
	role = user_datastore.find_or_create_role('student')
	user_datastore.add_role_to_user(user,role)
	user.leap_id = leap_id_gen(user.id)
	db.session.commit()
user_registered.connect(user_registered_sighandler)

if __name__ == '__main__':
	app.run()