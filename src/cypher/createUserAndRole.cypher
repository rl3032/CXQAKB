CREATE CONSTRAINT FOR (u:User) REQUIRE u.username IS UNIQUE;

CREATE (adminRole:Role {name: 'Admin'});
CREATE (csrRole:Role {name: 'CSR'});
CREATE (ssrRole:Role {name: 'SSR'});

MATCH (adminRole:Role {name: 'Admin'})
CREATE (admin:User {username: 'admin', password: "123456"})-[:HAS_ROLE]->(adminRole);
