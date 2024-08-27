from datetime import datetime



def add_question(tx, question, answer, product, technologies, username):
    tx.run("""
        MATCH (u:User {username: $username})
        CREATE (q:Question {text: $question, answer: $answer, verified: false, last_modified: $last_modified, frequency: 0, likes: 0, outdated_count: 0})
        CREATE (u)-[:CREATED]->(q)
        WITH q
        UNWIND $technologies AS tech
        MATCH (t:Technology {name: tech, type:$product})
        CREATE (q)-[:BELONGS_TO]->(t)
        """, question=question, answer=answer, product=product, technologies=technologies, last_modified=datetime.now().isoformat(), username=username)


def get_unverified_qas(tx, product, technology):
    query = """
        MATCH (q:Question {verified: false})-[:BELONGS_TO]->(t:Technology)
    """
    if product != "All":
        query += " WHERE t.type = $product"
    if technology != "All":
        if product == "All":
            query += " WHERE t.name = $technology"
        else:
            query += " AND t.name = $technology"
    query += " RETURN q.text AS question, q.answer AS answer, q.last_modified AS last_modified"

    result = tx.run(query, product=product, technology=technology)
    return [{"question": record["question"], "answer": record["answer"], "last_modified": record["last_modified"]} for record in result]


def get_all_qas(tx, product, technology):
    query = """
        MATCH (q:Question)-[:BELONGS_TO]->(t:Technology)
    """
    if product != "All":
        query += " WHERE t.type = $product"
    if technology != "All":
        if product == "All":
            query += " WHERE t.name = $technology"
        else:
            query += " AND t.name = $technology"
    query += " RETURN q.text AS question, q.answer AS answer, q.verified AS verified, q.last_modified AS last_modified, q.frequency AS frequency, q.likes AS likes, q.outdated_count AS outdated_count"

    result = tx.run(query, product=product, technology=technology)


    return [{"question": record["question"], "answer": record["answer"], "verified": record["verified"], "last_modified": record["last_modified"], "frequency": record.get("frequency", 0), "likes": record.get("likes", 0), "outdated_count": record.get("outdated_count", 0)} for record in result]


def update_question(tx, original_question, new_question, new_answer, username):
    tx.run("""
        MATCH (q:Question {text: $original_question})
        SET q.text = $new_question, q.answer = $new_answer, q.last_modified = $last_modified
        WITH q
        MATCH (u:User {username: $username})
        CREATE (u)-[:UPDATED]->(q)
        """, original_question=original_question, new_question=new_question, new_answer=new_answer, last_modified=datetime.now().isoformat(), username=username)


def verify_question(tx, question, username):
    tx.run("""
        MATCH (q:Question {text: $question})
        SET q.verified = true
        WITH q
        MATCH (u:User {username: $username})
        CREATE (u)-[:VERIFIED]->(q)
        """, question=question, username=username)


def update_frequency(tx, question, username):
    tx.run("""
        MATCH (q:Question {text: $question})
        MATCH (u:User {username: $username})
        SET q.frequency = COALESCE(q.frequency, 0) + 1
        CREATE (u)-[:REFERRED]->(q)
        """, question=question, username=username)


def update_likes(tx, question, username):
    tx.run("""
        MATCH (q:Question {text: $question})
        MATCH (u:User {username: $username})
        SET q.likes = COALESCE(q.likes, 0) + 1
        CREATE (u)-[:LIKED]->(q)
        """, question=question, username=username)


def update_outdated(tx, question, username):
    result = tx.run("""
        MATCH (q:Question {text: $question})
        MATCH (u:User {username: $username})
        SET q.outdated_count = COALESCE(q.outdated_count, 0) + 1
        CREATE (u)-[:MARKED_OUTDATED]->(q)
        RETURN q.outdated_count AS outdated_count
        """, question=question, username=username)
    record = result.single()
    return record["outdated_count"]



def mark_unverified(tx, question):
    tx.run("""
        MATCH (q:Question {text: $question})
        SET q.verified = false, q.outdated_count = 0
        """, question=question)


def remove_question(tx, question):
    tx.run("""
        MATCH (q:Question {text: $question})
        DETACH DELETE q
        """, question=question)


def search_qas(qas, search_query):
    return [qa for qa in qas if search_query.lower() in qa['question'].lower()]