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
   actor = get_actors_data([{'uid': uid, 'name': name}])
   level = 1
   a = Actor(actor[0]['uid'], actor[0]['name'], level)
   titles_added = a.create(actor[0]['data']['titles'])

   # titles = get_titles_data(titles_added) # cast_uids
   casts_uids = get_titles_data(titles_added) # cast_uids
   # new_titles = []
   actors = []
   for actor_uids in casts_uids:
      #  actors.append( get_actors_data(actor_uids) )
       actors += get_actors_data(actor_uids)

   for actor in actors:
       level = 2 #really 3. here: change class

       a = Actor(
          actor['data']['uid'], 
          actor['data']['name'], 
          level)

       a.create(actor['data']['titles'])

   # t = Demo
   # t.including()
   # actors = ["Ricky Whittle", "Lyriq Bent", "Lynn Whitfield", "Ernie Hudson", "Daria Johns",
   #  "Camille Guaty", "Brittany S. Hall", "Terry Serpico", "Jen Harper", "Danielle Lyn", "George Wallace", 
   #  "John Salley", "RonReaco Lee", "Bo Yokely"]
   return render_template('actor.html',actors=actors)

@app.route('/create_title',methods = ['GET'])#post
def create_title():
   uid = "tt0482571"
   title = "The Prestige"
   released = 2006

   cast_uids = get_titles_data([{'uid':uid, 'title': title, 'released': released}])
   actors = get_actors_data(cast_uids[0])

   for actor in actors:
       level = 2 #really 1? here:

       a = Actor(
          actor['data']['uid'], 
          actor['data']['name'], 
          level)

       a.create(actor['data']['titles'])

   return "Template here"


def get_actors_data(actors_attr):
    new_actors = []
    for actor in actors_attr['filmography'] if 'filmography' in actors_attr else actors_attr:
       uid = None
       if type(actor) == dict and (not 'found' in actor or not actor['found']):
           uid = actor['uid']
       elif type(actor) == Actor and (actor.found is None or not actor.found):
           uid = actor.uid

       if True: #uid
            # resource = API.retrieve( "/actors/get-all-filmography", {"nconst": actor['uid']})
           if 'name' in actor:#remove here:
               with open('sanaaFilms2.txt') as f: resource = f.read()
           else:
         #       resource = API.retrieve( "/actors/get-all-filmography", {"nconst": actor['uid']})
               with open('CuocoFilms2.txt') as f: resource = f.read()
           data = Actor.parse_filmography(resource)

           this_actor = {'data': data}
           this_actor['uid'] = actor['uid']
           this_actor['data']['uid'] = actor['uid']
           this_actor['name'] = actor['name'] if 'name' in actor else data['name']
           new_actors.append(this_actor)

       if not 'name' in actor:
           break

    return new_actors

def get_titles_data(titles_attr): #get_data_related_to_titles
    new_titles = []
   #  related_actors_data = []
    for title in titles_attr:
      #   if 'found' not in title or not title['found']:
      #   if title.found is None or not title.found:
        uid = None
        if type(title) == dict and (not 'found' in title or not title['found']):
            uid = title['uid']
        elif type(title) == Title and (title.found is None or not title.found):
            uid = title.uid

        if True: # uid:
            # resource = API.retrieve( "/title/get-top-cast", {"tconst": uid})
            with open('aCast2.txt') as f: resource = f.read()
            from pprintpp import pprint
            pprint(resource)
            cast_uids = Title.parse_cast(resource) #uids, no names

            # for actor_uid in cast_uids:
            #     related_actors_data.append( get_actors_data(actor_uid) )

            # this_title = {'cast_uids': cast_uids}
            # this_title['uid'] = title['uid']
            # this_title['title'] = title['title']
            new_titles.append(cast_uids)
            break#here: break

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