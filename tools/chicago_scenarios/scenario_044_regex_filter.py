from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("regex-filter", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?value . FILTER(REGEX(STR(?value), \"^(Alpha|Beta)$\")) } ORDER BY ?value''', 2)
