from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("values-string-literals", '''SELECT ?value WHERE { VALUES ?value { "Alpha" "Beta" "Gamma" } } ORDER BY ?value''', 3, inline_query=True)
