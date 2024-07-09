// load Question and Answer Pairs
// From 'QA_processed_data.csv'


// Load CSV file
LOAD CSV WITH HEADERS FROM 'file:///QA_processed_data.csv' AS row
WITH row, split(row.Technology, ', ') AS technologies, split(row.Source, ', ') AS sources, split(row.Form, ', ') AS forms
// Create or merge Question nodes
MERGE (q:Question {id:row.Index})
SET q.text = row.Question, q.answer = row.Answer

// Create or merge Source nodes and link to Question
FOREACH (source IN sources |
  FOREACH (_ IN CASE WHEN source IS NOT NULL THEN [1] ELSE [] END |
    MERGE (src:Source {url: source})
    SET src.last_update_time = row.`Last Update Time`
    MERGE (q)-[:HAS_SOURCE]->(src)
  )
)

// Create Technology, Service, Type, and ClassOfWork nodes, and link them hierarchically
FOREACH (tech IN technologies |
  MERGE (t:Technology {name: tech})

  // Create or merge Service nodes unique to each Technology
  MERGE (s:Service {name: row.Services, technology: tech})
  MERGE (t)-[:HAS_SERVICE]->(s)

  // Create or merge Type nodes unique to each Service
  FOREACH (type IN CASE WHEN row.Type IS NOT NULL THEN [row.Type] ELSE [] END |
    MERGE (ty:Type {name: type, service: row.Services, technology: tech})
    MERGE (s)-[:HAS_TYPE]->(ty)

    // Create or merge ClassOfWork nodes unique to each Type
    FOREACH (classOfWork IN CASE WHEN row.`Class Of Work` IS NOT NULL THEN [row.`Class Of Work`] ELSE [] END |
      MERGE (c:ClassOfWork {name: classOfWork, type: type, service: row.Services, technology: tech})
      MERGE (ty)-[:HAS_CLASS_OF_WORK]->(c)
      // Link question to ClassOfWork if it exists
      MERGE (q)-[:RELATED_TO_CLASS_OF_WORK]->(c)
    )
    // Link question to Type if ClassOfWork does not exist
    FOREACH (_ IN CASE WHEN row.`Class Of Work` IS NULL THEN [1] ELSE [] END |
      MERGE (q)-[:RELATED_TO_TYPE]->(ty)
    )
  )
  // Link question to Service if Type does not exist
  FOREACH (_ IN CASE WHEN row.Type IS NULL THEN [1] ELSE [] END |
    MERGE (q)-[:RELATED_TO_SERVICE]->(s)
  )
)


// Create or merge Form nodes and relationships, if applicable
FOREACH (form IN forms |
  MERGE (f:Form {name: form})
  MERGE (q)-[:RELATED_TO_FORM]->(f)
)