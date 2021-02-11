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
   # uid = "nm0005125"
   uid = "5411"
   name = "Sanaa Lathan"
   actor_data = get_actors_data([{'uid': uid, 'name': name}])
   level = 1
   a = Actor(actor_data[0]['uid'], actor_data[0]['name'], level)
   titles_added = a.create(actor_data[0]['titles'])

   # titles = get_titles_data(titles_added) # cast_uids
   casts = get_titles_data(titles_added) # cast_uids
   # # new_titles = []
   # actors = []
   for cast in casts:
      t = Title(cast['uid'],
         cast['title'],
         cast['released'],
         cast['title_type'])

      t.create(cast['cast'])
   #    #  actors.append( get_actors_data(actor_uids) )
   #     actors += get_actors_data(cast)

   # for actor in actors:
   #     level = 2 #really 3. here: change class

   #     a = Actor(
   #        actor['data']['uid'], 
   #        actor['data']['name'], 
   #        level)

   #     a.create(actor['data']['titles'])

   # t = Demo
   # t.including()
   actors = ["Ricky Whittle", "Lyriq Bent", "Lynn Whitfield", "Ernie Hudson", "Daria Johns",
    "Camille Guaty", "Brittany S. Hall", "Terry Serpico", "Jen Harper", "Danielle Lyn", "George Wallace", 
    "John Salley", "RonReaco Lee", "Bo Yokely"]
   return render_template('actor.html',actors=actors)

@app.route('/create_title',methods = ['GET'])#post
def create_title():
   uid = "1124"
   title = "The Prestige"
   released = 2006
   title_type = 'movie'

   title_data = get_titles_data([{'uid':uid, 'title': title, 'released': released,
        "title_type": title_type}])
   t = Title(uid, title, released, title_type)
   actors_added = t.create(title_data[0]['cast'])
   #--------------------------------------------
   # actors = []
   
   # for title in title_data: #here: actors_added
   # for actor in actors_added:
   actors = get_actors_data(actors_added)

   for actor in actors:
       level = 2 #really 1? here:

       a = Actor(
          actor['uid'], 
          actor['name'], 
          level)

       a.create(actor['titles'])

   return "Template here"


def get_actors_data(actors_attr):
    new_actors = []
    count = 0 #here:
    for actor in actors_attr: #['filmography'] if 'filmography' in actors_attr else actors_attr:
       uid = None
       if type(actor) == dict:# and (not 'found' in actor or not actor['found']):
           uid = actor['uid'] #[2:] if actor['uid'][0].isalpha() else actor['uid']
       
       elif type(actor) == Actor and (actor.children_known is None or not actor.children_known):
           uid = actor.uid[2:] #if actor.uid[0].isalpha() else actor.uid

      #  if True: #uid
       if uid:
            # response = API.retrieve( "/actors/get-all-filmography", {"nconst": actor['uid']})
           response = API.retrieve(f"/person/{uid}/combined_credits")
        #    if 'name' in actor:#remove here:
        #        with open('sanaaFilms2.txt') as f: resource = f.read()
        #    else:
        #  #       resource = API.retrieve( "/actors/get-all-filmography", {"nconst": actor['uid']})
        #        with open('CuocoFilms2.txt') as f: resource = f.read()
         #   with open('geneFilms2.txt') as f: response = f.read()
        #    from pprintpp import pprint
        #    pprint(response)
           titles = Actor.parse_filmography(response)

           this_actor = {'titles': titles}
           this_actor['uid'] = "na" + (actor['uid'] if type(actor) == dict else actor.uid)
        #    this_actor['data']['uid'] = actor['uid']
           this_actor['name'] = actor['name'] if type(actor) == dict else actor.name
           new_actors.append(this_actor)

    #    if not 'name' in actor:
      #  break
       count += 1
      #  if count == 2:
      #     break

    return new_actors

def get_titles_data(titles_attr): #get_data_related_to_titles
    new_titles = []
    count = 0 #here:
   #  related_actors_data = []
    for title in titles_attr:
      #   if 'found' not in title or not title['found']:
      #   if title.found is None or not title.found:
        uid = None
        if type(title) == dict:# and (not 'children_known' in title or not title['children_known']):
            uid = title['uid'] #[2:] if title['uid'][0].isalpha() else title['uid']
            title_type = title['title_type']

        elif type(title) == Title and (title.children_known is None or not title.children_known):
            uid = title.uid[2:] #if title.uid[0].isalpha() else title.uid
            title_type = title.title_type

      #   if True: # uid:
        if uid:
            # # resource = API.retrieve( "/title/get-top-cast", {"tconst": uid})
            response = API.retrieve(f'/{title_type}/{uid}/credits',{})
            # # response = API.retrieve('/tv/551',{})
            # with open('aCast3.txt') as f: response = f.read()
            # from pprintpp import pprint
            # pprint(response)
            cast = Title.parse_cast(response) #uids, no names

            # for actor_uid in cast_uids:
            #     related_actors_data.append( get_actors_data(actor_uid) )

            this_title = {'cast': cast}
            this_title['uid'] = title['uid'] if type(title) == dict else title.uid
            this_title['released'] = title['released'] if type(title) == dict else title.released
            this_title['title_type'] = title_type
            this_title['title'] = title['title'] if type(title) == dict else title.title
            new_titles.append(this_title)
            # break#here: break

        count += 1
      #   if count == 2:
         #   break
   #  return cast #new_titles
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