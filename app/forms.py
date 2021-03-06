from flask.ext.wtf import Form, TextField, BooleanField, RecaptchaField, TextAreaField, RadioField,SelectField,IntegerField, FileField,SubmitField,validators, ValidationError, PasswordField
from flask.ext.wtf import Required, Length, NumberRange
from app.models import User


class EditForm(Form):
    nickname = TextField('nickname', validators = [Required()])
    about_me = TextAreaField('about_me', validators = [Length(min = 0, max = 140)])
    phone = IntegerField('phone')
    fileName = FileField()

    def __init__(self, original_nickname, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
        self.original_nickname = original_nickname
        
    def validate(self):
        if not Form.validate(self):
            return False
        if self.nickname.data == self.original_nickname:
            return True
        user = User.query.filter_by(nickname = self.nickname.data).first()
        
        if user != None:
            self.nickname.errors.append('This nickname is already in use. Please choose another one.')
            return False
        return True
        
class PostForm(Form):
    title = TextField('Title', validators = [Required()])
    style = SelectField('Property Type', choices=[('House', 'House'), ('Town House','Town House'), ('Condo', 'Condo'), ('Apartment','Apartment')])
    bedroom_no = IntegerField('Bedroom', validators = [NumberRange(min=1, max= 5)])
    bathroom_no = IntegerField('Bathroom', validators = [NumberRange(min=1, max= 5)])
    garage_no = IntegerField('Garage', validators = [NumberRange(min=0, max= 4)])
    body = TextAreaField('Body')
    fileName = FileField()
    location = location = SelectField('City', choices=[('Toronto', 'Toronto'), ('Mississauga', 'Mississauga'),('Markham','Markham'),('Richmond Hill','Richmond Hill'),('Vaughan','Vaughan'),('Milton','Milton')])
    price = IntegerField('Price', validators = [NumberRange(min=100000, max= 10000000)])
    address = TextField('Address')
    
    

class ContactForm(Form):
    name = TextField("Name",  [validators.Required("Please enter your name.")])
    email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("e.g. user@example.com")])
    subject = TextField("Subject",  [validators.Required("Please enter a subject.")])
    message = TextAreaField("Message",  [validators.Required("Please enter a message.")])
    submit = SubmitField("Send")

class SignupForm(Form):
    firstname = TextField("First name",  [validators.Required("Please enter your first name.")])
    lastname = TextField("Last name",  [validators.Required("Please enter your last name.")])
    email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.Required("Please enter a password.")])
    #Select fields keep a choices property which is a sequence of (value, label) pairs.
    user_role = SelectField('Role', choices=[('user', 'User'), ('agent', 'Agent')])
    recaptcha = RecaptchaField()
    submit = SubmitField("Create account")
 
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
 
    def validate(self):
        if not Form.validate(self):
            return False
        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user:
            self.email.errors.append("That email is already taken")
            return False
        else:
            return True

class SigninForm(Form):
    email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
    password = PasswordField('Password', [validators.Required("Please enter a password.")])
    remember_me = BooleanField('Remember me', default = False)
    submit = SubmitField("Sign In")
    
    def __init__(self, *args, **kwargs):
        Form.__init__(self, *args, **kwargs)
 
    def validate(self):
        if not Form.validate(self):
            return False
     
        user = User.query.filter_by(email = self.email.data.lower()).first()
        if user and user.check_password(self.password.data):
            return True
        else:
            self.email.errors.append("Invalid e-mail or password")
            return False

class PeferForm(Form):
    style = SelectField('Property Type', choices=[('House', 'House'), ('Town House','Town House'), ('Condo', 'Condo'), ('Apartment','Apartment')])
    bedroom_no = IntegerField('Bedroom', default = 3, validators = [NumberRange(min=1, max= 5)])
    bathroom_no = IntegerField('Bathroom', default = 3, validators = [NumberRange(min=1, max= 5)])
    garage_no = IntegerField('Garage', default = 1, validators = [NumberRange(min=0, max= 4)])
    notify = BooleanField('Notify Me', default = True)
    location = SelectField('Location', choices=[('Toronto', 'Toronto'), ('Mississauga', 'Mississauga'),('Markham','Markham'),('Richmond Hill','Richmond Hill'),('Vaughan','Vaughan'),('Milton','Milton')])
    price = IntegerField('Price', validators = [NumberRange(min=100000, max= 10000000)])
    
    submit = SubmitField("Send")
    
    def validate(self):
        return True

    
class OrderForm(Form):
    order = SelectField('Sort By', choices=[('price', 'Price'), ('location', 'Location'),('style','Type'), ('date','Date')])