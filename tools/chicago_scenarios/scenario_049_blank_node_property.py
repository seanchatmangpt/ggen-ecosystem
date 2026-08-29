from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("blank-node-property", '''PREFIX sh: <http://www.w3.org/ns/shacl#>
SELECT ?value WHERE { ?shape sh:property ?value . FILTER(isBlank(?value)) } ORDER BY ?value''', 2)
