from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("regex-case-insensitive", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?value . FILTER(REGEX(STR(?value), "^alpha$", "i")) } ORDER BY ?value''', 1)

