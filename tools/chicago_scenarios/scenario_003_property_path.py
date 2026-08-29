from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("property-path", '''PREFIX sh: <http://www.w3.org/ns/shacl#>
SELECT ?value WHERE { ?s sh:property ?p . ?p sh:path ?value } ORDER BY ?value''', 2)
