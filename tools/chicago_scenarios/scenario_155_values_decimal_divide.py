from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("values-decimal-divide", '''SELECT ?value WHERE { VALUES ?n { 2 4 6 } BIND(?n / 2 AS ?value) } ORDER BY ?value''', 3, inline_query=True)
