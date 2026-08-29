from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("inline-values-pairs", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { VALUES (?s ?value) { (ex:a "Alpha") (ex:c "Gamma") } FILTER EXISTS { ?s ex:name ?value } } ORDER BY ?value''', 2, inline_query=True)

