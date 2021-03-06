from flask import Flask
from flask import  render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security,SQLAlchemyUserDatastore,UserMixin,RoleMixin,login_required

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:xanthis07@localhost/flask_movie'
app.config['SECRET_KEY']='super-secret'
app.config['SECURITY_REGISTERABLE']=True
app.config['SECURITY_PASSWORD_HASH']='plaintext'
app.debug=True
db=SQLAlchemy(app)

#create models

roles_users = db.Table('roles_users',
                       db.Column('user_id',db.Integer(),db.ForeignKey('user.id')),
                       db.Column('role_id',db.Integer(),db.ForeignKey('role.id')))

class Role(db.Model,RoleMixin):
    id=db.Column(db.Integer(),primary_key=True)
    name= db.Column(db.String(80),unique=True)
    description=db.Column(db.String(255))

class User(db.Model,UserMixin):
    id= db.Column(db.Integer, primary_key=True)
    email= db.Column(db.String(255),unique=True)
    password=db.Column(db.String(255))
    active= db.Column(db.Boolean())
    confirmed_at=db.Column(db.DateTime())
    roles=db.relationship('Role',secondary=roles_users,backref=db.backref('users',lazy='dynamic'))

#setup flask security
user_datastore=SQLAlchemyUserDatastore(db,User,Role)
security=Security(app, user_datastore)

@app.route('/')
def index():
    return  render_template('index.html')

@app.route('/profile/<email>')
@login_required
def profile(email):
    user=User.query.filter(email=email).first()
    return  render_template('profile.html',user=user)

if __name__=="__main__":
    app.run()