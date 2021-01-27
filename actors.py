#from py2neo import Graph
# from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom, Graph, Node
# from titles import Title
# graph = Graph("bolt://neo4j:12345@localhost:7687")

# class Actor(GraphObject):
class Actor:
    #__primarykey__ = "id"

  # uid = Property()
  # name = Property()

  # acted_in = RelatedTo(Title)

  def __init__(self, uid, name, level=1):
    self.uid = uid
    self.name = name
    self.level = level
    
  # def add_title(title_uid, title):
  #   a = Node("Actor", name=name, uid=uid)
  #   b = Node("Title", title=title, uid=title_uid)
  #   ACTED_IN = Relationship.type("ACTED_IN")
  #   graph.merge(ACTED_IN(a, b), "Title", "uid")


  def create(self):
    tx.run("MERGE(b:Actor {name: $name, uid: $uid})", uid=self.uid, name=name)
    #add titles while possibly creating actor node
    #loop that checks to see if any titles were created. those that were get an Title instance 
    # and its create checks to see if any actors were created. however because of its level, nothing further will happen

  def add_title(self, tx, title_uid, title):
    tx.run("MATCH(a:Actor {uid: $uid}) "
    "MERGE(b:Title {title: $title, uid: $uid}) "
    "MERGE(a)-[:ACTED_IN]->(b) ", uid=self.uid, title=title, title_uid=title_uid)

  def add_titles(self, tx, titles):
    # tx.run("foreach(uid,title in length | MERGE(t:Title {title: $title, uid: $uid}) )")
    
    query = ""
    params = {"name": self.name, "uid": self.uid}

    for i in range(0,len(titles)):
      query += "MERGE (a:Actor {name: $name, uid: $uid}) "
      query += f"MERGE (t{i}:Title "
      query += "{title:$titles" + str(i) + "_title, uid:$titles" + str(i) + "_uid}) "
      query += f"""MERGE (a)-[:ACTED_IN]->(t{i}) 
      ON CREATE SET t{i}.found=FALSE 
      ON MATCH SET t{i}.found=TRUE 
      RETURN t{i}.found as found, t{i}.uid as uid, t{i}.title as title 
      UNION """

      params[f"titles{i}_uid"] = titles[i]["uid"]
      params[f"titles{i}_title"] = titles[i]["title"]


      # with_clause.append("t"+str(i))

    # query += " WITH " + ", ".join(with_clause) + " "
    # query += "RETURN "
    query = query[:-6]
    print(query)
    tx.run(query, params)

  def get_coactors(self, tx):
    payload = tx.run("""MATCH(a:Actor {uid: $uid})-[:ACTED_IN]->(b:Title) 
    <-[:ACTED_IN]-(c:Actor) 
      WHERE c.uid <> $uid  
      RETURN distinct c.uid, c.name as cname""", uid=self.uid) #RETURN b.id, b.title, c.id, c.name""", uid=self.uid)
    
    for record in payload:
      print("" + str(record["c.uid"]) + " and name:" + record["cname"])

  def get_titles(self, tx):
    tx.run("""MATCH(a:Actor {uid: $uid})-[:ACTED_IN]->(b:Title)  
     RETURN b.uid, b.title""", uid=self.uid)

  def get_groups_coactors(self, tx, actor_uids):
    actor_uids.append(self.uid)

    payload = tx.run("""MATCH(a:Actor)-[r1:ACTED_IN]->(b:Title) 
     WHERE a.uid IN $actor_uids 
     WITH count(r1) as rels, b 
     WHERE rels = $rels 
     MATCH (b)<-[ACTED_IN]-(c:Actor) 
     WHERE NOT c.id IN $actor_uids 
     RETURN distinct c.uid, c.name as cname""", actor_uids=actor_uids, rels = len(actor_uids)) #RETURN b.id, b.title, c.id, c.name""", uid=self.uid, inc_ids=inc_ids)

    for record in payload:
      print("" + str(record["c.uid"]) + " and name:" + record["cname"])

  def get_groups_titles(self, tx):
    tx.run("""MATCH(a:Actor)-[:ACTED_IN]->(b:Title) 
     WHERE a.uid IN $actor_uids 
     WITH count(r1) as rels, b 
     WHERE rels = $len(actor_uids) 
     RETURN distinct b.uid, b.title""", uid=self.uid)

  def get_groups_coactors_and_titles(self, tx, actor_uids):
    actor_uids.append(self.uid)

    payload = tx.run("""MATCH(a:Actor)-[r1:ACTED_IN]->(b:Title) 
     WHERE a.uid IN $actor_uids 
     WITH count(r1) as rels, b 
     WHERE rels = $rels 
     MATCH (b)<-[ACTED_IN]-(c:Actor) 
     WHERE NOT c.id IN $actor_uids 
     RETURN distinct c.uid, c.name as cname
     
     
     MATCH(a:Actor)-[r1:ACTED_IN]->(b:Title) 
     WHERE a.uid IN [32,17] 
     WITH count(r1) as rels, b 
     WHERE rels = 2 
	 WITH collect(b) as bb, b
	 
     MATCH (b)<-[ACTED_IN]-(c:Actor) 
     WHERE NOT c.id IN [32,17] 
     with collect(c) as cc, bb
     RETURN distinct cc,bb""", actor_uids=actor_uids, rels = len(actor_uids))

  def titles_string(self, titles):
    str = ""

# /////////////// compare explain query
    #  WHERE NOT c.id IN $inc_ids 
    #  with [b.id, b.title] as hh,[c.id,c.name] as g
    #  return  collect(hh),collect(g)
     
  # def add_titles([imdb_ids_titles]):
  
  # def list():
  
  # def connected_actors():
    
