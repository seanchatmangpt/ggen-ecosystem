from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("iri-construction", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?name . BIND(IRI(CONCAT("https://example.org/generated/", ENCODE_FOR_URI(STR(?name)))) AS ?value) } ORDER BY ?value''', 3)

