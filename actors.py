from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom, Graph, Node, Model
from initialClass import Actor
graph = Graph("bolt://neo4j:12345@localhost:7687")

class Actor(Actor):
  max_level = 3

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

  def tester(self):
    print(self.__class__.__name__)

  def create(self, titles_info):
    #add titles while possibly creating actor node
    #loop that checks to see if any titles were created. those that were get an Title instance 
    # and its create checks to see if any actors were created. however because of its level, nothing further will happen
    from titles import Title

    if self.level > self.__class__.max_level:
      return
    elif self.level == self.__class__.max_level:
      # tx.run("MERGE(b:Actor {name: $name, uid: $uid})", uid=self.uid, name=self.name)
      u = graph.run("MERGE(b:Actor {name: $name, uid: $uid})", {"uid": self.uid, "name": self.name})
      return

    # titles_added = self.add_titles(tx, titles_info)
    return self.add_titles(titles_info)

    # for title in titles_added:
    #   print(title['found']) #to do: delete
    #   if not title['found']:
    #     # t = Title(title['uid'], title['title'], self.level+1)
        
    #     t = Title(title.uid, title.title, self.level+1)
    #     # t.create()

  def add_title(self, tx, title_uid, title):
    tx.run("MATCH(a:Actor {uid: $uid}) "
    "MERGE(b:Title {title: $title, uid: $uid}) "
    "MERGE(a)-[:ACTED_IN]->(b) ", uid=self.uid, title=title, title_uid=title_uid)

  def add_titles(self, titles_info):    
    from titles import Title
    query = "MERGE (a:Actor {name: $name, uid: $uid}) SET a.children_known = True "
    params = {"name": self.name, "uid": self.uid}

    # for i in range(0,len(titles_info)):
    #   query += "MERGE (a:Actor {name: $name, uid: $uid}) "
    #   query += f"MERGE (t{i}:Title "
    #   query += "{title:$titles" + str(i) + "_title, uid:$titles" + str(i) + "_uid}) "
    #   query += f"""MERGE (a)-[:ACTED_IN]->(t{i}) 
    #   ON CREATE SET t{i}.found=FALSE 
    #   ON MATCH SET t{i}.found=TRUE 
    #   RETURN t{i}.found as found, t{i}.uid as uid, t{i}.title as title 
    #   UNION """

    #   params[f"titles{i}_uid"] = titles_info[i]["uid"]
    #   params[f"titles{i}_title"] = titles_info[i]["title"]

    # query = query[:-6]

    #######same
    title_uids = []
    # for i in range(0,len(titles_info['filmography'])):
    for i in range(0,len(titles_info)):
      query += f"MERGE (t{i}:Title "
      query += "{title:$titles" + str(i) + "_title, uid:$titles" + str(i) + "_uid, "
      query += "released:$titles" + str(i) + "_released, title_type:$titles" + str(i) + "_title_type}) "
      query += f"""MERGE (a)-[:ACTED_IN]->(t{i}) """
      # ON CREATE SET t{i}.found=FALSE 
      # ON MATCH SET t{i}.found=TRUE """

      params[f"titles{i}_uid"] = titles_info[i]["uid"]
      params[f"titles{i}_title"] = titles_info[i]["title"]
      params[f"titles{i}_released"] = titles_info[i]["released"]
      params[f"titles{i}_title_type"] = titles_info[i]["title_type"]
      title_uids.append(titles_info[i]["uid"])

    # query = query[:-6]
    graph.run(query, params)

    titles = Title.match(graph ).raw_query("""MATCH (_:Title) 
      WHERE _.uid IN $title_uids """, {"title_uids":title_uids})

    # query = query + "RETURN "
    return titles

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
    from titles import Title
    # titles = Title.match(graph ).raw_query(MATCH(a:Actor {uid: $uid})-[:ACTED_IN]->(_:Title) , params)

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

  def get_groups_titles(self, tx, actor_uids):
    tx.run("""MATCH(a:Actor)-[:ACTED_IN]->(b:Title) 
     WHERE a.uid IN $actor_uids 
     WITH count(r1) as rels, b 
     WHERE rels = $len(actor_uids) 
     RETURN distinct b.uid, b.title""", uid=self.uid)

    from titles import Title
    #here: distinct needed?
    actor_uids.append(self.uid)
    titles = Title.match(graph ).raw_query("""MATCH(a:Actor)-[:ACTED_IN]->(_:Title) 
     WHERE a.uid IN $actor_uids 
     WITH count(r1) as rels, _ 
     WHERE rels = $right_num""", {"actor_uids":actor_uids, "right_num":len(actor_uids) })

  # def get_groups_coactors_and_titlesDELETE(self, tx, actor_uids):
  #   actor_uids.append(self.uid)

  #   payload = tx.run("""MATCH(a:Actor)-[r1:ACTED_IN]->(b:Title) 
  #    WHERE a.uid IN $actor_uids 
  #    WITH count(r1) as rels, b 
  #    WHERE rels = $rels 
  #    MATCH (b)<-[ACTED_IN]-(c:Actor) 
  #    WHERE NOT c.id IN $actor_uids 
  #    RETURN distinct c.uid, c.name as cname
     
     
  #    MATCH(a:Actor)-[r1:ACTED_IN]->(b:Title) 
  #    WHERE a.uid IN [32,17] 
  #    WITH count(r1) as rels, b 
  #    WHERE rels = 2 
	#  WITH collect(b) as bb, b
	 
  #    MATCH (b)<-[ACTED_IN]-(c:Actor) 
  #    WHERE NOT c.id IN [32,17] 
  #    with collect(c) as cc, bb
  #    RETURN distinct cc,bb""", actor_uids=actor_uids, rels = len(actor_uids))

  def get_groups_coactors_and_titles(self, tx, actor_uids):
    actor_uids.append(self.uid)

    payload = tx.run("""MATCH(a:Actor)-[r1:ACTED_IN]->(b:Title) 
     WHERE a.uid IN $actor_uids 
     WITH count(r1) as rels, b 
     WHERE rels = $rels 
     WITH collect(b) as bb, b 

     MATCH (b)<-[ACTED_IN]-(c:Actor) 
     WHERE NOT c.id IN $actor_uids 
     with collect(c) as cc, bb
     RETURN distinct cc,bb""", actor_uids=actor_uids, rels = len(actor_uids))


  def titles_string(self, titles):
    str = ""

  @classmethod
  def find_by_uid(cls, uid):
    # actor = match(graph ).where("_.uid IN ['56', 32]").all()#first()
    actor = cls.match(graph).where("_.uid IN ['56', 32]").first()
    # actor = NodeMatcher(graph).match("Actor").where("_.uid IN ['56', 32]").all()#works

    return actor

  @classmethod
  def find_by_name(cls, query):
    # actor = match(graph ).where("_.uid IN ['56', 32]").all()#first()
    q_parts = query.replace(',',' ').split()
    params = {}

    # if len(q_parts) > 1 and False:
    if len(q_parts) > 1:
      # where_clause = """WHERE _.name =~ '$name1.* $name2.*'
      #  or _.name =~ '$name4.* $name3.*' """
      
      where_clause = """WHERE _.name =~ $name1
       or _.name =~ $name2 """

      params['name1'] = q_parts[0] + ".*" + q_parts[1] + ".*"
      params['name2'] = q_parts[1] + ".*" + q_parts[0] + ".*"
    else:
      where_clause = "WHERE _.name =~ $name"
      params['name'] = query + ".*"

    actor = cls.match(graph ).raw_query("MATCH (_:Actor) " + where_clause, params)
    # actor = NodeMatcher(graph).match("Actor").where("_.uid IN ['56', 32]").all()#works

    return actor

  @classmethod
  def get_paginated_all(cls, tx):
    pass

  @staticmethod
  def parse_filmography(actor_data):
    # from pprintpp import pprint
    # pprint(values)
    import json
    # import re
    actor_data = json.loads(actor_data)
    # titles = values['cast']
    titles = actor_data['combined_credits']['cast']
    # pprint(titles[0])
    title = titles[0]
    print(f"the uid is {title['id']}")
    # print(f"the title is {title['title']}")
    # print(f"the start year is {title['startYear']}")
    # print(f"the  (real) start year is {title['year']}")

    title = titles[3]
    # pprint(title)
    print(f"the uid is {title['id']}")
    # print(f"the title is {title['title']}")
    # print(f"the start year is {title['startYear']}")
    # print(f"the (real) start year is {title['year']}")
    # pprint(title)

    result = []
    for title in titles:
      title_type = title['media_type']
      result.append({
        "uid": "mo" + str(title['id']) if title_type == 'movie' else "tv" + str(title['id']),
        # "uid": "mo" + title['id'] if title_type == 'movie' else "tv" + title['id'],
        "title": title['title'] if title_type == 'movie' else title['name'], 
        # "released": title['first_air_date'][:4] if title_type == 'tv' else title['release_date'][:4],
        "released": title['first_air_date'][:4] if 'first_air_date' in title else title['release_date'][:4] if 'release_date' in title else "",
        "title_type": title_type})

    # return {"titles": result, 
    # "name": values['base']["name"]}
    return {"titles": result, "uid": "na" + str(actor_data['id']),
        "name": actor_data['name']}

  #  @staticmethod
  # def def find_by_name(name):
  #   pass
  #   name = name.split(" ")
  #   option1 = name.join(".* ") + ".*"
  #   option2 = name.reverse().join(".* ") + ".*"
  #   #*sanaa*lat* or name like *lat*sanaa*

# /////////////// compare explain query
    #  WHERE NOT c.id IN $inc_ids 
    #  with [b.id, b.title] as hh,[c.id,c.name] as g
    #  return  collect(hh),collect(g)
     
  # def add_titles([imdb_ids_titles]):
  
  # def list():
  
  # def connected_actors():
    
