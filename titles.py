# from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom, Graph, Node
# class Title(GraphObject):
class Title:
  #__primarykey__ = "id"
  max_level = 3

  # uid = Property()
  # title = Property()
  # released = Property()

  # actors = RelatedFrom("Actor", "ACTED_IN")

  def __init__(self, uid, title, released, level=1):
    self.uid = uid
    self.title = title
    self.released = released
    self.level = level
    
  def create(self, tx, titles):
    actors_added = add_cast(tx, titles)

    if self.level > max_level:
      return
    elif self.level == max_level:
      tx.run("MERGE(b:Title {title: $title, uid: $uid})", uid=self.uid, title=self.title)
      return

    for actor in actors_added:
      if not actor.found:
        a = Actor(actor.uid, actor.name, self.level+1)
        # t.create()
    
  def add_cast(self, uids_names):
    pass

  def get_cast(self):
    pass
  
  # def find():
  
  # def list():
  