from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("negated-ends", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?value . FILTER(!STRENDS(STR(?value), "z")) } ORDER BY ?value''', 3)

