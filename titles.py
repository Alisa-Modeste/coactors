from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom, Graph, Node
class Title(GraphObject):
  #__primarykey__ = "id"

  uid = Property()
  title = Property()
  released = Property()

  actors = RelatedFrom("Actor", "ACTED_IN")

  def __init__(self, uid, title, released):
    self.uid = uid
    self.title = title
    self.released = released
    
    
  def add_cast(uids_names):
    pass

  def get_cast():
    pass
  
  # def find():
  
  # def list():
  