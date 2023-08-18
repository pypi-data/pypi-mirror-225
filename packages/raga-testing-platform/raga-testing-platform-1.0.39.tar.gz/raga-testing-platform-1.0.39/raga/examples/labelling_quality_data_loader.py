from raga import *
import pandas as pd
import json
import datetime

def get_timestamp_x_hours_ago(hours):
    current_time = datetime.datetime.now()
    delta = datetime.timedelta(days=90, hours=hours)
    past_time = current_time - delta
    timestamp = int(past_time.timestamp())
    return timestamp

Annotations = SemanticSegmentationObject()
Annotations.add(SemanticSegmentation(Id=0, ClassId=0, ClassName="car", Format="xn,yn_normalised", Confidence=1))
Annotations.add(SemanticSegmentation(Id=0, ClassId=1, ClassName="background", Format="xn,yn_normalised", Confidence=1))
Loss = LossValue()
Loss.add(id=0, values = 0.01554573141)
Loss.add(id=1, values = 0.007743358146)
data = [
    {
        'ImageId': StringElement("abc_image.jpg"),
        'ImageUri': StringElement(f"https://lh4.googleusercontent.com/JDjSmaNIR-Px5svzdyVwpGd9B6S8vaCt0sWMxGjpkHOm-u6Q4lmJhVrRwq3oz8MGu3QrfyqjrrDo4CZUtgIa6d97ig=s400"),
        'TimeOfCapture': TimeStampElement(get_timestamp_x_hours_ago(1)),
        'SourceLink': StringElement("abc_image.jpg"),
        'Reflection':StringElement('Yes'),
        'Overlap':StringElement('No'),
        'CameraAngle':StringElement('Top'),
        'Annotations': Annotations,
        'LossValue':Loss
    }
]

pd_data_frame = pd.DataFrame(data)

print(data_frame_extractor(pd_data_frame))
# schema = RagaSchema()
# schema.add("ImageId", PredictionSchemaElement(), pd_data_frame)
# schema.add("ImageUri", ImageUriSchemaElement(), pd_data_frame)
# schema.add("TimeOfCapture", TimeOfCaptureSchemaElement(), pd_data_frame)
# schema.add("SourceLink", FeatureSchemaElement(), pd_data_frame)
# schema.add("Reflection", AttributeSchemaElement(), pd_data_frame)
# schema.add("Overlap", AttributeSchemaElement(), pd_data_frame)
# schema.add("CameraAngle", AttributeSchemaElement(), pd_data_frame)
# schema.add("Annotations", SemanticSegmentationSchemaElement(model="modelA"), pd_data_frame)
# schema.add("LossValue", LossValueSchemaElement(model="modelA"), pd_data_frame)

# #create test_session object of TestSession instance
# test_session = TestSession(project_name="testingProject",run_name= "run-17-aug-v2")

# # # #create test_ds object of Dataset instance
# test_ds = Dataset(test_session=test_session, name="dataset-17-aug-v1")

# # #load schema and pandas data frame
# test_ds.load(data=pd_data_frame, schema=schema)