from py2neo import Graph
from py2neo.ogm import Property, Graph, Model
graph = Graph("bolt://neo4j:12345@localhost:7687")

class Title(Model):
  uid = Property()
  title = Property()
  released = Property()
  children_known = Property()
  title_type = Property()
  
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

    
  def add_cast(self, cast_info):
    from actors import Actor

    query = """MERGE (t:Title {uid: $uid}) 
       SET t += {title: $title, released: $released, title_type: $title_type} 
       SET t.children_known = True  """
    params = {"title": self.title, "uid": self.uid, "released": self.released, "title_type":self.title_type}

    actor_uids = []
    for i in range(0,len(cast_info)):

      query += f"MERGE (a{i}:Actor " + "{uid:$actors" + str(i) + "_uid}) "
      query += f"SET a{i}.name = $actors" + str(i) + "_name "
      query += f"""MERGE (a{i})-[:ACTED_IN]->(t) """

      params[f"actors{i}_uid"] = cast_info[i]["uid"]
      params[f"actors{i}_name"] = cast_info[i]["name"]
      actor_uids.append(cast_info[i]["uid"])

    graph.run(query, params)

    return Actor.match(graph ).raw_query("""MATCH (_:Actor) 
      WHERE _.uid IN $actor_uids """, {"actor_uids":actor_uids})



  def get_cast(self):
    pass
  
  # def find():
  
  # def list():
  
  @staticmethod
  def parse_cast(title_data, title_type):
    import json

    title_data = json.loads(title_data) 
    cast = title_data['credits']['cast'] if 'credits' in title_data else title_data['aggregate_credits']['cast']

    uid = "tv" + str(title_data['id']) if title_type == "tv" else "mo" + str(title_data['id'])
    released =  title_data['first_air_date'][:4] if 'first_air_date' in title_data else title_data['release_date'][:4] if 'release_date' in title_data else "",
    title = title_data['title'] if title_type == 'movie' else title_data['name']

    result = []
    min_episodes = int(title_data['number_of_episodes'] * 0.05) if 'number_of_episodes' in title_data else None
    for actor in cast:
      if 'total_episode_count' in actor and actor['total_episode_count'] < min_episodes:
        continue
      result.append({
        "uid": "na" + str(actor['id']),
        "name": actor['name'] }) 

    return {'cast': result, 'uid': uid, 
      'released': released,
      "title_type": title_type,
      'title': title}