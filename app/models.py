from app import db
from flask_login import UserMixin
from datetime import datetime as dt
from werkzeug.security import generate_password_hash, check_password_hash
from app import login

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(255))
    item_price = db.Column(db.Integer)
    item_des = db.Column(db.Text)
    item_category = db.Column(db.String(255))
    item_img = db.Column(db.String(255))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def __repr__(self):
        return f'<id: {self.id} | {self.item_name}>'

    def to_dict(self):
        data={
            'id': self.id,
            'item_name': self.item_name,
            'item_price': self.item_price,
            'item_des': self.item_des,
            'item_category': self.item_category,
        }
        return data
    def add_item(self):
        db.session.add(self)
        db.session.commit()
    
    def delete_item(self):
        db.session.delete(self)
        db.session.commit()

class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f'<id: {self.id} | {self.item_id}>'

    def to_dict(self):
        data={
            'id': self.id,
            'item_id': self.item_id,
            'user_id': self.user_id
        }
        return data
    def add_item(self):
        db.session.add(self)
        db.session.commit()

    def add_item(self):
        db.session.add(self)
        db.session.commit()


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    email = db.Column(db.String(200), unique = True, index=True)
    password = db.Column(db.String(200))
    created_on = db.Column(db.DateTime, default=dt.utcnow)
    
    

    def __repr__(self):
        return f'<User: {self.id} | {self.email}>'

    def from_dict(self, data):
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = self.hash_password(data['password'])
        self.save()


    def hash_password(self, original_password):
        return generate_password_hash(original_password)

    def check_hashed_password(self, login_password):
        return check_password_hash(self.password, login_password)

    def save(self):
        db.session.add(self)
        db.session.commit()

    

@login.user_loader
def load_user(id):
    return User.query.get(int(id))