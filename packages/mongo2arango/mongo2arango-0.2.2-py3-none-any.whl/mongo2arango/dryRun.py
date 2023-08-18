from arango import ArangoClient
from models import User, Country, Location, Order, TravelGraph
from dotenv import load_dotenv
import os
import json

load_dotenv()
ARANGODB_HOST = os.environ.get("ARANGODB_HOST")
ARANGODB_USER = os.environ.get("ARANGODB_USER")
ARANGODB_PW = os.environ.get("ARANGODB_PW")
DB_NAME = os.environ.get("ARANGODB_DB")

# ArangoDB connection
client = ArangoClient(hosts=ARANGODB_HOST)
db = client.db(DB_NAME, username=ARANGODB_USER, password=ARANGODB_PW)

# Initialize counters and example lists
connection_stats = {
    "UserCountry": {
        "validated": 0,
        "failed": 0,
    },
    "OrderUser": {
        "validated": 0,
        "failed": 0,
    },
    "OrderCountry": {
        "validated": 0,
        "failed": 0,
    },
}

# Simulate creating relationships without actually doing it
users = db.collection(User.__collection__).all()
for user in users:
    if user.get("countryId"):
        connection_stats["UserCountry"]["validated"] += 1

    else:
        connection_stats["UserCountry"]["failed"] += 1

orders = db.collection(Order.__collection__).all()
for order in orders:
    for passenger in order.get("passengers", []):
        if passenger.get("userId"):
            connection_stats["OrderUser"]["validated"] += 1

        else:
            connection_stats["OrderUser"]["failed"] += 1

        if passenger.get("countryId"):
            connection_stats["OrderCountry"]["validated"] += 1

        else:
            connection_stats["OrderCountry"]["failed"] += 1

# Calculate percentages
total_validated = sum([stats["validated"] for stats in connection_stats.values()])
total_failed = sum([stats["failed"] for stats in connection_stats.values()])

for connection, stats in connection_stats.items():
    stats["%_of_total_validated"] = (stats["validated"] / total_validated) * 100
    stats["%_of_total_failed"] = (stats["failed"] / total_failed) * 100

with open("/logs/connection_stats.json", "w") as f:
    f.write(json.dumps(connection_stats, indent=4))
