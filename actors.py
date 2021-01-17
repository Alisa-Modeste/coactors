#from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom, Graph, Node
from titles import Title
graph = Graph("bolt://neo4j:12345@localhost:7687")

class Actor(GraphObject):
    #__primarykey__ = "id"

  uid = Property()
  name = Property()

  acted_in = RelatedTo(Title)

  def __init__(self, uid, name):
    self.uid = uid
    self.name = name
    
    
  def add_title(title_uid, title):
    a = Node("Actor", name=name, uid=uid)
    b = Node("Title", title=title, uid=title_uid)
    ACTED_IN = Relationship.type("ACTED_IN")
    graph.merge(ACTED_IN(a, b), "Title", "uid")


  def add_title_take_two(tx, title_uid, title):
    tx.run("MATCH(a:Actor {uid: $uid}) "
    "MERGE(b:Title {title: $title, uid: $uid}) "
    "MERGE(a)-[:ACTED_IN]->(b) ", uid=self.uid, title=title, title_uid=title_uid)

  def get_coactors(tx):
    tx.run("""MATCH(a:Actor {uid: $uid})-[:ACTED_IN]->(b:Title) 
    <-[:ACTED_IN]-(c:Actor)
     WHERE c.id <> $uid  
     RETURN b.id, b.title, c.id, c.name""", uid=self.uid)

  def get_groups_coactors(tx, actor_uids):
     tx.run("""MATCH(a:Actor)-[r1:ACTED_IN]->(b:Title) 
     WHERE a.id IN $inc_ids 
     WITH r, b 
     WHERE count(r) = $len(inc_ids) 
     MATCH (b)<-[ACTED_IN]-(c:Actor) 
     WHERE c.id NOT IN $inc_ids 
     RETURN b.id, b.title, c.id, c.name""", uid=self.uid, inc_ids=inc_ids)


  # def add_titles([imdb_ids_titles]):
  
  # def list():
  
  # def connected_actors():
    
