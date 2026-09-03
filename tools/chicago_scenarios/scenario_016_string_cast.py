from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("string-cast", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:rank ?rank . BIND(STR(?rank) AS ?value) } ORDER BY ?value''', 3)
