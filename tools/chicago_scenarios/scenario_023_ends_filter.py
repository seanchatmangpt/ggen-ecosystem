from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("ends-filter", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?value . FILTER(STRENDS(STR(?value), \"a\")) } ORDER BY ?value''', 3)
