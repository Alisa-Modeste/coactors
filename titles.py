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
    from actors import Actor
    return Actor.match(graph ).raw_query("MATCH(t:Title {uid: $uid})<-[:ACTED_IN]-(_:Actor) ", {"uid":self.uid})
  
  # def find():
  
  # def list():
  
  @staticmethod
  def parse_cast(title_data, title_type):
    import json
    from titles import Title

    title_data = json.loads(title_data) 
    cast = title_data['credits']['cast'] if 'credits' in title_data else title_data['aggregate_credits']['cast']

    # uid = "tv" + str(title_data['id']) if title_type == "tv" else "mo" + str(title_data['id'])
    # released =  title_data['first_air_date'][:4] if 'first_air_date' in title_data else title_data['release_date'][:4] if 'release_date' in title_data else ""
    # title = title_data['title'] if title_type == 'movie' else title_data['name']
    properties = Title.parse_properties(title_data, title_type) 


    result = []
    min_episodes = int(title_data['number_of_episodes'] * 0.05) if 'number_of_episodes' in title_data else None
    for actor in cast:
      if 'total_episode_count' in actor and actor['total_episode_count'] < min_episodes:
        continue
      result.append({
        "uid": "na" + str(actor['id']),
        "name": actor['name'] }) 

    return {'cast': result, 'uid': properties['uid'], 
      'released': properties['released'],
      "title_type": title_type,
      'title': properties['title']}

  @classmethod
  def find_by_uid(cls, uid):
    #here: safe handling of where clause
    # where() doesn't seem to allow for parameterized queries and so the related problem of SQL/Cypher injection
    # return cls.match(graph).where(f"_.uid = '{uid}'").first()
    title = cls.match(graph).raw_query("MATCH (_:Title {uid: $uid}) ", {'uid':uid})

    if title:
      return title[0]

  @classmethod
  def find_by_title(cls, query):
    q_parts = query.replace(',',' ').split()
 
    where_clause = "WHERE _.title =~ $title"
    params = {'title': "(?i).*" + '.*'.join(q_parts) + ".*"} #"(?i)" + query + ".*"

    return cls.match(graph ).raw_query("MATCH (_:Title) " + where_clause, params)

  @classmethod
  def parse_properties(cls, result, title_type=None, prepend=True):
    if prepend:
      uid = "mo" + str(result['id']) if title_type == 'movie' else "tv" + str(result['id'])
    else:
      uid = str(result['id'])

    title = result['title'] if title_type == 'movie' else result['name']
    released = result['first_air_date'][:4] if 'first_air_date' in result else result['release_date'][:4] if 'release_date' in result else ""
    title_type = title_type if title_type else result['media_type']

    return {
        "uid": uid,
        "title": title, 
        "released": released,
        "title_type": title_type
      }

    # if title_type:
    #   return {
    #     "uid": "mo" + str(result['id']) if title_type == 'movie' else "tv" + str(result['id']),
    #     "title": result['title'] if title_type == 'movie' else result['name'], 
    #     "released": result['first_air_date'][:4] if 'first_air_date' in result else result['release_date'][:4] if 'release_date' in result else "",
    #     "title_type": title_type
    #   }
    # else:
    #   return {
    #     "uid": "mo" + str(result['id']) if result['media_type'] == 'movie' else "tv" + str(result['id']),
    #     "title": result['title'] if result['media_type'] == 'movie' else result['name'], 
    #     "released": result['first_air_date'][:4] if 'first_air_date' in result else result['release_date'][:4] if 'release_date' in result else "",
    #     "title_type": result['media_type']
    #   }