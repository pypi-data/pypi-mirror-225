from raga import *

test_session = TestSession(project_name="testingProject",
                           run_name="labelling-11-aug-v2")

rules = LQRules()
rules.add(metric="loss", label=["All"], metric_threshold=0.005)


edge_case_detection = labelling_quality_test(test_session=test_session,
                                            dataset_name = "dataset-7-aug-v3",
                                            test_name = "Test",
                                            gt = "groundtruth",
                                            type = "labelling_consistency",
                                            rules = rules)
print(edge_case_detection)
# test_session.add(edge_case_detection)

# test_session.run()