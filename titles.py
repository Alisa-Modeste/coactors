from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom, Graph, Node
from initialClass import Title

class Title(Title):
  max_level = 3

  def __init__(self, uid, title, released, level=1):
    self.uid = uid
    self.title = title
    # self.released = released
    self.level = level
    
  def create(self, tx, cast_info):
    if self.level > Title.max_level:
      return
    elif self.level == Title.max_level:
      tx.run("MERGE(b:Title {title: $title, uid: $uid})", uid=self.uid, title=self.title)
      return

    actors_added = add_cast(tx, cast_info)

    for actor in actors_added:
      if not actor['found']:
        a = Actor(actor['uid'], actor['name'], self.level+1)
        # t.create()
    
  def add_cast(self, tx, cast_info):
    query = ""
    params = {"name": self.name, "uid": self.uid, "released": self.released}

    for i in range(0,len(cast_info)):
      query += "MERGE (t:Title {title: $title, uid: $uid, released: $released}) "
      query += f"MERGE (a{i}:Actor "
      query += "{name:$actors" + str(i) + "_name, uid:$actors" + str(i) + "_uid}) "
      query += f"""MERGE (a)-[:ACTED_IN]->(t{i}) 
      ON CREATE SET t{i}.found=FALSE 
      ON MATCH SET t{i}.found=TRUE 
      RETURN t{i}.found as found, t{i}.uid as uid, t{i}.title as title 
      UNION """

      params[f"titles{i}_uid"] = titles_info[i]["uid"]
      params[f"titles{i}_title"] = titles_info[i]["title"]

    query = query[:-6]
    return tx.run(query, params)

  def get_cast(self):
    pass
  
  # def find():
  
  # def list():
  