// Attach Form Questions

LOAD CSV WITH HEADERS FROM 'file:///QA_sample_form_question.csv' AS row
MATCH (f: Form {name:row.Form, formID:row.`Form ID`})
MERGE (fq: FormQuestion {text:row.Question, type:row.Type})
MERGE (f)-[:HAS]->(fq);