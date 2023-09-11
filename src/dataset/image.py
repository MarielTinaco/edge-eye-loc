import os
from pathlib import Path
from collections import namedtuple
from typing import Union
from PIL import Image

Landmark = namedtuple('Landmark', 
                [    'left_brow', 
                        'right_brow',
                        'left_eye',
                        'right_eye',
                        'nose',
                        'lower_face',
                        'outer_lips',
                        'inner_lips',
                        'left_eye_lash',
                        'left_eye_lid',
                        'right_eye_lash',
                        'right_eye_lid', 
                        'face',]
                )


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