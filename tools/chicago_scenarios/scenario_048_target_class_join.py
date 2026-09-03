from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("target-class-join", '''PREFIX sh: <http://www.w3.org/ns/shacl#>
SELECT ?value WHERE { ?shape sh:targetClass ?class . ?value a ?class } ORDER BY ?value''', 3)
