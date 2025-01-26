from typing import Any, List, Optional, Tuple

import cv2
import numpy as np

from savant.base.converter import BaseComplexModelOutputConverter
from savant.base.model import AttributeModel
from savant.base.model import ComplexModel

class TrackNetPoseExtractor(BaseComplexModelOutputConverter):


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
        model: ComplexModel,
        roi: Tuple[float, float, float, float],
    ) -> Tuple[np.ndarray, List[List[Tuple[str, Any, float]]]]:
        
    
        pred = output_layers[0]
        print(pred.shape)
        print(pred)
        points = []
        # Process heatmaps and find keypoints
        # for kps_num in range(14):
        #     heatmap = (pred[kps_num] * 255).astype(np.uint8)  # Convert to uint8 for visualization

        #     # Postprocess heatmap to find keypoints
        #     x_pred, y_pred = self.postprocess(heatmap, scale=1, low_thresh=170, max_radius=25)
        #     points.append((x_pred, y_pred))


        return None, None