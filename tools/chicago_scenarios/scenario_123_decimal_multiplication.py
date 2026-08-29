from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("decimal-multiplication", '''PREFIX ex: <https://example.org/chicago-consumer#>
SELECT ?value WHERE { ?s ex:amount ?amount . BIND(?amount * 2.0 AS ?value) } ORDER BY ?value''', 3)

