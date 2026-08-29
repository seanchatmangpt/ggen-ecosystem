from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("shape-identity", '''PREFIX sh: <http://www.w3.org/ns/shacl#>\nSELECT ?value WHERE { ?value a sh:NodeShape } ORDER BY ?value''', 2)
