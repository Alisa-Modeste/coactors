from py2neo import Graph
from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom, Graph, Node
from initialClass import Title
graph = Graph("bolt://neo4j:12345@localhost:7687")

class Title(Title):
  # uid = Property()
  # title = Property()
  # released = Property()
  
  max_level = 3

  def __init__(self, uid, title, released, title_type, level=1):
    self.uid = uid
    self.title = title
    self.released = released
    self.level = level
    self.title_type = title_type
    
  def create(self, cast_info):
    from actors import Actor
    if self.level > Title.max_level:
      return
    elif self.level == Title.max_level:
      u = graph.run("MERGE(b:Title {title: $title, uid: $uid})", uid=self.uid, title=self.title)
      return

    return self.add_cast(cast_info)

    # for actor in actors_added:
    #   if not actor['found']:
    #     # a = Actor(actor['uid'], actor['name'], self.level+1)
    #     a = Actor(actor.uid, actor.name, self.level+1)
    #     # t.create()
    
  def add_cast(self, cast_info):
    from actors import Actor
    query = """MERGE (t:Title {title: $title, uid: $uid, released: $released, title_type: $title_type}) 
       SET t.children_known = True  """
    params = {"title": self.title, "uid": self.uid, "released": self.released, "title_type":self.title_type}

    actor_uids = []
    for i in range(0,len(cast_info)):
      query += f"MERGE (a{i}:Actor "
      query += "{name:$actors" + str(i) + "_name, uid:$actors" + str(i) + "_uid}) "
      query += f"""MERGE (a{i})-[:ACTED_IN]->(t) """
      # ON CREATE SET a{i}.found=FALSE 
      # ON MATCH SET a{i}.found=TRUE """

      params[f"actors{i}_uid"] = cast_info[i]["uid"]
      params[f"actors{i}_name"] = cast_info[i]["name"]
      actor_uids.append(cast_info[i]["uid"])

    # query = query[:-6]
    graph.run(query, params)
    #graph.run doesn't return results
    actors = Actor.match(graph ).raw_query("""MATCH (_:Actor) 
      WHERE _.uid IN $actor_uids """, {"actor_uids":actor_uids})

    return actors


  def get_cast(self):
    pass
  
  # def find():
  
  # def list():
  
  @staticmethod
  def parse_cast(cast):
    # from pprintpp import pprint
    # pprint(values)
    import json
    # import re
    cast = json.loads(cast)['cast']
    # print(mvalues[0])

    result = []
    for actor in cast:
      result.append({
        "uid": "na" + str(actor['id']),
        "name": actor['name'] }) #re.search("e/(.*)/", actor)[1] })

    return result