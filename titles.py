from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom, Graph, Node
class Title(GraphObject):
  #__primarykey__ = "id"

  uid = Property()
  title = Property()
  released = Property()

  actors = RelatedFrom("Actor", "ACTED_IN")

  def __init__(self, id, title):
    self.id = id
    self.title = title
    
    
  # def add_actor([imdb_ids_names]):
  
  # def find():
  
  # def list():
  