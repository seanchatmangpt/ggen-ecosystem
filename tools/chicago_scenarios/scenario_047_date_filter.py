from chicago_consumer_matrix import Scenario
SCENARIO = Scenario("date-filter", '''PREFIX ex: <https://example.org/chicago-consumer#> PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?value WHERE { ?s ex:when ?value . FILTER(?value >= \"2026-08-30\"^^xsd:date) } ORDER BY ?value''', 2)
