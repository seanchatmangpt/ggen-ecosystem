from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("negated-starts", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?value . FILTER(!STRSTARTS(STR(?value), "A")) } ORDER BY ?value''', 2)

