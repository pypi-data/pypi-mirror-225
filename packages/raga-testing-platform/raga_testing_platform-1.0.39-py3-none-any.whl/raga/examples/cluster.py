from raga import *

project_name = "testingProject"
run_name = "drift-7-aug-v4"

test_session = TestSession(project_name="testingProject",
                           run_name="cluster-9-aug-v1")

rules = FMARules()
rules.add(metric="Precision", conf_threshold=0.8, label=["All"], metric_threshold=0.5)

cls_default = clustering(method ="k-means", embedding_col="dataset-7-aug-v3", level="roi", args= {"num_of_clusters": 5})

edge_case_detection = failure_mode_analysis(test_session=test_session,
                                            dataset_name = "dataset-7-aug-v3",
                                            test_name = "Test",
                                            model = "model",
                                            gt = "groundtruth",
                                            type = "embeddings",
                                            clustering = cls_default,
                                            rules = rules,
                                            output_type="multi-label")

test_session.add(edge_case_detection)

test_session.run()