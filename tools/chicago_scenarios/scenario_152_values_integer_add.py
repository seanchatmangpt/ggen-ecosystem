from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("ws3-152-values-integer-add", '''SELECT ?value WHERE { VALUES ?n { 1 2 3 } BIND(?n + 10 AS ?value) } ORDER BY ?value''', 3, inline_query=True)
