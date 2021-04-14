CREATE (sla:Actor {name:'Sanaa Lanthan', uid:"na1"})
CREATE (avp:Title {title: "Alien vs. Predator", released: '2004',uid:"mo1",title_type: "movie"})
CREATE (lnb:Title {title: "Love & Basketball", released: "2000",uid:"mo2",title_type: "movie"})
CREATE (sn:Title {title: "Something New", released: '2006',uid:'mo3',title_type: "movie"})
CREATE (bl:Title {title: "Blade", released: '1998',uid:"mo4",title_type: "movie"})
CREATE (sla)-[:ACTED_IN]->(avp),
    (sla)-[:ACTED_IN]->(lnb),
    (sla)-[:ACTED_IN]->(sn),
    (sla)-[:ACTED_IN]->(bl)

CREATE (kpa:Actor {name:'Kyla Pratt', uid:"na2"})
CREATE (oea:Actor {name:'Omar Epps', uid:"na3"})
CREATE (rha:Actor {name:'Regina Hall', uid:"na4"})
	

CREATE (kpa)-[:ACTED_IN]->(avp),
    (oea)-[:ACTED_IN]->(avp),
    (rha)-[:ACTED_IN]->(avp)

CREATE (tha:Actor {name:'Taraji P. Henson', uid:"na5"})
CREATE (mba:Actor {name:'Marcus Brown', uid:"na6"})
CREATE (rha2:Actor {name:'Russell Hornsby', uid:"na7"})
CREATE (sba:Actor {name:'Simon Baker', uid:"na8"})
CREATE (mea:Actor {name:'Mike Epps', uid:"na9"})

CREATE (tha)-[:ACTED_IN]->(sn),
    (mba)-[:ACTED_IN]->(sn),
    (rha2)-[:ACTED_IN]->(sn),
    (sba)-[:ACTED_IN]->(sn),
    (mea)-[:ACTED_IN]->(sn)

CREATE (wsa:Actor {name:'Wesley Snipes', uid:"na11"})

CREATE (wsa)-[:ACTED_IN]->(bl)