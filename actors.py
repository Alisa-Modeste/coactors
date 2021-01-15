from py2neo import Graph
graph = Graph("bolt://neo4j:12345@localhost:7687")

class Actor(Model):
    __primarykey__ = "imdb_id"

  imdb_id = Property("tagline")
  name = Property()

  acted_in = RelatedTo(Images)
  
  def __init__(self, id, name):
    self.id = id
    self.name = name
    
    
  def add_image(image_imdb_id, title):
    a = Node("Actor", name=name, imdb_id=imdb_id)
    b = Node("Image", title=title, image_imdb_id=image_imdb_id)
    ACTED_IN = Relationship.type("ACTED_IN")
    graph.merge(ACTED_IN(a, b), "Image", "image_imdb_id")

  def add_images([ids_titles]):
  
  def list():
  
  def connected_actors():
    payload = tx.run('''Match (g:Guest)
      Where g.guest_id=$guest_id 
      Optional MATCH (g)-[r1:PAID_FOR]->(e:Event)
      Optional MATCH (g)-[r2:IS_AT_EVENT]->(e:Event)
      return r1 is not null as paid_for,r2 is not null as is_at''',guest_id=guest_id)
    
    for record in payload:
      return {'paid_for':record['paid_for'],'is_at':record['is_at']}
    
    return {}
  