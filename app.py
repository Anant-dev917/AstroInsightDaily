from datetime import datetime, timedelta
from dateutil import parser
import os
from flask import Flask,render_template, request, redirect, url_for, session, flash, jsonify
from pymongo import MongoClient
import requests
from dotenv import load_dotenv

#you must create a .env file to store your mongodb connection URI
load_dotenv()

#NASA API
API_KEY='Get your API Key from the NASA open APIs website'
response = requests.get(f'https://api.nasa.gov/planetary/apod?api_key={API_KEY}')

#Spaceflight API
curdate = datetime.today()
yesterday = curdate - timedelta(3)
SFURL = f'https://api.spaceflightnewsapi.net/v4/articles/?news_site=NASA%2C%20Reuters%2C%20Planetary%20society%2C%20Space.com%2C%20SpaceFlight%20Insider%2C%20Spaceflight%20Now%2C%20The%20Space%20Devs%2C%20Phys%2C%20The%20Wall%20Street%20Journal%2C%20The%20National%2C%20SpaceNews&published_at_gte={yesterday}&ordering=-published_at'
SFAres = requests.get(SFURL)


#Checking if the API servers are up or not (200-> connection was successful)
#print(response.status_code)

print(SFAres.status_code)

#Printing the data corresponding to the API link we're using

#print(f"NASA API response\n--------------------------\n{response.json()}")

#print(f"\n\nSpaceflight API response\n-------------------------\n{SFAres.json()}")



def create_app():

    app = Flask(__name__)

    #You will need an account in mongodb atlas website, and need to set up a database in mongodb compass GUI
    Client = MongoClient(os.getenv("MONGODB_URI"))
    app.db = Client.Users

    #Secret key set for session; session won't work without one
    app.secret_key = 'Set your secret key'


    @app.route('/', methods = ["GET","POST"])
    def home():

        article = []

        for dict in SFAres.json()['results']:    
            title = dict['title']
            smr = dict['summary']
            image = dict['image_url']
            site = dict['news_site']
            pbl = parser.parse(dict['published_at'],)
            upd = parser.parse(dict['updated_at'])

            #dateutil parser returns datetime.datetime object, which was stored in pbl variable; So we can use it in tandem with strftime
            # and convert JSON date into any format 
            fpbl = pbl.strftime("%b %d, %Y %H:%M %Z")

            fupd = upd.strftime("%b %d, %Y %H:%M %Z")

            link = dict['url']
            
            article.append((title,smr,image,site,fpbl,fupd, link))

        return render_template("home.htm",articles=article)
    

    
    @app.route("/pics", methods = ["GET","POST"])
    def POD():
        date = response.json()['date']

        rfdate = datetime.strptime(date, "%Y-%m-%d").strftime("%b %d %Y")

        url = response.json()['url']

        media = response.json()['media_type']

        heading = response.json()['title']

        desc = response.json()['explanation']

        if media == 'image':
            hdlink = response.json()['hdurl']

        else:
            hdlink = '#'

        return render_template("Picture.html",date=rfdate, url=url, media=media, heading=heading, desc=desc, hdlink=hdlink)
    
    @app.route("/login",methods=["GET","POST"])
    def log():

        if 'fname' in session:
            return render_template("error.html",text=f"Already logged in as \"{session['uname']}\" ")
        
        else:

            if request.method == "POST":
                user = request.form.get("uname")
                pwd = request.form.get("pass")

                for urecord in app.db.uinfo.find({}):
                    if user==urecord["username"] and pwd==urecord["password"]:
                        session['fname'] = urecord["First_name"]
                        session['lname'] = urecord["Last_name"]
                        session['email'] = urecord["Email"]
                        session['pno'] = urecord["Phone_number"]
                        session['dob'] = urecord["Date_of_Birth"]
                        session['doj'] = urecord["Date_joined"]
                        session['uname'] = urecord["username"]
                        return render_template("Error.html",text=f"Log-in successful! Welcome {session['fname']}")
                                
                flash("Incorrect username or password! Please try again")
                return redirect(url_for('log'))

        
            return render_template("Login.html")
    
    
    
    @app.route("/signin",methods = ["GET","POST"])
    def sign():

        if request.method =="POST":
            name = request.form.get("fname")
            surname = request.form.get("lname")
            email = request.form.get("Email")
            pno = request.form.get("phno")
            DOB = request.form.get("dob")
            doj = datetime.today().strftime("%d-%m-%Y %H:%M %Z")
            usname = request.form.get("uname")
            pwd = request.form.get("pass")
            rpwd = request.form.get("pass_repeat")

            for data in app.db.uinfo.find({}):
                if usname == data['username']:
                    flash("Username already exists!")
                    return redirect(url_for('sign'))

            if pwd == rpwd:
                app.db.uinfo.insert_one({"First_name":name, "Last_name":surname, "Email":email, 
                                         "Phone_number":pno, "Date_of_Birth":DOB, "Date_joined":doj, 
                                         "username":usname, "password":pwd})

                return render_template("Error.html",text="Successfully signed-in")

                
                #data= [name,surname,usname,pwd,rpwd]
                #session['data'] = data
                #return redirect(url_for('testing'))

            else:
                flash("The passwords do not match!")
                return redirect(url_for('sign'))


        return render_template("signup.html")
    

    
    @app.route("/logout")
    def lgot():
        if 'fname' in session:
            for s in ['fname','lname','email','pno','dob','doj','uname']:
                session.pop(s,None)
                return render_template("logout.html")
            
        else:
            return render_template("logout.html")
        

    
    @app.route("/prof", methods=["GET","POST"])
    def profile():
        if 'fname' in session:
            udata = []
            access = []
            mudob = datetime.strptime(session['dob'],"%Y-%m-%d").strftime("%d-%m-%Y")
            

            udata.append((session['fname'], session['lname'], session['email'], session['pno'], mudob, session['doj']))

            for acrecord in app.db.laccess.find({}):
                if acrecord['user'] == session['uname']:
                    access.append((acrecord['user'], acrecord['News_link'], acrecord['Headline'], acrecord['source'] , acrecord['published_on'], 
                                    acrecord['updated_on'] , acrecord['summary'] ,acrecord['pic']))
                    
                    return render_template("profile.html",record = udata, lastac = access)    
                
            return render_template("profile.html",record = udata)
                
        else:
            return render_template("Error.html",text="You must log in to view this page")
        


    #Receiving JQuery data from 'home.htm' file here
    @app.route("/process",methods=['POST'])
    def process():

        data = request.get_json()
         #Inserting clicked link info into database
        if 'fname' in session:
            for acrecord in app.db.laccess.find({}):
                if acrecord['user'] == session['uname']:
                    query_filter = {'user':session['uname']}
                    update_operation = {'$set':
                                        {'News_link': data['link'], 'Headline': data['title'], 'source':data['source'], 'published_on':data['pubdate']
                                          ,'updated_on':data['update'],'summary':data['summary'],'pic': data['image'] }
                                        }
                    app.db.laccess.update_one(query_filter,update_operation)
                    return "success"
                    

            app.db.laccess.insert_one({'user':session['uname'], 'News_link': data['link'], 'Headline': data['title'], 'source':data['source'], 'published_on':data['pubdate']
                                          ,'updated_on':data['update'],'summary':data['summary'],'pic': data['image']})
            return "success"
        



        
    @app.route("/error")
    def err():

        return render_template("error.html")



    
    return app 
