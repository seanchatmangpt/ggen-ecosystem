from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("blank-object-filter", '''PREFIX sh: <http://www.w3.org/ns/shacl#>
SELECT ?value WHERE { ?shape sh:property ?value . FILTER(isBlank(?value)) } ORDER BY ?value''', 2)

