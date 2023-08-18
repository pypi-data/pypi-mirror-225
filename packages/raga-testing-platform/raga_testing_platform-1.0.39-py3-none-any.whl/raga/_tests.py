from typing import Optional
from raga import TestSession, ModelABTestRules, FMARules, LQRules

def model_ab_test(test_session:TestSession, dataset_name: str, test_name: str, modelA: str, modelB: str,
                  type: str, rules: ModelABTestRules, aggregation_level:  Optional[list] = [],
                  gt: Optional[str] = "", filter: Optional[str] = ""):
    dataset_id = ab_test_validation(test_session=test_session, dataset_name=dataset_name, test_name=test_name, modelA=modelA, modelB=modelB, type=type, rules=rules, gt=gt, aggregation_level=aggregation_level)    
    response = {
            "datasetId": dataset_id,
            "experimentId": test_session.experiment_id,
            "name": test_name,
            "modelA": modelA,
            "modelB": modelB,
            "type": type,
            "rules": rules.get(),
            "aggregationLevels": aggregation_level,
            'filter':filter,
            'gt':gt,
            'test_type':'ab_test'
        }
    return response


def ab_test_validation(test_session:TestSession, dataset_name: str, test_name: str, modelA: str, modelB: str,
               type: str, rules: ModelABTestRules,
               gt: Optional[str] = "", aggregation_level:Optional[list] = []):
    
    assert isinstance(test_session, TestSession), "test_session must be an instance of the TestSession."
    assert isinstance(dataset_name, str) and dataset_name, "dataset_name is required and must be str."

    res_data = test_session.http_client.get(f"api/dataset?projectId={test_session.project_id}&name={dataset_name}", headers={"Authorization": f'Bearer {test_session.token}'})
    if not isinstance(res_data, dict):
            raise ValueError("Invalid response data. Expected a dictionary.")
    dataset_id = res_data.get("data", {}).get("id")
    if not dataset_id:
        raise KeyError("Invalid response data. Token not found.")
    
    assert isinstance(test_name, str) and test_name, "test_name is required and must be an instance of the str."
    assert isinstance(modelA, str) and modelA, "modelA is required and must be an instance of the str."
    assert isinstance(modelB, str) and modelB, "modelB is required and must be an instance of the str."
    assert isinstance(type, str), "type must be an instance of the str."
    assert isinstance(rules, ModelABTestRules) and rules.get(), "rules is required and must be an instance of the ModelABTestRules class."

    if aggregation_level:
        assert isinstance(aggregation_level, list), "aggregation_level must be list."

    if type == "labelled":
        assert isinstance(gt, str) and gt, "gt is required on labelled type and must be an instance of the str."

    if type == "unlabelled":
        if isinstance(gt, str) and gt:
            raise ValueError("gt is not required on unlabelled type.")
    return dataset_id

def failure_mode_analysis(test_session:TestSession, dataset_name:str, test_name:str, model:str, gt:str, type:str, clustering=dict, rules=FMARules, output_type=str):
    dataset_id = failure_mode_analysis_validation(test_session, dataset_name, test_name, model, gt, type, clustering, rules, output_type)
    response = {
            "datasetId": dataset_id,
            "experimentId": test_session.experiment_id,
            "name": test_name,
            "model": model,
            "gt": gt,
            "type": type,
            "rules": rules.get(),
            "test_type":"cluster",
            "filter":"",
            "clustering":clustering,
            "outputType":output_type

        }
    return response

def failure_mode_analysis_validation(test_session:TestSession, dataset_name:str, test_name:str, model:str, gt:str, type:str, clustering=dict, rules=FMARules, output_type=str):
    assert isinstance(test_session, TestSession), "test_session must be an instance of the TestSession."
    assert isinstance(dataset_name, str) and dataset_name, "dataset_name is required and must be str."
    res_data = test_session.http_client.get(f"api/dataset?projectId={test_session.project_id}&name={dataset_name}", headers={"Authorization": f'Bearer {test_session.token}'})
    if not isinstance(res_data, dict):
            raise ValueError("Invalid response data. Expected a dictionary.")
    dataset_id = res_data.get("data", {}).get("id")
    if not dataset_id:
        raise KeyError("Invalid response data. Token not found.")
    assert isinstance(test_name, str) and test_name, "test_name is required and must be str."
    assert isinstance(model, str) and model, "model is required and must be str."
    assert isinstance(gt, str) and gt, "gt is required and must be str."
    assert isinstance(type, str) and type, "type is required and must be str."
    assert isinstance(clustering, dict) and clustering, "clustering is required and must be dict."
    assert isinstance(rules, FMARules) and rules, "rules is required and must be an instance of the FMARules."
    assert isinstance(output_type, str) and output_type, "output_type is required and must be str."
    return dataset_id

def clustering(method:str, embedding_col:str, level:str, args=dict):
    assert isinstance(method, str) and method, "method is required and must be str."
    assert isinstance(embedding_col, str) and embedding_col, "embedding_col is required and must be str."
    assert isinstance(level, str) and level, "level is required and must be str."

    response = {
        "method":method,
        "embeddingCol":embedding_col,
        "level":level,
        "args":args
    } 
    return response

def labelling_quality_test(test_session:TestSession, dataset_name:str, test_name:str, gt:str, type:str,rules=LQRules):
    dataset_id = labelling_quality_test_validation(test_session, dataset_name, test_name, gt, type, rules)
    response = {
            "datasetId": dataset_id,
            "experimentId": test_session.experiment_id,
            "name": test_name,
            "gt": gt,
            "type": type,
            "rules": rules.get(),
            "test_type":"labelling_quality",
            "filter":"",
        }
    return response

def labelling_quality_test_validation(test_session:TestSession, dataset_name:str, test_name:str, gt:str, type:str, rules=LQRules):
    assert isinstance(test_session, TestSession), "test_session must be an instance of the TestSession."
    assert isinstance(dataset_name, str) and dataset_name, "dataset_name is required and must be str."
    res_data = test_session.http_client.get(f"api/dataset?projectId={test_session.project_id}&name={dataset_name}", headers={"Authorization": f'Bearer {test_session.token}'})
    if not isinstance(res_data, dict):
            raise ValueError("Invalid response data. Expected a dictionary.")
    dataset_id = res_data.get("data", {}).get("id")
    if not dataset_id:
        raise KeyError("Invalid response data. Token not found.")
    assert isinstance(test_name, str) and test_name, "test_name is required and must be str."
    assert isinstance(gt, str) and gt, "gt is required and must be str."
    assert isinstance(type, str) and type, "type is required and must be str."
    assert isinstance(rules, LQRules) and rules, "rules is required and must be an instance of the FMARules."
    return dataset_id

