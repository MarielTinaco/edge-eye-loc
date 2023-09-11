import os
from pathlib import Path
from dataclasses import dataclass
from typing import Union, List, Tuple
from PIL import Image

@dataclass
class Landmark:
        left_brow :     List[Tuple[float, float]]
        right_brow :    List[Tuple[float, float]]
        left_eye :      List[Tuple[float, float]]
        right_eye:      List[Tuple[float, float]]
        nose:           List[Tuple[float, float]]
        lower_face:     List[Tuple[float, float]]
        outer_lips:     List[Tuple[float, float]]
        inner_lips:     List[Tuple[float, float]]
        left_eye_lash:  List[Tuple[float, float]]
        left_eye_lid:   List[Tuple[float, float]]
        right_eye_lash: List[Tuple[float, float]]
        right_eye_lid:  List[Tuple[float, float]]
        face:           List[Tuple[float, float]]

class FaceLandmarkImage:

        def __init__(self, landmarks : Landmark, image = None, image_path : Union[Path, str] = None):
                self._landmarks = landmarks

                if image:
                        self._image = Image(image)
                        print("Image path is ignored")
                        image_path = None

                if image_path:                
                        self._image_path = Path(image_path)
                        self._image = Image.open(self._image_path)

        @property
        def image(self):
                if self._image:
                        return self._image
                else:
                        return Image.open(self._image_path)

        @property
        def landmarks(self):
                return self._landmarks

        def __str__(self):
                return str(self._image_path)

        def __repr__(self):
                return os.path.basename(self._image_path)
        
        def crop(self, left=None, top=None, right=None, bottom=None):

                ...