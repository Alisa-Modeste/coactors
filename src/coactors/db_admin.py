from py2neo.ogm import Graph
try:
    from api import API
except ImportError:
    from coactors.api import API

try:
    neo4j_pw = API.get_secret("NEO4J_PASSWORD",2)
    graph = Graph(f"bolt://neo4j:{neo4j_pw}@54.146.245.71:7687")
except:
    graph = Graph("bolt://neo4j:12345@localhost:7687")