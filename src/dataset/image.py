import os
import numpy as np
from pathlib import Path
from dataclasses import dataclass
from typing import Union, List, Tuple
from copy import deepcopy
from PIL import Image, ImageDraw

from ..utils.enumerates import FacePart

def clip_x(xy_list : List[Tuple[float, float]], x_sub):
        return list(filter(lambda z : z[0] >= 0, [(x-x_sub, y) for x, y in xy_list]))

def clip_y(xy_list : List[Tuple[float, float]], y_sub):
        return list(filter(lambda z : z[1] >= 0, [(x, y-y_sub) for x, y in xy_list]))

def drop_x(xy_list : List[Tuple[float, float]], x_drop):
        return list(filter(lambda z : z[0] <= x_drop, [(x, y) for x, y in xy_list]))

def drop_y(xy_list : List[Tuple[float, float]], y_drop):
        return list(filter(lambda z : z[1] <= y_drop, [(x, y) for x, y in xy_list]))

def scale(xy_list : List[Tuple[float, float]], sf):
        return list(map(lambda z : (z[0]*sf, z[1]*sf), xy_list))

def clip_drop_arr(arr: np.ndarray, px_crop : tuple):
        arr_to_list = arr.tolist()
        clipped = drop_y(drop_x(clip_y(clip_x(arr_to_list, px_crop[0]), px_crop[1]), px_crop[2]), px_crop[3])
        return np.array(clipped)

@dataclass
class Landmark:
        points : np.ndarray
        indices : dict

        def get_cluster(self, facepart : FacePart):
                facepart = FacePart(facepart)
                return self.points[np.array(self.indices[facepart.value])]


class FaceLandmarkImage:

        def __init__(self, landmarks : Landmark, image = None, image_path : Union[Path, str] = None):
                self._landmarks = landmarks

                if image:
                        self._image = image
                        print("Image path is ignored")
                        image_path = None

                if image_path:                
                        self._image_path = Path(image_path)
                        self._image = Image.open(self._image_path)

        @property
        def image(self):
                return self._image

        @property
        def landmarks(self):
                return self._landmarks

        @property
        def width(self):
                return self._image.width

        @property
        def height(self):
                return self._image.height
        
        def show(self):
                return self._image.show()

        def __str__(self):
                return str(self._image_path)

        def __repr__(self):
                return os.path.basename(self._image_path)
        
        def crop(self, left=None, top=None, right=None, bottom=None):
                
                # Set to 0 if no argument provided
                left = int(left or 0)
                top = int(top or 0)
                right = int(right or self._image.width)
                bottom = int(bottom or self._image.height)

                image = self._image.crop((left, top, right, bottom))

                landmark = Landmark(
                        points= clip_drop_arr(self._landmarks.points, (left, top, right, bottom)),
                        indices= self._landmarks.indices
                )

                return type(self)(landmarks=landmark, image=image)

        def uniform_scale(self, scaling_factor: float):

                width, height = self._image.size
                new_width = width * scaling_factor
                new_height = height * scaling_factor

                image = self._image.resize((int(new_width), int(new_height)))

                landmark = Landmark(
                        left_brow=scale(self._landmarks.left_brow, scaling_factor),
                        right_brow=scale(self._landmarks.right_brow, scaling_factor),
                        left_eye = scale(self._landmarks.left_eye, scaling_factor),
                        right_eye = scale(self._landmarks.right_eye, scaling_factor),
                        nose = scale(self._landmarks.nose, scaling_factor),
                        lower_face = scale(self._landmarks.lower_face, scaling_factor),
                        outer_lips = scale(self._landmarks.outer_lips, scaling_factor),
                        inner_lips = scale(self._landmarks.inner_lips, scaling_factor),
                        left_eye_lash = scale(self._landmarks.left_eye_lash, scaling_factor),
                        left_eye_lid = scale(self._landmarks.left_eye_lid, scaling_factor),
                        right_eye_lash = scale(self._landmarks.right_eye_lash, scaling_factor),
                        right_eye_lid = scale(self._landmarks.right_eye_lid, scaling_factor),
                        face = scale(self._landmarks.face, scaling_factor),
                )

                return type(self)(landmarks=landmark, image=image)

        def draw_bbox(self, color='red', eye=False, nose=False, lips=False):

                image_draw = deepcopy(self._image)
                draw = ImageDraw.Draw(image_draw)

                if eye:
                        try:
                                left_eye_x = self._landmarks.get_cluster('left_eye')[:,0].tolist()
                                left_eye_lash_y = self._landmarks.get_cluster('left_eye_lash')[:,1].tolist()
                                left_eye_lid_y = self._landmarks.get_cluster('left_eye_lid')[:,1].tolist()

                                if all([len(left_eye_x)>0, len(left_eye_lash_y)>0, len(left_eye_lid_y)]):
                                        left_eye_left_localized = min(left_eye_x)
                                        left_eye_right_localized = max(left_eye_x)
                                        left_eye_top_localized = min(left_eye_lash_y)
                                        left_eye_bottom_localized = max(left_eye_lid_y)

                                        draw.rectangle((left_eye_left_localized, left_eye_top_localized, left_eye_right_localized, left_eye_bottom_localized), outline=color)
                        except:
                                print("Can't draw left eye bounding box")

                        try:
                                right_eye_x = self._landmarks.get_cluster('right_eye')[:,0].tolist()
                                right_eye_lash_y = self._landmarks.get_cluster('right_eye_lash')[:,1].tolist()
                                right_eye_lid_y = self._landmarks.get_cluster('right_eye_lid')[:,1].tolist()
                                
                                if all([len(right_eye_x)>0, len(right_eye_lash_y)>0, len(right_eye_lid_y)]):

                                        right_eye_left_localized = min(right_eye_x)
                                        right_eye_right_localized = max(right_eye_x)
                                        right_eye_top_localized = min(right_eye_lash_y)
                                        right_eye_bottom_localized = max(right_eye_lid_y)

                                        draw.rectangle((right_eye_left_localized, right_eye_top_localized, right_eye_right_localized, right_eye_bottom_localized), outline=color)
                        except:
                                print("Can't draw right eye bounding box")

                return image_draw

if __name__ == "__main__":

        example = [(9, 9), (3, 4), (1, 2)]

        # print(clip_x(example, 9))

        print(clip_y(example, 6))