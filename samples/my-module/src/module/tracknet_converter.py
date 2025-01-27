from typing import Any, List, Optional, Tuple

import cv2
import numpy as np

from savant.base.converter import BaseAttributeModelOutputConverter
from savant.base.model import AttributeModel
from savant.parameter_storage import param_storage
FRAME = param_storage()['frame']

class TrackNetPoseExtractor(BaseAttributeModelOutputConverter):


    def __init__(
            self,
            **kwargs
    ):
        
        super().__init__(**kwargs)

    
    def postprocess(self,heatmap, scale=2, low_thresh=155, min_radius=10, max_radius=30):
        x_pred, y_pred = None, None
        ret, heatmap = cv2.threshold(heatmap, low_thresh, 255, cv2.THRESH_BINARY)
        circles = cv2.HoughCircles(heatmap, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=50, param2=2, minRadius=min_radius,
                                maxRadius=max_radius)
        if circles is not None:
            x_pred = circles[0][0][0] * scale
            y_pred = circles[0][0][1] * scale
        return x_pred, y_pred

    def __call__(
        self,
        *output_layers: np.ndarray,
        model: AttributeModel,
        roi: Tuple[float, float, float, float],
    ) -> Tuple[np.ndarray, List[List[Tuple[str, Any, float]]]]:
        # Suppose the model has 1 output layer: a 14xH xW heatmap
        pred = output_layers[0]
        pred = (pred * 255).astype(np.uint8)

        keypoints = []

        print("frame:", FRAME)
        print(pred.shape[1])

        scale = FRAME['height'] // model.input.height

        for i in range(14):
            heatmap = pred[i]
            x_pred, y_pred = self.postprocess(heatmap, scale=scale, low_thresh=170, max_radius=25)
            # Convert (x_pred, y_pred) to list so Savant can serialize it
            keypoints.append([float(x_pred), float(y_pred)])


        attributes_output = [
            
                ("keypoints", np.array(keypoints), 1.0)
            
        ]
        print("attrs:",attributes_output)

        return attributes_output 