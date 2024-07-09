// Load Hierarchy from the sample data

// Create Nodes
LOAD CSV WITH HEADERS FROM 'file:///QA_sample_data.csv' AS row
MERGE (tech:Technology {name: row.Technology})
MERGE (serv:Service {name: row.Service, technology: row.Technology})
MERGE (typ:Category {name: row.Category, technology: row.Technology, service: row.Service})
MERGE (serv)-[:BELONGS_TO_TECHNOLOGY]->(tech)
MERGE (typ)-[:BELONGS_TO_SERVICE]->(serv)
MERGE (q:Question {text: row.Question, questionID: row.Index})
ON CREATE SET q.classOfWork = CASE WHEN row.`Class Of Work` <> "" THEN row.`Class Of Work` ELSE q.classOfWork END
MERGE (a:Answer {text: row.Answer})
ON CREATE SET a.updateTime = CASE WHEN row.`Answer Update Time` <> "" THEN row.`Answer Update Time` ELSE a.updateTime END
WITH row, q, a, typ
MERGE (src:Source {url: row.Source})
ON CREATE SET src.updateTime = CASE WHEN row.`Source Update Time` <> "" THEN row.`Source Update Time` ELSE src.updateTime END
MERGE (q)-[:BELONGS_TO_CATEGORY]->(typ)
MERGE (q)-[:HAS_ANSWER]->(a)
MERGE (q)-[:HAS_SOURCE]->(src)
FOREACH (i IN RANGE(0, size(split(COALESCE(row.Form, ''), ';')) - 1) |
  MERGE (f:Form {name: trim(split(COALESCE(row.Form, ''), ';')[i]), formID: trim(split(COALESCE(row.`Form ID`, ''), ';')[i])})
  MERGE (q)-[:HAS_FORM]->(f)
);

// Clean up empty Form nodes
MATCH (f:Form)
WHERE f.name IS NULL OR f.name = '' OR f.formID IS NULL OR f.formID = ''
DETACH DELETE f;


// Update dates in Answer nodes
MATCH (a:Answer)
SET a.updateTime = apoc.date.format(apoc.date.parse(a.updateTime, 'ms', 'MM/dd/yyyy'), 'ms', 'yyyy-MM-dd');

// Update dates in Source nodes
MATCH (src:Source)
WHERE src.updateTime IS NOT NULL
SET src.updateTime = apoc.date.format(apoc.date.parse(src.updateTime, 'ms', 'MM/dd/yyyy'), 'ms', 'yyyy-MM-dd');
