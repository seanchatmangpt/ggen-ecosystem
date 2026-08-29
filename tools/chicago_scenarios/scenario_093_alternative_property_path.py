from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("alternative-property-path", '''PREFIX ex: <https://example.org/chicago-consumer#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
SELECT ?value WHERE { ?s (ex:name|rdfs:label) ?value } ORDER BY ?value''', 5)

