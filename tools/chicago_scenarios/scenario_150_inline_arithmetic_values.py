from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("inline-arithmetic-values", '''SELECT ?value WHERE { VALUES (?a ?b) { (2 3) (4 5) } BIND((?a * ?b) + 1 AS ?value) } ORDER BY ?value''', 2, inline_query=True)

