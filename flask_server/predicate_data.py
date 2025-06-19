ETAG_VERSION = [1]

PREDICATE_JSON = [{
  "feature": ".x.y.z",
  "operation": {
    "operator": "and",
    "operations": [
      {
        "operator": "isNotNone"
      },
      {
        "operator": "isGreaterThan",
        "operand": 13
      },
      {
        "operator": "isLessThan",
        "operand": 45
      }
    ]
  }
}]

OPERATORS = ["and", "or"]

CONDITION_TYPES = ["isGreaterThan", "isEqualTo", "isLessThan"]
