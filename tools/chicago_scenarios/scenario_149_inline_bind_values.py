from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("inline-bind-values", '''SELECT ?value WHERE { VALUES ?n { 1 2 3 } BIND(?n + 100 AS ?value) } ORDER BY ?value''', 3, inline_query=True)

