from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    name = Column(String(150), nullable=False)
    email = Column(String(30))
    picture = Column(String(250))

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
           'email'        : self.email,
           'picture'      : self.picture,
       }


class State(Base):
    __tablename__ = 'state'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    abbrev = Column(String(2), nullable=False)
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'         : self.name,
           'id'           : self.id,
           'abbrev'       : self.abbrev,
       }


class Site(Base):
    __tablename__ = 'site'

    name =Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)
    notes = Column(String(250))
    city = Column(String(100))
    site_type = Column(String(100))
    phone = Column(String(12))
    website = Column(String(100))
    state_id = Column(Integer,ForeignKey('state.id'))
    state = relationship(State)
    user_id = Column(Integer,ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
       """Return object data in easily serializeable format"""
       return {
           'name'       : self.name,
           'notes'      : self.notes,
           'id'         : self.id,
           'city'       : self.city,
           'site_type'  : self.site_type,
           'phone'      : self.phone,
           'website'    : self.website,
           'state_id'   : self.state_id,
       }


engine = create_engine('postgresql://catalog:70075u173!@localhost/catalog')


Base.metadata.create_all(engine)
