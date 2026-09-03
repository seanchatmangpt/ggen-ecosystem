from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("starts-filter", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?value . FILTER(STRSTARTS(STR(?value), \"A\")) } ORDER BY ?value''', 1)
