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
    
  # def add_title(title_uid, title):
  #   a = Node("Actor", name=name, uid=uid)
  #   b = Node("Title", title=title, uid=title_uid)
  #   ACTED_IN = Relationship.type("ACTED_IN")
  #   graph.merge(ACTED_IN(a, b), "Title", "uid")


  def add_title(tx, title_uid, title):
    tx.run("MATCH(a:Actor {uid: $uid}) "
    "MERGE(b:Title {title: $title, uid: $uid}) "
    "MERGE(a)-[:ACTED_IN]->(b) ", uid=self.uid, title=title, title_uid=title_uid)

  # def add_titles(tx, title_uid, title):

  def get_coactors(self, tx):
    payload = tx.run("MATCH(a:Actor {id: $uid})-[:ACTED_IN]->(b:Title) "
    "<-[:ACTED_IN]-(c:Actor) "
      "WHERE c.id <> $uid  "
      "RETURN distinct c.id, c.name as cname", uid=self.uid) #RETURN b.id, b.title, c.id, c.name""", uid=self.uid)
    
    for record in payload:
      return record["cname"]

  def get_titles(tx):
    tx.run("""MATCH(a:Actor {uid: $uid})-[:ACTED_IN]->(b:Title)  
     RETURN b.uid, b.title""", uid=self.uid)

  def get_groups_coactors(tx, actor_uids):
     tx.run("""MATCH(a:Actor)-[r1:ACTED_IN]->(b:Title) 
     WHERE a.uid IN $inc_ids 
     WITH count(r1) as rels, b 
     WHERE rels = $len(inc_uids) 
     MATCH (b)<-[ACTED_IN]-(c:Actor) 
     WHERE NOT c.id IN $inc_uids 
     RETURN distinct c.uid, c.name""", uid=self.uid, inc_ids=inc_ids) #RETURN b.id, b.title, c.id, c.name""", uid=self.uid, inc_ids=inc_ids)

  def get_groups_titles(tx):
    tx.run("""MATCH(a:Actor)-[:ACTED_IN]->(b:Title) 
     WHERE a.uid IN $inc_ids 
     WITH count(r1) as rels, b 
     WHERE rels = $len(inc_uids) 
     RETURN distinct b.uid, b.title""", uid=self.uid)

# /////////////// compare explain query
    #  WHERE NOT c.id IN $inc_ids 
    #  with [b.id, b.title] as hh,[c.id,c.name] as g
    #  return  collect(hh),collect(g)
     
  # def add_titles([imdb_ids_titles]):
  
  # def list():
  
  # def connected_actors():
    
