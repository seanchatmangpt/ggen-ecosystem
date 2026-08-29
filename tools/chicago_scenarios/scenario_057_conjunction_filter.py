from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("conjunction-filter", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:rank ?rank ; ex:enabled ?enabled ; ex:name ?value . FILTER(?rank > 1 && ?enabled) } ORDER BY ?value''', 1)

