from py2neo.ogm import Property, Model

try:
    import py2neo_monkeypatch
    from db_admin import graph
except ImportError:
    import coactors.py2neo_monkeypatch
    from coactors.db_admin import graph

class Title(Model):
    uid = Property()
    title = Property()
    released = Property()
    children_known = Property()
    title_type = Property()

    def __init__(self, uid, title, released, title_type):
        self.uid = uid
        self.title = title
        self.released = released
        self.title_type = title_type
    
    def add_cast(self, cast_info):
        try:
            from actors import Actor
        except ImportError:
            from coactors.actors import Actor

        query = """MERGE (t:Title {uid: $uid}) 
            ON CREATE SET t += {title: $title, released: $released, title_type: $title_type} 
            SET t.children_known = True  
            WITH t 
            CALL {
                WITH t 
                UNWIND $batch as row 
                MERGE (_:Actor {uid: row.uid}) 
                ON CREATE SET _ += {name: row.name} 
                MERGE (_)-[:ACTED_IN]->(t) 
                RETURN _ 
            }"""
        params = {"title": self.title, "uid": self.uid, "released": self.released, "title_type":self.title_type}
        batch = []

        for i in range(0,len(cast_info)):

            batch.append( {"uid": cast_info[i]["uid"], "name":cast_info[i]["name"]} )

        params['batch'] = batch
        return Actor.match(graph ).raw_query(query, params)



    def get_cast(self):
        try:
            from actors import Actor
        except ImportError:
            from coactors.actors import Actor
        return Actor.match(graph ).raw_query("MATCH(t:Title {uid: $uid})<-[:ACTED_IN]-(_:Actor) ", {"uid":self.uid})
  
    @staticmethod
    def parse_cast(title_data, title_type):
        import json
        try:
            from titles import Title
        except ImportError:
            from coactors.titles import Title

        title_data = json.loads(title_data) 
        cast = title_data['credits']['cast'] if 'credits' in title_data else title_data['aggregate_credits']['cast']

        properties = Title.parse_properties(title_data, title_type) 


        result = []
        min_episodes = int(title_data['number_of_episodes'] * 0.05) if 'number_of_episodes' in title_data else None
        min_episodes = 0 if min_episodes and cast[0]['total_episode_count'] < min_episodes else min_episodes
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
        # py2neo's where() doesn't seem to allow for parameterized queries and so the related problem of SQL/Cypher injection
        title = cls.match(graph).raw_query("MATCH (_:Title {uid: $uid}) ", {'uid':uid})

        if title:
            return title[0]

    @classmethod
    def find_by_title(cls, query):
        q_parts = query.replace(',',' ').split()
    
        where_clause = "WHERE _.title =~ $title"

        # It???s insensitive. Looks for words in any order
        # (?:(.*?)\\s|)x -- start searching at the beginning of a word
        # (?=...) -- any order via the lookahead
        params = {'title': "(?i)^(?=(?:(.*?)\\s|)" + ')(?=(?:(.*?)\\s|)'.join(q_parts) + ").*"}

        return cls.match(graph ).raw_query("MATCH (_:Title) " + where_clause, params)

    @classmethod
    def parse_properties(cls, result, title_type=None, prepend=True):
        if prepend:
            uid = "mo" + str(result['id']) if title_type == 'movie' else "tv" + str(result['id'])
        else:
            uid = str(result['id'])

        title_type = title_type if title_type else result['media_type']
        title = result['title'] if title_type == 'movie' else result['name']
        released = result['first_air_date'][:4] if 'first_air_date' in result else result['release_date'][:4] if 'release_date' in result else ""

        return {
            "uid": uid,
            "title": title, 
            "released": released,
            "title_type": title_type
        }

    @classmethod
    def get_all(cls, skip=0, limit=100):
        #here: created_date or alpha
        return cls.match(graph ).raw_query(
        "CALL { MATCH (_:Title) RETURN _ ORDER BY _.children_known skip $skip limit $limit } ", {"skip": skip, "limit": limit}
        ) 

    def serialize(self):
        return {"uid": self.uid,
            "title": self.title,
            "released": self.released,
            "children_known": self.children_known if self.children_known else False}
          
    def serialize2(self,cast):
        cast_list = []

        for actor in cast:
            cast_list.append( {"uid": actor.uid,
                "name": actor.name,
                "children_known": actor.children_known if actor.children_known else False})

        return {"uid": self.uid,
            "title": self.title,
            "released": self.released,
            "cast": cast_list}