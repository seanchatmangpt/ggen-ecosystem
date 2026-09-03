from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("equality-filter", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?value . FILTER(?value = \"Alpha\") } ORDER BY ?value''', 1)
