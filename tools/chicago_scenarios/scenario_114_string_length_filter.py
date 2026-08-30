from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("string-length-filter", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?value . FILTER(STRLEN(STR(?value)) >= 4) } ORDER BY ?value''', 3)

