from chicago_consumer_matrix import Scenario

SCENARIO = Scenario("uri-subject-filter", '''SELECT ?value WHERE { ?value ?p ?o . FILTER(isURI(?value)) } ORDER BY ?value''', 1)

