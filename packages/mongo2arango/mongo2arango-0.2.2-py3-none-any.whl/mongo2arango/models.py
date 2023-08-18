from arango_orm import Collection, Graph, fields
from arango_orm.references import relationship


class Country(Collection):
    __collection__ = "countries"
    _key = fields.String(required=True)  # This is the ID of the country


class User(Collection):
    __collection__ = "users"
    _key = fields.String(required=True)  # This is the ID of the user
    countryId = fields.String(allow_none=True)
    country = relationship(Country, "countryId")


class Location(Collection):
    __collection__ = "locations"
    _key = fields.String(required=True)  # This is the ID of the location
    countryId = fields.String(allow_none=True)
    country = relationship(Country, "countryId")


class Order(Collection):
    __collection__ = "orders"
    _key = fields.String(required=True)  # This is the ID of the order
    passengers = fields.List(fields.Dict())


class TravelGraph(Graph):
    __graph__ = "travel_graph"
    edge_definitions = [
        {
            "edge_collection": "UserCountry",
            "from_vertex_collections": ["users"],
            "to_vertex_collections": ["countries"],
        },
        {
            "edge_collection": "OrderUser",
            "from_vertex_collections": ["orders"],
            "to_vertex_collections": ["users"],
        },
        {
            "edge_collection": "OrderCountry",
            "from_vertex_collections": ["orders"],
            "to_vertex_collections": ["countries"],
        },
    ]
