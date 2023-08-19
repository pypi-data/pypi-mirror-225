from raga import *

test_session = TestSession(project_name="testingProject",
                           run_name="labelling-18-aug-v6")

rules = LQRules()
rules.add(metric="loss", label=["All"], metric_threshold=0.005)


edge_case_detection = labelling_quality_test(test_session=test_session,
                                            dataset_name = "labelling-dataset-17-aug-v3",
                                            test_name = "Test",
                                            gt = "modelA",
                                            type = "labelling_consistency",
                                            rules = rules)
test_session.add(edge_case_detection)

test_session.run()