from py2neo.ogm import Property, Model

try:
    import py2neo_monkeypatch
    from db_admin import graph
except ImportError:
    import coactors.py2neo_monkeypatch
    from coactors.db_admin import graph

class Actor(Model):
    uid = Property()
    name = Property()
    children_known = Property()

    def __init__(self, uid, name):
        self.uid = uid
        self.name = name
        
    def add_title(self, tx, title_uid, title):
        tx.run("MATCH(a:Actor {uid: $uid}) "
            "MERGE(b:Title {title: $title, uid: $uid}) "
            "MERGE(a)-[:ACTED_IN]->(b) ", uid=self.uid, title=title, title_uid=title_uid)

    def add_titles(self, titles_info):
        try:
            from titles import Title
        except ImportError:
            from coactors.titles import Title

        query = """MERGE (a:Actor {uid: $uid}) 
                ON CREATE SET a += {name: $name} 
                SET a += {children_known: True} 

                WITH a 
                CALL {
                WITH a 
                UNWIND $batch as row 
                MERGE (_:Title {uid: row.uid}) 
                ON CREATE SET _ += {title: row.title, released: row.released, title_type: row.title_type} 
                MERGE (a)-[:ACTED_IN]->(_) 
                RETURN _ 
                }"""
            
        params = {"name": self.name, "uid": self.uid}
        batch = []

        for i in range(0,len(titles_info)):

            batch.append( {"uid": titles_info[i]["uid"], "title":titles_info[i]["title"],
            "released":titles_info[i]["released"],"title_type":titles_info[i]["title_type"]} )

        params['batch'] = batch
        return Title.match(graph ).raw_query(query, params)


    def get_coactors(self):
        return self.__class__.match(graph ).raw_query("""MATCH(a:Actor {uid: $uid})-[:ACTED_IN]->(b:Title) 
        <-[:ACTED_IN]-(_:Actor) 
        WHERE _.uid <> $uid  
        WITH distinct _ """ , {"uid":self.uid})

    def get_titles(self):
        try:
            from titles import Title
        except ImportError:
            from coactors.titles import Title
        return Title.match(graph ).raw_query("MATCH(a:Actor {uid: $uid})-[:ACTED_IN]->(_:Title) ", {"uid":self.uid})

    def get_groups_coactors(self, actor_uids):
        actor_uids.append(self.uid)

        return self.__class__.match(graph ).raw_query("""MATCH(a:Actor)-[r1:ACTED_IN]->(b:Title) 
            WHERE a.uid IN $actor_uids 
            WITH count(r1) as rels, b 
            WHERE rels = $rels 
            MATCH (b)<-[ACTED_IN]-(_:Actor) 
            WHERE NOT _.uid IN $actor_uids 
            WITH distinct _ """ , {"actor_uids":actor_uids, "rels": len(actor_uids)})



    def get_groups_titles(self, actor_uids):

        try:
            from titles import Title
        except ImportError:
            from coactors.titles import Title

        actor_uids.append(self.uid)

        return Title.match(graph ).raw_query("""MATCH(a:Actor)-[r1:ACTED_IN]->(_:Title) 
        WHERE a.uid IN $actor_uids 
        WITH count(r1) as rels, _ 
        WHERE rels = $rels 
        WITH distinct _ """, {"actor_uids":actor_uids, "rels": len(actor_uids)})

    def serialize(self):
        return {"uid": self.uid,
                "name": self.name,
                "children_known": self.children_known if self.children_known else False}
    
    def serialize2(self,titles, coactors, group_members=[]):
        title_list, coactor_list, member_list = [], [], []

        for title in titles:
            title_list.append( {"uid": title.uid,
            "title": title.title,
            "released": title.released,
            "children_known": title.children_known if title.children_known else False})

        for coactor in coactors:
            coactor_list.append( {"uid": coactor.uid,
                    "name": coactor.name, "children_known": coactor.children_known if coactor.children_known else False})

        for member in group_members:
            member_list.append( {"uid": member.uid,
                    "name": member.name, "children_known":member.children_known if member.children_known else False})

        return {"uid": self.uid,
                "name": self.name,
                "titles": title_list,
                "coactors": coactor_list,
                "group_members": member_list}

    @classmethod
    def find_by_uid(cls, uid):
        # py2neo's where() doesn't seem to allow for parameterized queries and so the related problem of SQL/Cypher injection
        actor = cls.match(graph).raw_query("MATCH (_:Actor {uid: $uid}) ", {'uid':uid})

        if actor:
            return actor[0]

    @classmethod
    def find_by_uids(cls, uids):
        # py2neo's where() doesn't seem to allow for parameterized queries and so the related problem of SQL/Cypher injection
        return cls.match(graph).raw_query("MATCH (_:Actor) WHERE _.uid IN $uids", {'uids':uids})


    @classmethod
    def find_by_name(cls, query):
        q_parts = query.replace(',',' ').split()

        where_clause = "WHERE _.name =~ $name"
        
        # It’s insensitive. Looks for words/names in any order
        # (?:(.*?)\\s|)x -- start searching at the beginning of a word
        # (?=...) -- any order via the lookahead
        params = {'name': "(?i)^(?=(?:(.*?)\\s|)" + ')(?=(?:(.*?)\\s|)'.join(q_parts) + ").*"}

        return cls.match(graph ).raw_query("MATCH (_:Actor) " + where_clause, params)


    @classmethod
    def get_all(cls, skip=0, limit=100):
        #here: created_date or alpha
        return cls.match(graph ).raw_query(
        "CALL { MATCH (_:Actor) return _ skip $skip limit $limit } ", {"skip": skip, "limit": limit}
        ) 

    @staticmethod
    def parse_filmography(actor_data):
        import json
        try:
            from titles import Title
        except ImportError:
            from coactors.titles import Title

        actor_data = json.loads(actor_data)

        titles = actor_data['combined_credits']['cast']

        result = []
        for title in titles:
            title_type = title['media_type']

            result.append( Title.parse_properties(title, title_type) )

        return {"titles": result, "uid": "na" + str(actor_data['id']),
            "name": actor_data['name']}

    
