from flask import Flask, render_template, request
# from debugger import initialize_flask_server_debugger_if_needed
from os import getenv
from demo9_meets_demo5 import Demo
from actors import Actor
from api import API

from datetime import datetime
import re

app = Flask(__name__)

@app.route('/')
def student():
   actors = ["Ricky Whittle", "Lyriq Bent", "Lynn Whitfield", "Ernie Hudson", "Daria Johns",
    "Camille Guaty", "Brittany S. Hall", "Terry Serpico", "Jen Harper", "Danielle Lyn", "George Wallace", 
    "John Salley", "RonReaco Lee", "Bo Yokely"]
   return render_template('actor.html',actors=["ll"])

@app.route('/result',methods = ['POST', 'GET'])
def result():
   if request.method == 'POST':
      result = request.form
      return render_template("result.html",result = result)


@app.route('/actor/<string:url_frag>')
def profiles(url_frag):
   pass


@app.route('/actordemo',methods = ['GET'])
def actordemo():
   t = Demo
   t.including()
   actors = ["Ricky Whittle", "Lyriq Bent", "Lynn Whitfield", "Ernie Hudson", "Daria Johns",
    "Camille Guaty", "Brittany S. Hall", "Terry Serpico", "Jen Harper", "Danielle Lyn", "George Wallace", 
    "John Salley", "RonReaco Lee", "Bo Yokely"]
   return render_template('actor.html',actors=actors)

@app.route('/create_actor',methods = ['GET'])#post
def create_actor():
   uid = "nm0005125"
   name = "Sanaa Lanthan"
   # resource = API.retrieve(API, "/actors/get-all-filmography", {"nconst": uid})
   # resource = API.retrieve( "/actors/get-all-filmography", {"nconst": uid})
   with open('sanaaFilms2.txt') as f: resource = f.read()

   titles = Actor.parse_filmography(resource)
   a = Actor(uid, name)
   a.create(titles)

   t = Demo
   t.including()
   actors = ["Ricky Whittle", "Lyriq Bent", "Lynn Whitfield", "Ernie Hudson", "Daria Johns",
    "Camille Guaty", "Brittany S. Hall", "Terry Serpico", "Jen Harper", "Danielle Lyn", "George Wallace", 
    "John Salley", "RonReaco Lee", "Bo Yokely"]
   return render_template('actor.html',actors=actors)


# print(f"__name__ is {__name__ }")
# print(f"__main__ is {__main__ }")
# if __name__ == '__main__':
# print("hello1")
# print( getenv("DEBUGGER"))
if getenv("DEBUGGER") == "True" or  __name__ == '__main__':
   # print("hello?")
   # app.run(debug = True)
   app.run()