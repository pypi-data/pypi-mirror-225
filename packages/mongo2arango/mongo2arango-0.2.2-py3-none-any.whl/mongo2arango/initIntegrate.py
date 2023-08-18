from arango import ArangoClient
from models import User, Country, Location, Order, TravelGraph
from dotenv import load_dotenv
import os

load_dotenv()
ARANGODB_HOST = os.environ.get("ARANGODB_HOST")
ARANGODB_USER = os.environ.get("ARANGODB_USER")
ARANGODB_PW = os.environ.get("ARANGODB_PW")
DB_NAME = os.environ.get("ARANGODB_DB")

# ArangoDB connection
client = ArangoClient(hosts=ARANGODB_HOST)
db = client.db(DB_NAME, username=ARANGODB_USER, password=ARANGODB_PW)

# Create collections and relationships if they don't exist
if not db.has_collection(User.__collection__):
    db.create_collection(User)
if not db.has_collection(Country.__collection__):
    db.create_collection(Country)
if not db.has_collection(Location.__collection__):
    db.create_collection(Location)
if not db.has_collection(Order.__collection__):
    db.create_collection(Order)
if not db.has_graph(TravelGraph.__name__):
    db.create_graph(TravelGraph)

# Create relationships (edges) based on the models
# For simplicity, I'm showing just one example. You'd repeat this for all relationships.
users = db.collection(User.__collection__).all()
for user in users:
    if user.get("countryId"):
        db.graph(TravelGraph.__name__).create_edge(
            "UserCountry",
            {"_from": f"users/{user['_key']}", "_to": f"countries/{user['countryId']}"},
        )

# Validation
# Again, just showing one example for brevity.
edges = db.graph(TravelGraph.__name__).edge_collection("UserCountry").all()
for edge in edges:
    user = db.collection(User.__collection__).get(edge["_from"].split("/")[1])
    country = db.collection(Country.__collection__).get(edge["_to"].split("/")[1])
    if not user or not country:
        print(f"Invalid edge from User {edge['_from']} to Country {edge['_to']}")

print("Initialization and validation completed!")
