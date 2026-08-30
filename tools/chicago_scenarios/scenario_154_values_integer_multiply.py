from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("values-integer-multiply", '''SELECT ?value WHERE { VALUES ?n { 2 3 4 } BIND(?n * 3 AS ?value) } ORDER BY ?value''', 3, inline_query=True)
