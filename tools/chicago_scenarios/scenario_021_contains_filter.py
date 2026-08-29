from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("contains-filter", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?value . FILTER(CONTAINS(STR(?value), \"a\")) } ORDER BY ?value''', 3)
