from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"])


def create_user(tx, username, password, role):
    hashed_password = pwd_context.hash(password)
    tx.run("""
        CREATE (u:User {username: $username, password: $password})
        WITH u
        MATCH (r:Role {name: $role})
        CREATE (u)-[:HAS_ROLE]->(r)
        """, username=username, password=hashed_password, role=role)


def get_user(tx, username):
    result = tx.run("""
        MATCH (u:User {username: $username})-[:HAS_ROLE]->(r:Role)
        RETURN u.username AS username, u.password AS password, r.name AS role
        """, username=username)
    record = result.single()
    if record:
        return {"username": record["username"], "password": record["password"], "role": record["role"]}
    return None


def authenticate_user(tx, username, password):
    user = get_user(tx, username)
    if user and pwd_context.verify(password, user["password"]):
        return user
    return None


def update_password(tx, username, new_password):
    hashed_password = pwd_context.hash(new_password)
    tx.run("""
        MATCH (u:User {username: $username})
        SET u.password = $password
        """, username=username, password=hashed_password)


def delete_user(tx, username):
    tx.run("""
        MATCH (u:User {username: $username})
        DETACH DELETE u
        """, username=username)