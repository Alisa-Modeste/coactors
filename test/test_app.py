from pytest import fixture
# import unittest
from unittest import mock
from unittest.mock import MagicMock, Mock
import coactors.py2neo_monkeypatch
from py2neo.ogm import Graph
# from coactors.app import tree

import sys
sys.modules['coactors.api'] = MagicMock()
sys.modules['coactors.db_admin'] = MagicMock()
sys.modules['coactors.db_admin'].graph = Graph("bolt://neo4j:123456@localhost:7687")


import coactors.app as app

graph = Graph("bolt://neo4j:123456@localhost:7687")


from flask import Flask
from flask_testing import TestCase

class MyTest(TestCase):

    def create_app(self):

        app = Flask(__name__)
        app.config['TESTING'] = True
        return app

@fixture
def empty_db():
    graph.run("Match (n) Detach delete n")

@fixture
def fill_db(empty_db):
    with open("data_dump.cypher") as file_object:
        queries = file_object.read()
        graph.run(queries)

def get_request_context():
    app2 = MyTest.create_app(MyTest)
    return app2.test_request_context()


def test_find_actor(fill_db):

    with get_request_context():
        actor = app.find_actor("na2")

    assert actor['name'] == 'Kyla Pratt'

    for title in actor['titles']:
        if "Alien vs. Predator" == title['title']:
            return
    assert 0, "Alien vs. Predator not in actor's titles"

def test_actor_text_search_exist_in_db(fill_db):
    with get_request_context(), mock.patch('coactors.app.request', MagicMock()):
        mock.patch('coactors.app.request.args', MagicMock())

        with mock.patch('coactors.app.request.args.get', MagicMock(side_effect =['s', None])):
            response = app.actor_text_search()

    assert "uid" in response['results'][0]
    assert "name" in response['results'][0]
    assert (response['results'][0]['name'] == "Sanaa Lathan"
        or response['results'][0]['name'] == "Simon Baker")

    assert response['known'] == True
    assert response['query'] == 's'

def test_actor_text_search_exist_in_db_any_order(fill_db):
    with get_request_context(), mock.patch('coactors.app.request', MagicMock()):
        mock.patch('coactors.app.request.args', MagicMock())

        with mock.patch('coactors.app.request.args.get', MagicMock(side_effect =['lathan s', None])):
            response = app.actor_text_search()

    assert "uid" in response['results'][0]
    assert "name" in response['results'][0]
    assert response['results'][0]['name'] == "Sanaa Lathan"

    assert response['known'] == True
    assert response['query'] == 'lathan s'


def test_actor_text_search_doesnt_exist_in_db():
    with get_request_context(), mock.patch('coactors.app.request', MagicMock()):
        mock.patch('coactors.app.request.args', MagicMock())
        # coactors.app.request.args.get = MagicMock(return_value = 's')
        mock.patch('coactors.app.request.args.get', MagicMock(return_value = 's'))
        # coactors.app.parse_search_results = MagicMock(return_value = {})
        
        with mock.patch('coactors.app.parse_search_results', MagicMock(return_value = {})):

            # print(coactors.app.request.args.get('query'))
            response = app.actor_text_search()

        assert response['known'] == False
        assert response['results'] == {}

    # coactors.app.parse_search_results.reset_mock(True)

def test_parse_actor_search_results():
    with open("resources/annouckQuery.txt") as file_object:
        response = file_object.read()
        parsed = coactors.app.parse_search_results(response, "actors")

    assert "uid" in parsed[0]
    assert "name" in parsed[0]
    
    assert ("Annouck Hautbois" in parsed[0]['name'] 
        or "Annouck Dupont" in parsed[0]['name'])

    assert len(parsed) == 2

def test_get_actors(fill_db):

    with get_request_context():
        actors = app.get_actors()

    actors = actors.json
    assert len(actors) == 10


def test_find_title(fill_db):

    with get_request_context():
        title = app.find_title("mo3")

    assert title['title'] == 'Something New'
    assert title['released'] == "2006"

    for actor in title['cast']:
        if "Sanaa Lathan" == actor['name']:
            return
    assert 0, "Sanaa Lathan not in title's cast"

def test_tv_text_search_exist_in_db(fill_db):
    with get_request_context(), mock.patch('coactors.app.request', MagicMock()):
        mock.patch('coactors.app.request.args', MagicMock())

        with mock.patch('coactors.app.request.args.get', MagicMock(side_effect =['m', None])):
            response = app.title_text_search()

    assert response['results'][0]['uid'] == "tv1"
    assert response['results'][0]['title'] == "The Mentalist"
    assert response['results'][0]['released'] == "2008"

    assert response['known'] == True
    assert response['query'] == 'm'

def test_movie_text_search_exist_in_db(fill_db):
    with get_request_context(), mock.patch('coactors.app.request', MagicMock()):
        mock.patch('coactors.app.request.args', MagicMock())

        with mock.patch('coactors.app.request.args.get', MagicMock(side_effect =['p', None])):
            response = app.title_text_search()

    assert response['results'][0]['uid'] == "mo1"
    assert response['results'][0]['title'] == "Alien vs. Predator"
    assert response['results'][0]['released'] == "2004"

    assert response['known'] == True
    assert response['query'] == 'p'

def test_movie_text_search_exist_in_db_any_order(fill_db):
    with get_request_context(), mock.patch('coactors.app.request', MagicMock()):
        mock.patch('coactors.app.request.args', MagicMock())

        with mock.patch('coactors.app.request.args.get', MagicMock(side_effect =['predator alien', None])):
            response = app.title_text_search()

    assert response['results'][0]['uid'] == "mo1"
    assert response['results'][0]['title'] == "Alien vs. Predator"
    assert response['results'][0]['released'] == "2004"

    assert response['known'] == True
    assert response['query'] == 'predator alien'


def test_title_text_search_doesnt_exist_in_db():
    with get_request_context(), mock.patch('coactors.app.request', MagicMock()):
        mock.patch('coactors.app.request.args', MagicMock())
        mock.patch('coactors.app.request.args.get', MagicMock(return_value = 'p'))
        
        with mock.patch('coactors.app.parse_search_results', MagicMock(return_value = {})):

            response = app.title_text_search()

        assert response['known'] == False
        assert response['results'] == {}

def test_parse_title_search_results():
    with open("resources/littleMermaidQuery.txt") as file_object:
        response = file_object.read()
        parsed = coactors.app.parse_search_results(response, "titles")

    assert "uid" in parsed[0]
    assert "title" in parsed[0]
    assert "released" in parsed[0]
    assert "title_type" in parsed[0]

    assert len(parsed) == 19
    
    for el in parsed:
        if el['title'] == "The Little Mermaid II: Return to the Sea":
            return
    
    assert 0, "The Little Mermaid II: Return to the Sea not in results"

def test_get_titles(fill_db):

    with get_request_context():
        titles = app.get_titles()

    titles = titles.json
    assert len(titles) == 5