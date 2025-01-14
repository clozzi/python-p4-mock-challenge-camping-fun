from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

convention = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

metadata = MetaData(naming_convention=convention)

db = SQLAlchemy(metadata=metadata)


class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)

    signups = db.relationship(
        'Signup', back_populates='activity', cascade='all, delete-orphan'
    )

    serialize_rules = ('-signups.activity',)

    def __repr__(self):
        return f'<Activity {self.id}: {self.name}>'


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)

    signups = db.relationship(
        'Signup', back_populates='camper', cascade='all, delete-orphan'
    )

    serialize_rules = ('-signups.camper',)

    @validates('age')
    def validate_age(self, key, age_value):
        if not (8 <= age_value <= 18):
            raise ValueError("Incorrect age")
        return age_value
    
    @validates('name')
    def validate_name(self, key, name_value):
        if not name_value:
            raise ValueError('Name must exist')
        return name_value
    
    def __repr__(self):
        return f'<Camper {self.id}: {self.name}>'


class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer)

    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))

    camper = db.relationship('Camper', back_populates='signups')
    activity = db.relationship('Activity', back_populates='signups')

    serialize_rules = ('-camper.signups', '-activity.signups',)

    @validates('time')
    def validate_age(self, key, time_value):
        if not (0 <= time_value <= 23):
            raise ValueError("Time outside of reality")
        return time_value
    
    def __repr__(self):
        return f'<Signup {self.id}>'


# add any models you may need.
