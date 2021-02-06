from py2neo.ogm import GraphObject, Property, RelatedTo, RelatedFrom, Graph, Node, Model

""" 
the beginning of these definitions are here to prevent a circular import situation
since each class takes the other as a parameter
"""
class Title(GraphObject):
# class Title:
  #__primarykey__ = "id"

  uid = Property()
  title = Property()
  released = Property()
  found = Property()

  # actors = RelatedFrom("Actor2", "ACTED_IN")
  # from actors_py2neo import Actor
  


class Actor(Model):
    # class Actor:
    #__primarykey__ = "id"

  uid = Property()
  id = Property()
  name = Property()
  found = Property()

  acted_in = RelatedTo(Title)

class Title(Title):
  actors = RelatedFrom(Actor, "ACTED_IN")


# t =Title
# print(t.actors)