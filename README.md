#Starry Night Production Site Database (Udacity Linux Configuration Project)
###(In fullfillment of Udacity's Full Stack Developer Program)

[http://ec2-35-166-167-209.us-west-2.compute.amazonaws.com/](http://ec2-35-166-167-209.us-west-2.compute.amazonaws.com/)

[http://35.166.167.209/](http://35.166.167.209/)

ssh port 2200

-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA1BF8lfdA4dtt+0J9Li0+DYLX+ZsXFvG4CKOFziH6GRK6KPe1
XgIKx7IZ9ZQKOnAo10V3teXaCWzUoKEJN0Xr2M0Y2xAnit4Eux8fVJfOcdwpX0DB
HgZENUNCgPogUCntHX/0ujCRgzawpiV0g09P72ilO801yOOhtHcMrZWa2Q+WnOAO
jpVgez3Pc+dSxRCdUClr309qu4hyiS1Ubnu46196sPsH531SZoNoJnRI3abG8G2c
UtgvpWtBWDAYz9LuU+GFOo6u48EV8/rT8KHl5hCMWJGVdIPqKSL3z9PI8sa97AXw
RXFel8YKpp9v00TjiUZDjd5yqBeZi3CcmGWd8QIDAQABAoIBAQC7uML9CULg61m+
6gtffeMJGMLQDC5zPAN5ei7u2nrGCSLLMwLUNaCPRyPdlG89bZ1pee/PD6ljYHgT
vJko2Xc9kcgn2nP2ZDPx5Enamwq/FXF2BR8t0cQ9Fc3f2AoUjBh+XY8n5ehZK2dR
m6Q4vFN5DLv/ZNbwfjfdROjvG5hX/OzHjzzzgxcAIesOkC7OCRTRFYMRbG5AiQXJ
xgmrxQVYsUcqZwvAbKDCDmUu3jdbO0mlNuRWsfgAa9XyY5DnUqhTktkp9p61tjx7
AVv/z3UDUC0oQlKpznq9sJAfB0LqpVYkypRBhAJRWCDpPzu60vvez/AsGtkt7ENL
oWdZEHKlAoGBAPEycKgJIWgSEa+te3+XBP9cr8npVoqeQDWmJtqZhR6xkGcnPYu3
b8+NyWYKm9tU727hQJUt1UZZoYkofJPRw/pNWFUKj42a/TiHUWotJLJna28I2GVE
16srycg3s5mKCi+1nN0d1JQRylYt3xX7vthQfFn0JDXsMrRUYIj/cT/DAoGBAOEV
ZDq6z/0A6nKQ5I/hFQjZu9m8Cwf5s1XNaqPjArcPcpfpDAcmNMViXZ3GECte81ht
gGoKsAkowELe9lrDKsTH8aP1Tqi1Er0Rl02PhrqrMiDDxOnT8XjBxQ/pgCRQ1M4H
qrXt7nkMV6Ghu4F7WslVzKF/3253nyZpCyXFkaQ7AoGBAMYFAEKkxF15wDV3+1Vj
+kFgqh3dySQjClpBX9LGiWkKpKBbsga8AjrnkDqLaSvoDm781ZXkPB32xk0iBS0i
4X/k8ilXc0XxwgUf63J9P4yMpcJSA78YhuvMFmyfdn8OupAyzWcn73flJzYbkPSu
ax+S7JS5gOUYVwR/5YV0GlkbAoGARZpB1k9yhcBEv4zCwSNPR99c0aXum1bB+CR/
d5J5gnZKb2NnjsZnxyn13RYkZeUExzGFZkVLzmlFmugrskFr9lIGDTeMTWtBEipg
aWGavhq2c59WQyCBKWByOctxDsnYJKYGSh/7gH8qkhbbTt0AZAYeM0rBov1mv4/4
HIQN14UCgYBY0mx0IZSIhRM2qKkIZKVzBrBYsO7EDPL65ooQVe7nzTAeBn78EgTW
4ivEGPrG9GHg9AQfumk8/n3c8z3F4gDFJiF0TWEVGV9+XRVB8TZ9p9wWUp3CEsTo
HxbWY4ShIn9XbG71eP1P3WRG4a9+O0zoFqWljC3Yn0STbaTCx2AMpQ==
-----END RSA PRIVATE KEY-----



The Starry Night Database was developed as part of Udacity's Full Stack Developer Nanodegree. It contains the front and back end code for a system designed to share data on great stargazing sites. This version is configured to run on AWS.

The purpose of this project was to develop a database and functions that would pass the requirements of the Linux Configuration project.

##Table of Contents
 * [Functionality](#functionality)
 * [Structure Overview](#structure-overview)
 * [Technologies](#technologies)
 * [Folders & Files](#folders-files)
 * [Libraries & Modules](#libraries-modules)
 * [Using the Software](#using-software)

<a id="functionality"></a>
##Functionality
The *Starry Night Database* contains functionality for adding, editing, and deleting sites (as well as states for Administrator privilige) for logged in users (restricted to record creator). The database also contains a State table that is loaded upon initilization, and the administrator is automatically designated with the first user. There is a mapping component that will translate addresses to latitude and longitude and provide a map for each site. Commonly used queries are stored as Python functions. The application has the ability to browse data without being logged in. The site utilizes Google and Facebook login APIs for authorization/authentication.
<a id="structure-overview"></a>
##Structure Overview

| Table         | Description                               | Key(s)                                    |
| ------------- | ----------------------------------------- | ----------------------------------------- |
| User (t)      | User data stored from logins              | id                                        |
| State (t)     | Manually loaded on initialization of app  | id, user_id (foreign)                     |
| Site (t)      | Data on location and description of sites | id, state_id (foreign), user_id (foreign) |
<a id="technologies"></a>
##Technologies

| Tool Used  | Purpose                                         | Notes                                       | About         |
| ---------- | ----------------------------------------------- | ------------------------------------------- | ------------- |
| AWS        | hosting platform                                | Runs Linux/Ubuntu                           | [More info](https://aws.amazon.com/) |
| Ubuntu     | Linux distribution provides OS                  |                                             | [More info](https://www.ubuntu.com/server) |
| Apache     | Web application server                          |                                             | [More info](https://httpd.apache.org/)
| GitHub     | provide configuration instructions for VM       | Fork & clone Udacity repo (link below)      | [More info](https://en.wikipedia.org/wiki/GitHub) |
| Git Bash   | run commands from VM                            | Provides Unix-Style terminal                | [More info](https://en.wikipedia.org/wiki/Bash_(Unix_shell)) |
| SQLite     | database for persistant data storage            | Runs on Virtual Machine (VM)                | [More info](https://sqlite.org/) |
| SQLAlchemy | allows interaction with the SQLite DB           | Run commands in Python file                 | [More info](http://www.sqlalchemy.org/) |
| Python     | language used to program functions              | Python files detailed below                 | [More info](https://www.python.org/about/) |
| Flask      | Python Microframework                           | Allows use of templates and Jinja2 commands | [More info](http://flask.pocoo.org/) |
| Google Maps API | Interface for utilizing Google Maps        | Translate address to geocode and get maps   | [More info](https://developers.google.com/maps/) |
| Google Oauth API | Interface for utilizing Google Login      | Allows secure Login using G+ account        | [More info](https://developers.google.com/maps/) |
| Facebook Oauth API | Interface for utilizing Facebook Login  | Allows secure Login using FB account        | [More info](https://developers.google.com/maps/) |
| JavaScript | Language for client-side scripts                | See code for script functions               | [More info](https://www.javascript.com/) |
| Bootstrap | Framework for front end                          |                                             | [More info](http://getbootstrap.com/) |
| CSS       | Language for styling web pages                   |                                             | [More info](http://www.w3schools.com/css/css_intro.asp) |
| HTML      | Language for structuring web pages               |                                             | [More info](http://www.w3schools.com/html/html_intro.asp) |
| JSON      | Data Interchange Format                          | App creates and utilizes JSON datasets      | [More info](http://www.json.org/) |

<a id="folders-files"></a>
##Folders & Files

| File                          | Purpose                                   | Notes                                       |
| ----------------------------- | ----------------------------------------- | ------------------------------------------- |
| database_setup.py             | db schema                                 | Run once to create database objects         |
| add_states.py                 | run to add state data to appliction       | Run once to create state data               |
| client_secrets.json           | file used by G+ login API                 |  |
| fb_client_secrets.py          | file used by FB login API                 |  |
| main.py                       | core code for application                 | Run to start up web server application (local port 8000) |
| templates/addState.html       | add a state (admin only)                  |  |
| templates/deleteSite.html     | delete a site (site owner only)           |  |
| templates/deleteState.html    | delete a state (admin only)               |  |
| templates/editSite.html       | edit site (site owner only can edit)      |  |
| templates/editState.html      | edit a state (admin only)                 |  |
| templates/header.html         | displays main screen and log in/out links |  |
| templates/login.html          | login screen                              |  |
| templates/main.html           | main template                             |  |
| templates/newsite.html        | add a site with state already attached    |  |
| templates/newsitenostate.html | add site and assign a state               |  |
| templates/singleSite.html     | displays information on a single site     |  |
| templates/site.html           | shows sites within a state                |  |
| templates/states.html         | main page                                 |  |
| static/green_6in.jpg          | Login screen image                        |  |
| static/styles.css             | CSS file with styles                      |  |
| static/sun_290ppi.jpg         | App header image                          |  |

<a id="libraries-modules"></a>
##Libraries & Modules
| Library or Module | Purpose                                                        |
| ----------------- | -------------------------------------------------------------- |
| oauth2client      | Python library for accessing resources protected by OAuth 2.0  |
| httplib2          | python library to interact with the web                        |
| flask             | Python framework (see above in [Technologies](#technologies))  |
| sqlalchemy        | allows for SQL queries                                         |
| random            | generates numbers (used in login route)                        |
| string            | allows for use of string functions                             |
| json              | provides tools for working with JSON data                      |
| requests          | allows for getting info from http request                      |
| psycopg2          | postgresql dialect                                             |

<a id="using-software"></a>
##Using the Software
**To use the software**

1.  Create your Virtual Machine with Amazon Web Services.
2.  Create a new user and grant sudo permissions (information on this step can be found in the Udacity Course, [Configuring Linux Web Severs](https://www.udacity.com/course/configuring-linux-web-servers--ud299)).
3.  Update all currently installed packages (see above for link on how).
4.  Configure the local timezone to UTC (use sudo dpkg-reconfigure tzdata).
5.  Change SSH port to 2200.
6.  Configure firewall to only allow incoming for ssh (port 2200), http (port 80), and ntp (port 123). See step two for link to information on how to do this.
7.  Install and configure Apache to serve a Python mod_wsgi appliction. Helpful instructions at [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-deploy-a-flask-application-on-an-ubuntu-vps).
8.  Pip install postgresql and sqlalchemy and any other modules needed (see list of modules above).
9.  Configure postgresql to not allow remote connections and create a new user that has limited permissions (CRUD).
10.  Install git on the remote server and clone this project to the project folder on the remote server. Info on doing this on the [GitHub Site](https://github.com/rijarobinson/starry-night-prod). You'll need to replace keys in the application with your own keys.
11.  Type "python database_setup.py" to add the database and tables (you must be in the main app directory).
12.  Login to the database from a browser using either Google or Facebook to create the Admin user.
13.  Return to the terminal and type "python add_states.py" to add the states to the database.

**To customize the files**
Feel free to modify your copy of the template files to customize to a different use. You will need to get your own API key for use of Google and Facebook login and the Maps APIs.

Instructions for this project were provided by [Udacity](http://www.Udacity.com). Additional instruction on Full Stack Application Development is available by signing up for a class on their site. No code was directly copied and pasted, but resources such as [DigitalOcean](http://www.digitalocean.com), the fabulous Udacity forums, [Google Searches](http://www.google.com), and [Stack Overflow](http://www.stackoverflow.com) and Udacity's instructional videos were used for guidance.

Images on the app were retrieved from the [NASA Gallery](https://www.nasa.gov/multimedia/imagegallery/).

I welcome any feedback on this project at marija@springmail.com.
