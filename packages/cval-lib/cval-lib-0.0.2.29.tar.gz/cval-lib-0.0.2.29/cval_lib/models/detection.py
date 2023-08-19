"""
Introducing CVAL Rest API, a powerful tool for AI developers in the computer vision field.
Our service combines the concepts of human-in-the-loop and active learning to improve the quality of
your models and minimize annotation costs for classification, detection, and segmentation cases.

With CVAL, you can iteratively improve your models by following our active learning loop.
First, manually or semi-automatically annotate a random set of images.
Next, train your model and use uncertainty and diversity methods to score the remaining images for annotation.
Then, manually or semi-automatically annotate the images marked as more confident to increase the accuracy of the model.
Repeat this process until you achieve an acceptable quality of the model.

Our service makes it easy to implement this workflow and improve your models quickly and efficiently.
Try our demo notebook to see how CVAL can revolutionize your computer vision projects.

To obtain a client_api_key, please send a request to k.suhorukov@digital-quarters.com
"""
from typing import List, Optional
from pydantic import validator

from pydantic import BaseModel, Field


class BBoxScores(BaseModel):
    """
    :param category_id: id of the category in FramePrediction namespace
    :param score: prediction of model on that bbox
    :param embedding_id: id of the embedding
    :param probabilities: the probabilities for each object category are relative to a predicted bounding box
    The order in the list is determined by the category number. sum must be = 1
    """
    category_id: Optional[str]
    score: Optional[float]
    embedding_id: Optional[str]
    probabilities: Optional[List[float]]

    @validator('score')
    def validate_score(cls, value):
        if not (0 < value < 1):
            raise ValueError('the predicted score should be in the range (0, 1)')
        return value

    @validator('probabilities')
    def validate_probabilities(cls, value: Optional[List[float]]):
        if value is not None:
            for prob in value:
                if prob < 0:
                    raise ValueError('Each probability must be > 0')
        return value


class FramePrediction(BaseModel):
    """
    :param frame_id: id of the frame
    :param predictions: bbox scores
    """
    frame_id: str = Field(max_length=32)
    predictions: Optional[List[BBoxScores]]


class DetectionSamplingOnPremise(BaseModel):
    """
    :param num_of_samples: absolute number of samples to select
    :param bbox_selection_policy:
    Which bounding box to select when there are multiple boxes on an image,
    according to their confidence.
    Supports: min, max, mean
    :param selection_strategy: Currently supports: margin, least, ratio, entropy, clustering
    :param probs_weights:
    Determines the significance (weight) of the prediction probability for each class.
    The order in the list corresponds to the order of the classes.
    It is essential for a multi-class entropy method.
    :param frames: prediction for th picture and the bbox
    :type frames: List[FramePrediction]
    :raises ValueError if value not in allowed
    """
    num_of_samples: int
    dataset_id: Optional[str]
    use_null_detections: bool = True
    bbox_selection_policy: Optional[str]
    selection_strategy: str
    sort_strategy: Optional[str]
    frames: List[FramePrediction]
    probs_weights: Optional[List[float]]
