import streamlit as st
import os
from neo4j import GraphDatabase
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initalize connection to Neo4j
NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USERNAME")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def get_driver():
    return driver


def create_graph():
    with driver.session() as session:
        session.run("""
        // Roles
        MERGE (adminRole:Role {name: 'Admin'})
        MERGE (ssrRole:Role {name: 'SSR'})
                    
        // Products
        MERGE (p1:Product {name: 'Permit'})
        MERGE (p2:Product {name: 'Certification'})
        MERGE (p3:Product {name: 'Licenses'})
        MERGE (p4:Product {name: 'Other'})
        
        // Technologies under Permit
        MERGE (t1:Technology {name: 'Electrical', type: 'Permit'})
        MERGE (t2:Technology {name: 'Gas', type: 'Permit'})
        MERGE (t3:Technology {name: 'BPVR', type: 'Permit'})
        MERGE (t4:Technology {name: 'Elevating Devices', type: 'Permit'})
        MERGE (t5:Technology {name: 'Passenger Ropeways', type: 'Permit'})
        MERGE (t6:Technology {name: 'Railways', type: 'Permit'})
        MERGE (t7:Technology {name: 'Amusement Devices', type: 'Permit'})

        // Technologies under Certification
        MERGE (t8:Technology {name: 'Electrical', type: 'Certification'})
        MERGE (t9:Technology {name: 'Gas', type: 'Certification'})
        MERGE (t10:Technology {name: 'BPVR', type: 'Certification'})
        MERGE (t11:Technology {name: 'Elevating Devices', type: 'Certification'})
        MERGE (t12:Technology {name: 'Passenger Ropeways', type: 'Certification'})
        MERGE (t13:Technology {name: 'Railways', type: 'Certification'})
        MERGE (t14:Technology {name: 'Amusement Devices', type: 'Certification'})
        
        // Technologies under Licenses
        MERGE (t15:Technology {name: 'Electrical', type: 'Licenses'})
        MERGE (t16:Technology {name: 'Gas', type: 'Licenses'})
        MERGE (t17:Technology {name: 'BPVR', type: 'Licenses'})
        MERGE (t18:Technology {name: 'Elevating Devices', type: 'Licenses'})
        MERGE (t19:Technology {name: 'Passenger Ropeways', type: 'Licenses'})
        MERGE (t20:Technology {name: 'Railways', type: 'Licenses'})
        MERGE (t21:Technology {name: 'Amusement Devices', type: 'Licenses'})
        
        // Technologies under Other
        MERGE (t22:Technology {name: 'Electrical', type: 'Other'})
        MERGE (t23:Technology {name: 'Gas', type: 'Other'})
        MERGE (t24:Technology {name: 'BPV', type: 'Other'})
        MERGE (t25:Technology {name: 'Elevating Devices', type: 'Other'})
        MERGE (t26:Technology {name: 'Passenger Ropeways', type: 'Other'})
        MERGE (t27:Technology {name: 'Railways', type: 'Other'})
        MERGE (t28:Technology {name: 'Amusement Devices', type: 'Other'})
        
        // Relationships
        MERGE (p1)-[:HAS]->(t1)
        MERGE (p1)-[:HAS]->(t2)
        MERGE (p1)-[:HAS]->(t3)
        MERGE (p1)-[:HAS]->(t4)
        MERGE (p1)-[:HAS]->(t5)
        MERGE (p1)-[:HAS]->(t6)
        MERGE (p1)-[:HAS]->(t7)
     
        MERGE (p2)-[:HAS]->(t8)
        MERGE (p2)-[:HAS]->(t9)
        MERGE (p2)-[:HAS]->(t10)
        MERGE (p2)-[:HAS]->(t11)
        MERGE (p2)-[:HAS]->(t12)
        MERGE (p2)-[:HAS]->(t13)
        MERGE (p2)-[:HAS]->(t14)
        
        MERGE (p3)-[:HAS]->(t15)
        MERGE (p3)-[:HAS]->(t16)
        MERGE (p3)-[:HAS]->(t17)
        MERGE (p3)-[:HAS]->(t18)
        MERGE (p3)-[:HAS]->(t19)
        MERGE (p3)-[:HAS]->(t20)
        MERGE (p3)-[:HAS]->(t21)
        MERGE (p3)-[:HAS]->(t22)
                    
        MERGE (p4)-[:HAS]->(t23)
        MERGE (p4)-[:HAS]->(t24)
        MERGE (p4)-[:HAS]->(t25)
        MERGE (p4)-[:HAS]->(t26)
        MERGE (p4)-[:HAS]->(t27)
        MERGE (p4)-[:HAS]->(t28)
        """)

# Run this function to create base nodes if they don't exist
create_graph()