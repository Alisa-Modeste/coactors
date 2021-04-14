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
    # coactors.app.request = MagicMock()
    with get_request_context(), mock.patch('coactors.app.request', MagicMock()):
    # coactors.app.request.args = MagicMock()
        mock.patch('coactors.app.request.args', MagicMock())
    # coactors.app.request.args.get = MagicMock()
    # coactors.app.request.args.get.side_effect =['s', None]

    # with get_request_context():
        # print(coactors.app.request.args.get('query'))
    # with get_request_context():# and 
    #     with mock.patch('coactors.app.request.args.get', MagicMock(side_effect =['s', None])):
    #         response = app.actor_text_search()
        with mock.patch('coactors.app.request.args.get', MagicMock(side_effect =['s', None])):
            response = app.actor_text_search()

    assert "uid" in response['results'][0]
    assert "name" in response['results'][0]
    assert ("Sanaa Lanthan" in response['results'][0]['name'] 
        or "Simon Baker" in response['results'][0]['name'])

    assert response['known'] == True
    assert response['query'] == 's'


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
        if "Sanaa Lanthan" == actor['name']:
            return
    assert 0, "Sanaa Lanthan not in title's cast"

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


def test_title_text_search_doesnt_exist_in_db():
    with get_request_context(), mock.patch('coactors.app.request', MagicMock()):
        mock.patch('coactors.app.request.args', MagicMock())
        mock.patch('coactors.app.request.args.get', MagicMock(return_value = 'p'))
        
        with mock.patch('coactors.app.parse_search_results', MagicMock(return_value = {})):

            response = app.title_text_search()

        assert response['known'] == False
        assert response['results'] == {}

