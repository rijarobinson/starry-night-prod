from flask import Flask, render_template, request, redirect, jsonify, url_for, flash  # noqa
app = Flask(__name__)

from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, State, Site, User

from flask import session as login_session
import random
import string

import httplib2
import json
from flask import make_response
import requests

# Connect to Database and create database session
engine = create_engine('postgresql://catalog:70075u173!@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

states = [["AL", "Alabama"], ["AK", "Alaska"], ["AZ", "Arizona"],
          ["AR", "Arkansas"], ["CA", "California"], ["CO", "Colorado"],
          ["CT", "Connecticut"], ["DC", "District of Columbia"],
          ["DE", "Delaware"], ["FL", "Florida"], ["GA", "Georgia"],
          ["HI", "Hawaii"], ["ID", "Idaho"], ["IL", "Illinois"],
          ["IN", "Indiana"], ["IA", "Iowa"], ["KS", "Kansas"],
          ["KY", "Kentucky"], ["LA", "Louisiana"], ["ME", "Maine"],
          ["MD", "Maryland"], ["MA", "Massachusetts"], ["MI", "Michigan"],
          ["MN", "Minnesota"], ["MS", "Mississippi"], ["MO", "Missouri"],
          ["MT", "Montana"], ["NE", "Nebraska"], ["NV", "Nevada"],
          ["NH", "New Hampshire"], ["NJ", "New Jersey"],
          ["NM", "New Mexico"], ["NY", "New York"],
          ["NC", "North Carolina"], ["ND", "North Dakota"],
          ["OH", "Ohio"], ["OK", "Oklahoma"], ["OR", "Oregon"],
          ["PA", "Pennsylvania"], ["RI", "Rhode Island"],
          ["SC", "South Carolina"], ["SD", "South Dakota"],
          ["TN", "Tennessee"], ["TX", "Texas"],
          ["UT", "Utah"], ["VT", "Vermont"], ["VA", "Virginia"],
          ["WA", "Washington"], ["WV", "West Virginia"],
          ["WI", "Wisconsin"],
          ["WY", "Wyoming"]]
for r in range(0, len(states)):
    newState = State(name=states[r][1],
                     abbrev=states[r][0],
                     user_id=1)
    session.add(newState)
    session.commit()
