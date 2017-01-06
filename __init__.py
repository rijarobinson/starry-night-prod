from flask import Flask, render_template, request, redirect, jsonify, url_for, flash, g  # noqa
from sqlalchemy import create_engine, asc, desc
from sqlalchemy.orm import sessionmaker
from database_setup import Base, State, Site, User
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
from oauth2client.client import AccessTokenCredentials
import httplib2
import json
from flask import make_response
import requests
from functools import wraps

app = Flask(__name__)

CLIENT_ID = (json.loads(open('/var/www/FlaskApp/StarryNight/client_secrets.json', 'r')
                        .read())['web']['client_id'])


# Connect to Database and create database session
engine = create_engine('postgresql+psycopg2://catalog:70075u173!@localhost/catalog')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state, result="")


@app.route('/gconnect', methods=['POST'])
def gconnect():
    # Validate state token
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Obtain authorization code
    code = request.data
    try:
        # Upgrade the authorization code into a credentials object
        oauth_flow = flow_from_clientsecrets('/var/www/FlaskApp/StarryNight/client_secrets.json', scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(
            json.dumps('Failed to upgrade the authorization code.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Check that the access token is valid.
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Verify that the access token is valid for this app.
    if result['issued_to'] != CLIENT_ID:
        response = make_response(
            json.dumps("Token's client ID does not match app's."), 401)
        print "Token's client ID does not match app's."
        response.headers['Content-Type'] = 'application/json'
        return response

    stored_credentials = login_session.get('credentials')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_credentials is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already ' +
                                            'connected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response

    # Store the access token in the session for later use.
    login_session['provider'] = 'google'
    login_session['credentials'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()
    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    userIDInDB = getUserID(login_session['email'])
    if not userIDInDB:
        createUser(login_session)
    # this is the ID (serial number) of the user
    login_session['user_id'] = userIDInDB
    # code to check to make sure record added in db
    userInfo = getUserInfo(userIDInDB)
    verifyUserData = (userInfo.email + " " + userInfo.name + " " + str(userInfo.id))  # noqa

    output = '<div class="row"><div class="col-md-12 text-center"'
    output += '<h3>Welcome, '
    output += login_session['username']
    output += '!</h3>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style="width: 50px; height: 50px; border-radius: '
    output += '25px;-webkit-border-radius: 25px;-moz-border-radius: 25px;">'
    output += '</div></div>'
    flash("You are now logged in as %s" % login_session['username'])
    print "done!"
    return output


# DISCONNECT - Revoke a current user's token and reset their login_session
@app.route('/gdisconnect/')
def gdisconnect():
    credentials = login_session.get('credentials')
    if credentials is None:
        response = make_response(json.dumps("Current user not connected."),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    my_access_token = credentials
    if my_access_token is None:
        print 'Access token is None'
        response = make_response(json.dumps("Current user is not connected."),
                                 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    url = ('https://accounts.google.com/o/oauth2/revoke?token=%s'
           % my_access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]

    if result['status'] == '200':
        del login_session['credentials']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']

        response = make_response(json.dumps('Successfully disconnected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token' +
                                            ' for given user</br>Status: %s'
                                            % result['status']), 400)
        response.headers['Content-Type'] = 'application/json'
        return response


@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token

    app_id = json.loads(open('/var/www/FlaskApp/StarryNight/fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('/var/www/FlaskApp/StarryNight/fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token)  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.4/me"
    # strip expire tag from access token
    token = result.split("&")[0]

    url = 'https://graph.facebook.com/v2.4/me?%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly
    # logout, strip out the information before the equals sign in our token
    stored_token = token.split("=")[1]
    login_session['access_token'] = stored_token

    # Get user picture
    url = 'https://graph.facebook.com/v2.4/me/picture?%s&redirect=0&height=200&width=200' % token  # noqa
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = '<div class="row"><div class="col-md-12 text-center"'
    output += '<h3>Welcome, '
    output += login_session['username']
    output += '!</h3>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style="width: 50px; height: 50px; border-radius: 25px;'
    output += '-webkit-border-radius: 25px;-moz-border-radius: 25px;">'
    output += '</div></div>'

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id, access_token)  # noqa
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"


@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            login_session['gplus_id'] = ""
            login_session['credentials'] = ""
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        login_session['username'] = ""
        login_session['email'] = ""
        login_session['picture'] = ""
        login_session['user_id'] = ""
        login_session['provider'] = ""
        flash("You have successfully been logged out.")
        return redirect(url_for('showStates'))
    else:
        flash("You were not logged in")
        return redirect(url_for('showStates'))

def logged_in(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if login_session['username'] is not "":
            return f(*args, **kwargs)
        else:
            flash("Log in for privileged access.")
            return redirect(url_for('showLogin'))
    return decorated_function


def admin_access(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if login_session['user_id'] == 1:
            return f(*args, **kwargs)
        else:
            flash("Only the admin can add states.")
            return redirect(url_for('showStates'))
    return decorated_function


# JSON APIs to view sites in State List
@app.route('/state/<int:state_id>/site/JSON')
def stateSiteJSON(state_id):
    state = filterStatesById(state_id)
    sites = session.query(Site).filter_by(state_id=state_id).all()
    return jsonify(Sites=[s.serialize for s in sites])


# JSON APIs to view single site
@app.route('/state/<int:state_id>/site/<int:site_id>/JSON')
def siteJSON(state_id, site_id):
    sites = filterSitesById(site_id)
    return jsonify(Site=sites.serialize)


# JSON API to view all states
@app.route('/states/JSON')
def statesJSON():
    states = session.query(State).all()
    return jsonify(states=[s.serialize for s in states])


# JSON API to view all sites
@app.route('/sites/JSON')
def sitesJSON():
    sites = session.query(Site).all()
    return jsonify(sites=[s.serialize for s in sites])


# Show all states and 5 newly created sites
@app.route('/')
@app.route('/state/')
def showStates():
    states = allStates()
    front = session.query(Site).order_by(desc(Site.id)).limit(5).all()
    session.commit()
    siteList = []
    for a in front:
        siteList.append(a.state_id)
    try:
        currentUserID = login_session['user_id']
        if currentUserID:
            return render_template('states.html', states=states,
                                   sites=siteList,
                                   currentUserID=currentUserID,
                                   allSites=front,
                                   jsSites=[s.serialize for s in front],
                                   jsStates=[s.serialize for s in states])
        else:
            return render_template('states.html', states=states,
                                   sites=siteList, allSites=front,
                                   jsSites=[s.serialize for s in front],
                                   jsStates=[s.serialize for s in states],
                                   currentUserID="")
    except:
        return render_template('states.html', states=states,
                               sites=siteList, allSites=front,
                               jsSites=[s.serialize for s in front],
                               jsStates=[s.serialize for s in states],
                               currentUserID="")


# only Administrator can add new states
@app.route('/state/new/', methods=['GET', 'POST'])
@logged_in
@admin_access
def addState():
    currentUserID = login_session['user_id']
    if request.method == 'POST':
        user_id = login_session['user_id']
        name = request.form['name']
        abbrev = request.form['abbrev']
        newState = State(name=name, abbrev=abbrev, user_id=user_id)
        session.add(newState)
        flash('New State %s Successfully Created' % newState.name)
        session.commit()
        return redirect(url_for('showStates'))
    else:
        return render_template('addState.html', currentUserID=currentUserID)


# Edit a state
@app.route('/state/<int:state_id>/edit/', methods=['GET', 'POST'])
@logged_in
@admin_access
def editState(state_id):
    currentUserID = login_session['user_id']
    allowedToEdit = thisStateOwner(login_session['user_id'], state_id)
    if allowedToEdit:
        editedState = filterStatesById(state_id)
        if request.method == 'POST':
            if request.form['name']:
                editedState.name = request.form['name']
            if request.form['abbrev']:
                editedState.abbrev = request.form['abbrev']
            flash('State Successfully Edited %s' % editedState.name)
            return redirect(url_for('showStates'))
        else:
            return render_template('editState.html', state=editedState,
                                   currentUserID=currentUserID)
    else:
        flash("Only the owner can edit this state.")
        return redirect('/state/')


# Delete a state
# Administrator only can delete/edit states.
# States cannot be deleted if there are sites
# related to the state.
@app.route('/state/<int:state_id>/delete/', methods=['GET', 'POST'])
@logged_in
@admin_access
def deleteState(state_id):
    currentUserID = login_session['user_id']
    allowedToDelete = thisStateOwner(login_session['user_id'], state_id)
    if stateHasSites(state_id):
        flash('The state has sites attached to it. Please remove sites ' +
              'before deleting the state info.')
        return redirect('/state/')
    else:
        if allowedToDelete:
            stateToDelete = (session.query(State).filter_by(id=state_id)
                             .one())
            session.commit()
            if request.method == 'POST':
                session.delete(stateToDelete)
                flash('%s Successfully Deleted' % stateToDelete.name)
                session.commit()
                return redirect(url_for('showStates', state_id=state_id,
                                        currentUserID=currentUserID))
            else:
                return render_template('deleteState.html',
                                       state=stateToDelete,
                                       currentUserID=currentUserID)
        else:
            flash('Only the owner can delete this state.')
            return redirect('/state/')


# Show a state's sites
# Anybody can add a site
@app.route('/state/<int:state_id>/')
@app.route('/state/<int:state_id>/site/')
def showSite(state_id):
    state = filterStatesById(state_id)
    sites = session.query(Site).filter_by(state_id=state_id).all()
    session.commit()
    creator = ""
    try:
        currentUserID = login_session['user_id']
        if not currentUserID:
            return render_template('site.html', sites=sites, state=state,
                                   creator=creator, currentUserID="",
                                   jsSites=[s.serialize for s in sites],
                                   jsStates=[state.serialize])
        else:
            creator = getUserID(login_session['email'])
            return render_template('site.html', sites=sites, state=state,
                                   creator=creator,
                                   currentUserID=currentUserID,
                                   jsSites=[s.serialize for s in sites],
                                   jsStates=[state.serialize])
    except:
        return render_template('site.html', sites=sites, state=state,
                               creator=creator, currentUserID="",
                               jsSites=[s.serialize for s in sites],
                               jsStates=[state.serialize])


@app.route('/state/<int:state_id>/site/<int:site_id>/',
           methods=['GET', 'POST'])
def showSingleSite(state_id, site_id):
    state = filterStatesById(state_id)
    site = filterSitesById(site_id)
    creator = ""
    try:
        currentUserID = login_session['user_id']
        if not currentUserID:
            return render_template('singleSite.html', site=site,
                                   state=state, creator=creator,
                                   currentUserID="",
                                   jsSites=[site.serialize],
                                   jsStates=[state.serialize])
        else:
            creator = getUserID(login_session['email'])
            return render_template('singleSite.html', site=site,
                                   state=state, creator=creator,
                                   currentUserID=currentUserID,
                                   jsSites=[site.serialize],
                                   jsStates=[state.serialize])
    except:
        return render_template('singleSite.html', site=site, state=state,
                               creator=creator, currentUserID="",
                               jsSites=[site.serialize],
                               jsStates=[state.serialize])


# Create a new site
@app.route('/state/<int:state_id>/site/new/', methods=['GET', 'POST'])
@logged_in
def newSite(state_id):
    currentUserID = login_session['user_id']
    # Any logged in user can add a site to a state
    state = filterStatesById(state_id)
    state_name = state.name
    if request.method == 'POST':
        newSite = Site(name=request.form['name'],
                       notes=request.form['notes'],
                       city=request.form['city'],
                       site_type=request.form['site_type'],
                       phone=request.form['phone'],
                       website=request.form['website'],
                       state_id=state_id,
                       user_id=login_session['user_id'])
        session.add(newSite)
        session.commit()
        flash('New Site (%s) Successfully Created' % (newSite.name))
        return redirect(url_for('showSite', state_id=state_id,
                                currentUserID=currentUserID))
    else:
        return render_template('newsite.html', state_id=state_id,
                               state_name=state_name,
                               currentUserID=currentUserID)


# Create a new site from the state page
@app.route('/state/site/new/', methods=['GET', 'POST'])
@logged_in
def newSiteNoState():
    currentUserID = login_session['user_id']
    # Any logged in user can add a site
    states = allStates()
    state_list = []
    for state in states:
        state_list.append(state.name)
    if request.method == 'POST':
        state_name = request.form['state']
        state = filterStatesByName(state_name)
        state_link = state.id
        newSite = Site(name=request.form['name'],
                       notes=request.form['notes'],
                       city=request.form['city'],
                       site_type=request.form['site_type'],
                       phone=request.form['phone'],
                       website=request.form['website'],
                       state_id=state_link,
                       user_id=login_session['user_id'])
        session.add(newSite)
        session.commit()
        flash('New Site (%s) Successfully Created' % (newSite.name))
        return redirect(url_for('showSite', state_id=state_link,
                                currentUserID=currentUserID))
    else:
        return render_template('newsitenostate.html', state_list=state_list,
                               currentUserID=currentUserID)


# Edit a site
@app.route('/state/<int:state_id>/site/<int:site_id>/edit/',
           methods=['GET', 'POST'])
@logged_in
def editSite(state_id, site_id):
    currentUserID = login_session['user_id']
    allowedToEdit = thisSiteOwner(login_session['user_id'], site_id)
    if allowedToEdit:
        editedSite = filterSitesById(site_id)
        state = filterStatesById(state_id)
        states = allStates()
        state_list = []
        for s in states:
            state_list.append(s.name)
        state_name = state.name
        if request.method == 'POST':
            state_name = request.form['state']
            state = filterStatesByName(state_name)
            state_link = state.id
            if request.form['name']:
                editedSite.name = request.form['name']
            if request.form['notes']:
                editedSite.notes = request.form['notes']
            if request.form['site_type']:
                editedSite.site_type = request.form['site_type']
            if request.form['city']:
                editedSite.city = request.form['city']
            if request.form['state']:
                editedSite.state_id = state_link
            if request.form['phone']:
                editedSite.phone = request.form['phone']
            if request.form['website']:
                editedSite.website = request.form['website']
            session.add(editedSite)
            session.commit()
            flash('Site Successfully Edited')
            return redirect('/state/%s/site/' % state_id)
        else:
            return render_template('editSite.html', state_id=state_id,
                                   site_id=site_id, site=editedSite,
                                   state_name=state_name,
                                   state_list=state_list,
                                   currentUserID=currentUserID)
    else:
        flash("Only the owner can edit this site.")
        return redirect('/state/%s/site/' % state_id)


# Delete a site
@app.route('/state/<int:state_id>/site/<int:site_id>/delete',
           methods=['GET', 'POST'])
@logged_in
def deleteSite(state_id, site_id):
    currentUserID = login_session['user_id']
    allowedToDelete = thisSiteOwner(login_session['user_id'], site_id)
    if allowedToDelete:
        state = filterStatesById(state_id)
        siteToDelete = filterSitesById(site_id)
        if request.method == 'POST':
            session.delete(siteToDelete)
            session.commit()
            flash('Viewing Site Successfully Deleted')
            return redirect(url_for('showSite', state_id=state_id))
        else:
            return render_template('deleteSite.html', site=siteToDelete,
                                   currentUserID=currentUserID)
    else:
        flash("Only the owner can delete this site.")
        return redirect('/state/%s/site/' % state_id)


def getUserID(email):
   try:
       user = session.query(User).filter_by(email=email).one()
       session.commit()
       return user.id
   except:
       return None


def getUserInfo(user_id):
        user = session.query(User).filter_by(id=user_id).first()
        session.commit()
        return user


def createUser(login_session):
    newUser = User(name=login_session['username'],
    	  	   email=login_session['email'],
                   picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    session.commit()
    return user.id


def allStates():
    allStates = session.query(State).order_by(asc(State.name)).all()
    session.commit()
    return allStates


def filterStatesById(state_id):
    filterById = session.query(State).filter_by(id=state_id).first()
    session.commit()
    return filterById


def filterStatesByName(state_name):
    filterByName = session.query(State).filter_by(name=state_name).first()
    session.commit()
    return filterByName

def thisStateOwner(user_id, state_id):
    thisStateOwned = session.query(State).filter_by(user_id=user_id).all()
    session.commit()
    stateList = []
    for s in thisStateOwned:
        stateList.append(s.id)
    if state_id in stateList:
        return True
    else:
        return False

def filterSitesById(site_id):
    filterSiteById = session.query(Site).filter_by(id=site_id).first()
    session.commit()
    return filterSiteById

def thisSiteOwner(user_id, site_id):
    thisSiteOwned = session.query(Site).filter_by(user_id=user_id).all()
    session.commit()
    siteList = []
    for s in thisSiteOwned:
        siteList.append(s.id)
    if site_id in siteList:
        return True
    else:
        return False

def stateHasSites(state_id):
    hasSites = session.query(Site).filter_by(state_id=state_id).first()
    session.commit()
    return hasSites


if __name__ == '__main__':
    app.secret_key = 'super_secret_key'
    app.debug = True
    app.run(host='0.0.0.0', port=8000)
