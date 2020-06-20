import datetime, time 
from flaskclub import db, login_manager
from flask_login import UserMixin
from flask import url_for

@login_manager.user_loader
def load_user(user_id):
	return Student.query.get(user_id)

person = db.Table('person', 
	db.Column('club_id', db.Integer, db.ForeignKey('clubs.id'), primary_key=True),
	db.Column('student_id', db.String(10), db.ForeignKey('student.student_id'), primary_key=True))

class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page,
                                **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page,
                                **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page,
                                **kwargs) if resources.has_prev else None
            }
        }
        return data


class Student(PaginatedAPIMixin, db.Model, UserMixin): 
	__tablename__ = 'student'
	id = db.Column('student_id', db.String(10), primary_key=True) 
	firstname = db.Column('first_name', db.String(255), nullable=False) 
	lastname = db.Column('last_name', db.String(255), nullable=True) 
	email = db.Column('email', db.String(255), unique=True, nullable=False) 
	password = db.Column('password', db.String(255), nullable=False)  
	gender = db.Column('gender', db.String(255), nullable=False)  
	batch = db.Column('batch', db.Integer, nullable=False) 
	role = db.Column('role', db.String(255), nullable=True)  
	club_id = db.Column('club_id', db.Integer, nullable=False) 
	image_file = db.Column('image_file', db.String(20), nullable=False, default='default.jpg')	

	clubs = db.relationship('Clubs', secondary=person, lazy='dynamic', backref=db.backref('people', lazy = 'dynamic'))
	posts = db.relationship('Post', backref='author', lazy=True) 
	replies = db.relationship('Reply', backref='author', lazy=True)


	def __repr__(self):
		return f"Student('{self.firstname}', '{self.lastname}', '{self.email}')"

	def to_dict(self):
		data = {'id':self.id, 
				'firstname':self.firstname, 
				'lastname':self.lastname, 
				'email':self.email, 
				'gender':self.gender,
				'batch':self.batch,
				'club_id':self.club_id, 
				'role':self.role,
				'links': {
					'self': url_for('api.get_user', id=self.id)
					}
				} 
		return data


class BinusID(db.Model, UserMixin):
	__tablename__ = 'binus_id' 
	id = db.Column('binusian_id', db.String(10), primary_key=True)  
	email = db.Column('email', db.String(255), nullable=True) 

	def __repr__(self):
		return f"BinusID('{self.id}')"

class Clubs(db.Model, UserMixin): 
	__tablename__ = 'clubs'
	id = db.Column('id', db.Integer, primary_key=True) 
	name = db.Column('name', db.String(255), nullable=False) 
	contact = db.Column('contact', db.String(255), nullable=True) 
	email = db.Column('email', db.String(255), nullable=True) 
	acronym = db.Column('acronym', db.String(10), nullable=False) 
	image_file = db.Column('image', db.String(20), nullable=False, default='default.png')	

	activities = db.relationship('Activities', backref='activ', lazy=True) 
	# posts = db.relationship('Post', backref='club', lazy=True) 
	
	def __repr__(self):
		return f"Clubs('{self.name}')" 

	def to_dict(self):
		data = {'id':self.id, 
				'name':self.name, 
				'contact':self.contact, 
				'email':self.email, 
				'acronym':self.acronym,
				'links': {
					'self': url_for('api.get_club', id=self.id)
					}
				} 
		return data

class Activities(db.Model, UserMixin): 
	__tablename__ = 'activities'
	id = db.Column('id', db.Integer, primary_key=True) 
	name = db.Column('name', db.String(255), nullable=False)  
	image_file = db.Column('image', db.String(20), nullable=False, default='default.jpg')	 
	date_posted = db.Column('date_posted', db.DateTime, nullable=False)
	
	club_id = db.Column('club_id', db.Integer, db.ForeignKey('clubs.id'))

	def __repr__(self):
		return f"Activities('{self.name}')" 

class Post(PaginatedAPIMixin, db.Model, UserMixin):
	__tablename__ = 'post'
	id = db.Column('id', db.Integer, primary_key=True)
	title = db.Column('title', db.String(100), nullable=False)
	date_posted = db.Column('date_posted', db.DateTime, nullable=False, default=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
	content = db.Column('content', db.Text, nullable=False)

	user_id = db.Column('user_id', db.String(10), db.ForeignKey('student.student_id'), nullable=False)
	# club_id = db.Column('club_id', db.Integer, db.ForeignKey('club.id'), nullable=False)

	def __repr__(self):
	    return f"Post('{self.title}', '{self.date_posted}')"

	def to_dict(self):
		data = {'id':self.id, 
				'title':self.title, 
				'date_posted':self.date_posted, 
				'content':self.content, 
				'author':self.user_id
				} 
		return data



class Reply(db.Model, UserMixin):
	__tablename__ = 'reply'
	id = db.Column('id', db.Integer, primary_key=True)
	content = db.Column('content', db.Text, nullable=False)
	date_posted = db.Column('date_posted', db.DateTime, nullable=False, default=datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))
	post_id = db.Column('post_id', db.Integer, db.ForeignKey('post.id'), nullable=False)
	user_id = db.Column('user_id', db.String(10), db.ForeignKey('student.student_id'), nullable=False)

	def __repr__(self):
	    return f"Reply('{self.post_id}', '{self.date_posted}')"

class Admin(db.Model, UserMixin):
	id = db.Column('id', db.Integer, primary_key=True) 
	username = db.Column('username', db.String(255), nullable=False, unique=True)
	email = db.Column('email', db.String(255), nullable=False, unique=True)
	password = db.Column('password', db.String(255), nullable=False) 

	def __repr__(self):
	    return f"Admin('{self.usernamed}')"

	
