from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("uri-construction", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?name . BIND(URI(CONCAT("https://example.org/uri/", ENCODE_FOR_URI(STR(?name)))) AS ?value) } ORDER BY ?value''', 3)

