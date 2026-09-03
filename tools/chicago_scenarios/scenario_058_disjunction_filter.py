from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("disjunction-filter", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:rank ?rank ; ex:name ?value . FILTER(?rank = 1 || ?rank = 3) } ORDER BY ?value''', 2)

