from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("peer-roundtrip-path", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name/^ex:name ?value } ORDER BY ?value''', 3)

