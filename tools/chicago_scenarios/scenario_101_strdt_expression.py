from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("strdt-expression", '''PREFIX ex: <https://example.org/chicago-consumer#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
SELECT ?value WHERE { ?s ex:rank ?rank . BIND(STRDT(STR(?rank), xsd:string) AS ?value) } ORDER BY ?value''', 3)

