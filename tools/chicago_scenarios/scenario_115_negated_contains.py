from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("negated-contains", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?value . FILTER(!CONTAINS(STR(?value), "ph")) } ORDER BY ?value''', 2)

