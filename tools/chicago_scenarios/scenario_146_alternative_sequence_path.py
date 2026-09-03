from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("alternative-sequence-path", '''PREFIX sh: <http://www.w3.org/ns/shacl#>
SELECT ?value WHERE { ?shape sh:property/(sh:path|sh:datatype) ?value } ORDER BY ?value''', 2)

