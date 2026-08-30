from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ws3-156-values-unary-minus", '''SELECT ?value WHERE { VALUES ?n { 1 2 3 } BIND(-?n AS ?value) } ORDER BY ?value''', 3, inline_query=True)
