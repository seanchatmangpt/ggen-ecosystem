from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("if-false-branch", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:rank ?rank . BIND(IF(?rank > 99, "impossible", "reachable") AS ?value) } ORDER BY ?value''', 3)

