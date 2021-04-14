from flask import Flask, render_template, request, redirect, url_for

try:
    from actors import Actor
    from titles import Title
    from api import API
except ImportError:
    from coactors.actors import Actor
    from coactors.titles import Title
    from coactors.api import API

from datetime import datetime
import re

app = Flask(__name__)

@app.after_request
def after_request_func(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route('/',methods = ['GET'])
def wake_up_server():
    return {}

@app.route('/create_actor',methods = ['GET'])
def create_actor():
    uid = request.args.get('uid')
    uid = uid if uid.isnumeric() else uid[2:]

    if not uid.isnumeric():
        return {}
    actor = find_actor("na" + uid)
    if actor and 'children_known' in actor:
        return actor

    actor_data = get_actors_data([{'uid': uid}])
    a = Actor(actor_data[0]['uid'], actor_data[0]['name'])
    titles_added = a.add_titles(actor_data[0]['titles'])

    casts = get_titles_data(titles_added)

    for cast in casts:
        t = Title(cast['uid'],
            cast['title'],
            cast['released'],
            cast['title_type'])

        t.add_cast(cast['cast'])

    return redirect(url_for('find_actor', uid=actor_data[0]['uid']))

@app.route('/create_title',methods = ['GET'])
def create_title():
    uid = request.args.get('uid')
    title_type = request.args.get('title_type')
    if uid.isnumeric():

        if title_type == "movie" or title_type == "tv":
            prefix = title_type[0:2]
        else:
            return {}
            
    elif uid[2:].isnumeric():
        prefix = uid[0:2]
        uid = uid[2:]
        if prefix == "mo":
            title_type = "movie"
        elif prefix == "tv":
            title_type = "tv"

    else:
            return {}


    title = find_title(prefix + uid)
    if title and 'children_known' in title:
        return title

    title_data = get_titles_data([{'uid':uid,
        "title_type": title_type}])
    t = Title(title_data[0]['uid'],
        title_data[0]['title'],
        title_data[0]['released'],
        title_data[0]['title_type'])
    actors_added = t.add_cast(title_data[0]['cast'])

    actors = get_actors_data(actors_added)

    for actor in actors:

        a = Actor(
            actor['uid'], 
            actor['name'])

        a.add_titles(actor['titles'])

    return redirect(url_for('find_title', uid=title_data[0]['uid']))


def get_actors_data(actors_attr):
    new_actors = []

    for actor in actors_attr:
        uid = None
        if type(actor) == dict:
            uid = actor['uid']
        
        elif type(actor) == Actor and (actor.children_known is None or not actor.children_known):
            uid = actor.uid[2:] 

        if uid:

            response = API.retrieve(f"/person/{uid}",{'append_to_response': "combined_credits"})

            titles = Actor.parse_filmography(response)

            new_actors.append(titles)

    return new_actors

def get_titles_data(titles_attr): 
    new_titles = []

    for title in titles_attr:

        uid = None
        if type(title) == dict:
            uid = title['uid'] 
            title_type = title['title_type']

        elif type(title) == Title and (title.children_known is None or not title.children_known):
            uid = title.uid[2:] 
            title_type = title.title_type

        if uid:

            if title_type == "movie":
               response = API.retrieve(f'/{title_type}/{uid}',{'append_to_response': "credits"})
            else:
               response = API.retrieve(f'/{title_type}/{uid}',{'append_to_response': "aggregate_credits"})

            cast = Title.parse_cast(response, title_type) 

            new_titles.append(cast)

    return new_titles

@app.route('/actor/<uid>',methods = ['GET'])
def find_actor(uid):
    group = request.args.get('ca').split(",") if request.args.get('ca') else None
    actor = Actor.find_by_uid(uid)

    if actor and group:
        group_members = Actor.find_by_uids(group)

        coactors = actor.get_groups_coactors(group.copy())
        titles = actor.get_groups_titles(group.copy())

        return actor.serialize2(titles, coactors, group_members)

    elif actor:
        coactors = actor.get_coactors()
        titles = actor.get_titles()

        return actor.serialize2(titles, coactors)
    else:
        return {}

@app.route('/actors',methods = ['GET'])
def get_actors():
    actors = Actor.get_all()
        
    actor_list = []
    for actor in actors:
        actor_list.append( actor.serialize() )

    from flask import jsonify
    return jsonify(actor_list)
  


@app.route('/title/<uid>',methods = ['GET'])
def find_title(uid):
    title = Title.find_by_uid(uid)
    if title:
        cast = title.get_cast()

        return title.serialize2(cast)
    else:
        return {}

@app.route('/titles',methods = ['GET'])
def get_titles():
    titles = Title.get_all()

    title_list = []
    for title in titles:
        title_list.append( title.serialize() )

    from flask import jsonify
    return jsonify(title_list)


@app.route('/actor_search',methods = ['GET'])
def actor_text_search():
    query = request.args.get('query')
    not_listed = request.args.get('more') if request.args.get('more') else None
    actors = None

    if not not_listed:
        actors = Actor.find_by_name(query)

    if actors:
        response = []
        for actor in actors:
            response.append( {"uid": actor.uid, "name": actor.name,
            "children_known": actor.children_known if actor.children_known else False} )
        

        return {"known": True, "results": response, "query":query}

    response = API.retrieve('/search/person',{'query': query})
    actors = parse_search_results(response, "actors")

    return {"known": False, "results": actors}


@app.route('/title_search',methods = ['GET'])
def title_text_search():
    query = request.args.get('query')
    not_listed = request.args.get('more') if request.args.get('more') else None
    titles = None

    if not not_listed:
        titles = Title.find_by_title(query)

    if titles:
        response = []
        for title in titles:
            response.append( {"uid": title.uid, "title": title.title,
            "released": title.released,"title_type":title.title_type,
            "children_known": title.children_known if title.children_known else False} )
        return {"known": True, "results": response, "query":query}

    response = API.retrieve('/search/multi',{'query': query})
    titles = parse_search_results(response, "titles")
    return {"known": False, "results": titles}


def parse_search_results(response, search_type):
    import json
    response = json.loads(response)
    response = response['results']

    result = []

    if search_type == "titles":
        for el in response:
            if el['media_type'] == "tv" or el['media_type'] == "movie":
                result.append( Title.parse_properties(el, None, False) )

    #people search
    else:
        for el in response:
            if el['known_for_department'] == "Acting" or el['known_for_department'] == "acting":
                result.append( 

                    {'uid': str(el['id']),
                    'name': el['name']}
                )

    return result


if  __name__ == '__main__':
    app.run()