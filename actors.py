#from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom, Graph, Node
graph = Graph("bolt://neo4j:12345@localhost:7687")

class Actor(GraphObject):
    #__primarykey__ = "id"

  imdb_id = Property()
  name = Property()

  acted_in = RelatedTo(Title)
  
  def __init__(self, id, name):
    self.id = id
    self.name = name
    
    
  def add_title(title_imdb_id, title):
    a = Node("Actor", name=name, imdb_id=imdb_id)
    b = Node("Title", title=title, imdb_id=title_imdb_id)
    ACTED_IN = Relationship.type("ACTED_IN")
    graph.merge(ACTED_IN(a, b), "Title", "imdb_id")

  def add_titles([imdb_ids_titles]):
  
  def list():
  
  def connected_actors():
    
  