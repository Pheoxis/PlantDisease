from kedro.pipeline import Pipeline, node
from .nodes import parse_image_data, preprocess_image, model_prediction, format_prediction

def create_pipeline(**kwargs):
    return Pipeline(
        [
            node(
                func=parse_image_data, 
                inputs="input_data", 
                outputs="raw_image", 
                name="parse_image_node"
            ),
            node(
                func=preprocess_image, 
                inputs="raw_image", 
                outputs="processed_image", 
                name="preprocess_image_node"
            ),
            node(
                func=model_prediction, 
                inputs="processed_image", 
                outputs="prediction", 
                name="model_prediction_node"
            ),
            node(
                func=format_prediction, 
                inputs=["prediction"], 
                outputs="formatted_prediction", 
                name="format_prediction_node"
            )
        ]
    )
