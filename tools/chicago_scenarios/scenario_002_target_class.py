from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("target-class", '''PREFIX sh: <http://www.w3.org/ns/shacl#>
SELECT ?value WHERE { ?s sh:targetClass ?value } ORDER BY ?value''', 2)
