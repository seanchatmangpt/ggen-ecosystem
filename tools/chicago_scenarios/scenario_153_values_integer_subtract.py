from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ws3-153-values-integer-subtract", '''SELECT ?value WHERE { VALUES ?n { 4 5 6 } BIND(?n - 1 AS ?value) } ORDER BY ?value''', 3, inline_query=True)
