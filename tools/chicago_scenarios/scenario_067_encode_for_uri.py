from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("encode-for-uri", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:name ?name . BIND(ENCODE_FOR_URI(CONCAT(STR(?name), " space")) AS ?value) } ORDER BY ?value''', 3)

