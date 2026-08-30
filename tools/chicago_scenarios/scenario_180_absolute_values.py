from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("absolute-values", '''SELECT ?value WHERE { VALUES ?n { -3 -2 -1 } BIND(ABS(?n) AS ?value) } ORDER BY ?value''', 3, inline_query=True)
