class Actor:
  def __init__(self, id, name):
    self.id = id
    self.name = name
    
    
  def add_image(id, title):
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
  