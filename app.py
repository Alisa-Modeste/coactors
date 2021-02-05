from flask import Flask, render_template, request
# from debugger import initialize_flask_server_debugger_if_needed
from os import getenv
from demo9_meets_demo5 import Demo
from actors import Actor
from titles import Title
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

#remove
api_count = 0

@app.route('/create_actor',methods = ['GET'])#post
def create_actor():
   uid = "nm0005125"
   name = "Sanaa Lanthan"
   # resource = API.retrieve( "/actors/get-all-filmography", {"nconst": uid})
   with open('sanaaFilms2.txt') as f: resource = f.read()

   level = 1

   titles = Actor.parse_filmography(resource)
   a = Actor(uid, name)
   titles_added = a.create(titles)

   level += 1
   for title in titles_added:
      print(title['found']) #to do: delete
      if not title['found']:
        # t = Title(title['uid'], title['title'], self.level+1)
        #call API
        t = Title(title.uid, title.title, level)
        # t.create()

        level += 1
      #   for actor in cast_added:
		# 		# print(title['found']) #to do: delete
      #       if not actor['found']:
		# 		# t = Title(title['uid'], title['title'], self.level+1)
		# 		#call API
      #          a = Actor(actor.uid, actor.name, level)
		# 		# t.create()

   t = Demo
   t.including()
   actors = ["Ricky Whittle", "Lyriq Bent", "Lynn Whitfield", "Ernie Hudson", "Daria Johns",
    "Camille Guaty", "Brittany S. Hall", "Terry Serpico", "Jen Harper", "Danielle Lyn", "George Wallace", 
    "John Salley", "RonReaco Lee", "Bo Yokely"]
   return render_template('actor.html',actors=actors)

def get_actors_data(actors_attr):
    new_actors = []
    for actor in actors_attr:
        if 'found' not in actor or not actor['found']:
            # resource = API.retrieve( "/actors/get-all-filmography", {"nconst": actor['uid']})
            with open('sanaaFilms2.txt') as f: resource = f.read()
            titles = Actor.parse_filmography(resource)

            this_actor = {'titles': titles}
            this_actor['uid'] = actor['uid']
            this_actor['name'] = actor['name']
            new_actors.append(this_actor)

    return new_actors

def get_titles_data(titles_attr): #get_data_related_to_titles
    new_titles = []
    related_actors_data = []
    for title in titles_attr:
        if 'found' not in title or not title['found']:
            # resource = API.retrieve( "/actors/get-all-filmography", {"nconst": actor['uid']})
            with open('sanaaFilms2.txt') as f: resource = f.read()
            cast_uids = Title.parse_filmography(resource) #uids, no names

            for actor_uid in cast_uids:
                related_actors_data.append( get_actors_data(actor_uid) )

            this_title = {'cast': cast}
            this_title['uid'] = title['uid']
            this_title['name'] = title['name']
            new_titles.append(this_title)

    return new_titles


# print(f"__name__ is {__name__ }")
# print(f"__main__ is {__main__ }")
# if __name__ == '__main__':
# print("hello1")
# print( getenv("DEBUGGER"))
if getenv("DEBUGGER") == "True" or  __name__ == '__main__':
   # print("hello?")
   # app.run(debug = True)
   app.run()