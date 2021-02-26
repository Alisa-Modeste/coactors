from py2neo import Graph #here: here or ogm?
from py2neo.ogm import Property, Graph, Model
graph = Graph("bolt://neo4j:12345@localhost:7687")

class Actor(Model):
  max_level = 3

  uid = Property()
  name = Property()
  children_known = Property()

  def __init__(self, uid, name, level=1):
    self.uid = uid
    self.name = name
    self.level = level
    
  # def add_title(title_uid, title):
  #   a = Node("Actor", name=name, uid=uid)
  #   b = Node("Title", title=title, uid=title_uid)
  #   ACTED_IN = Relationship.type("ACTED_IN")
  #   graph.merge(ACTED_IN(a, b), "Title", "uid")

  def create(self, titles_info):
    #add titles while possibly creating actor node
    #loop that checks to see if any titles were created. those that were get an Title instance 
    # and its create checks to see if any actors were created. however because of its level, nothing further will happen
    from titles import Title

    if self.level > self.__class__.max_level:
      return
    elif self.level == self.__class__.max_level:
      u = graph.run("MERGE(b:Actor {name: $name, uid: $uid})", {"uid": self.uid, "name": self.name})
      return

    return self.add_titles(titles_info)


  def add_title(self, tx, title_uid, title):
    tx.run("MATCH(a:Actor {uid: $uid}) "
    "MERGE(b:Title {title: $title, uid: $uid}) "
    "MERGE(a)-[:ACTED_IN]->(b) ", uid=self.uid, title=title, title_uid=title_uid)

  def add_titles(self, titles_info):
    query = "CALL {"
    from titles import Title
    params = {"name": self.name, "uid": self.uid}

    # title_uids = []
    for i in range(0,len(titles_info)):
      query += """MERGE (a:Actor {uid: $uid}) 
        SET a += {name: $name, children_known: True} """

# -      RETURN t{i} as _.found as found, t{i}.uid as uid, t{i}.title as title

      query += f"MERGE (t{i}:Title " + "{uid:$titles" + str(i) + "_uid}) "
      query += f" SET t{i} += " + "{title:$titles" + str(i) + "_title, released:$titles" + str(i) 
      query += "_released, title_type:$titles" + str(i) + "_title_type} "      
      query += f"""MERGE (a)-[:ACTED_IN]->(t{i}) 
      ON CREATE SET t{i}.found=FALSE 
      ON MATCH SET t{i}.found=TRUE 
      RETURN t{i} as _ 
      UNION """


      params[f"titles{i}_uid"] = titles_info[i]["uid"]
      params[f"titles{i}_title"] = titles_info[i]["title"]
      params[f"titles{i}_released"] = titles_info[i]["released"]
      params[f"titles{i}_title_type"] = titles_info[i]["title_type"]
# +      title_uids.append(titles_info[i]["uid"])

    query = query[:-6] + "} "

    titles = Title.match(graph ).raw_query(query, params)

    return titles

  def get_coactors(self):
    return self.__class__.match(graph ).raw_query("""MATCH(a:Actor {uid: $uid})-[:ACTED_IN]->(b:Title) 
    <-[:ACTED_IN]-(_:Actor) 
      WHERE _.uid <> $uid  
      WITH distinct _ """ , {"uid":self.uid})

  def get_titles(self):
    from titles import Title
    return Title.match(graph ).raw_query("MATCH(a:Actor {uid: $uid})-[:ACTED_IN]->(_:Title) ", {"uid":self.uid})

  def get_groups_coactors(self, actor_uids):
    actor_uids.append(self.uid)

    # payload = tx.run("""MATCH(a:Actor)-[r1:ACTED_IN]->(b:Title) 
    return self.__class__.match(graph ).raw_query("""MATCH(a:Actor)-[r1:ACTED_IN]->(b:Title) 
     WHERE a.uid IN $actor_uids 
     WITH count(r1) as rels, b 
     WHERE rels = $rels 
     MATCH (b)<-[ACTED_IN]-(_:Actor) 
     WHERE NOT _.uid IN $actor_uids 
     WITH distinct _ """ , {"actor_uids":actor_uids, "rels": len(actor_uids)})

    #  RETURN distinct c.uid, c.name as cname""", actor_uids=actor_uids, rels = len(actor_uids)) #RETURN b.id, b.title, c.id, c.name""", uid=self.uid, inc_ids=inc_ids)


    # for record in payload:
    #   print("" + str(record["c.uid"]) + " and name:" + record["cname"])

  def get_groups_titles(self, actor_uids):
    # tx.run("""MATCH(a:Actor)-[:ACTED_IN]->(b:Title) 
    #  WHERE a.uid IN $actor_uids 
    #  WITH count(r1) as rels, b 
    #  WHERE rels = $len(actor_uids) 
    #  RETURN distinct b.uid, b.title""", uid=self.uid)

    from titles import Title
    #here: distinct needed?
    actor_uids.append(self.uid)
    # titles = Title.match(graph ).raw_query("""MATCH(a:Actor)-[:ACTED_IN]->(_:Title) 
    #  WHERE a.uid IN $actor_uids 
    #  WITH count(r1) as rels, _ 
    #  WHERE rels = $right_num""", {"actor_uids":actor_uids, "right_num":len(actor_uids) })

    return Title.match(graph ).raw_query("""MATCH(a:Actor)-[r1:ACTED_IN]->(_:Title) 
     WHERE a.uid IN $actor_uids 
     WITH count(r1) as rels, _ 
     WHERE rels = $rels 
     WITH distinct _ """, {"actor_uids":actor_uids, "rels": len(actor_uids)})


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


  # def toJSON(self):
  #   import json
  #   print(self.__dict__)
  #   print(vars(self))
  #   print( json.dumps(self, default=lambda o: o.__dict__, 
  #           sort_keys=True, indent=4) )
  #   return json.dumps(self, default=lambda o: o.__dict__, 
  #           sort_keys=True, indent=4)

  def serialize(self):
    return {"uid": self.uid,
            "name": self.name}

  @classmethod
  def find_by_uid(cls, uid):
    #here: safe handling of where clause
    # where() doesn't seem to allow for parameterized queries and so the related problem of SQL/Cypher injection
    # return cls.match(graph).where(f"_.uid = '{uid}'").first()
    actor = cls.match(graph).raw_query("MATCH (_:Actor {uid: $uid}) ", {'uid':uid})

    if actor:
      return actor[0]

  @classmethod
  def find_by_uids(cls, uids):
    #here: safe handling of where clause
    # where() doesn't seem to allow for parameterized queries and so the related problem of SQL/Cypher injection
    # return cls.match(graph).where(f"_.uid = '{uid}'").first()
    return cls.match(graph).raw_query("MATCH (_:Actor) WHERE _.uid IN $uids", {'uids':uids})

    # if actor:
    #   return actor[0]


  @classmethod
  def find_by_name(cls, query):
    q_parts = query.replace(',',' ').split()
    params = {}

    if len(q_parts) > 1:
      
      where_clause = """WHERE _.name =~ $name1
       or _.name =~ $name2 """

      params['name1'] = "(?i).*" + q_parts[0] + ".*" + q_parts[1] + ".*"
      params['name2'] = "(?i).*" + q_parts[1] + ".*" + q_parts[0] + ".*"
    else:
      where_clause = "WHERE _.name =~ $name"
      params['name'] = "(?i)" + query + ".*"

    return cls.match(graph ).raw_query("MATCH (_:Actor) " + where_clause, params)


  @classmethod
  # def get_paginated_all(cls, tx):
  def get_all(cls, skip=0, limit=500):
    #here: created_date or alpha
    return cls.match(graph ).raw_query(
      "CALL { MATCH (_:Actor) return _ skip $skip limit $limit } ", {"skip": skip, "limit": limit}
    ) 

  @staticmethod
  def parse_filmography(actor_data):
    import json

    actor_data = json.loads(actor_data)

    titles = actor_data['combined_credits']['cast']

    result = []
    for title in titles:
      title_type = title['media_type']
      result.append({
        "uid": "mo" + str(title['id']) if title_type == 'movie' else "tv" + str(title['id']),
        "title": title['title'] if title_type == 'movie' else title['name'], 
        "released": title['first_air_date'][:4] if 'first_air_date' in title else title['release_date'][:4] if 'release_date' in title else "",
        "title_type": title_type})

    return {"titles": result, "uid": "na" + str(actor_data['id']),
        "name": actor_data['name']}

    
