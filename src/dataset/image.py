import os
from pathlib import Path
from dataclasses import dataclass
from typing import Union, List, Tuple
from copy import deepcopy
from PIL import Image, ImageDraw

def clip_x(xy_list : List[Tuple[float, float]], x_sub):
        return list(filter(lambda z : z[0] >= 0, [(x-x_sub, y) for x, y in xy_list]))

def clip_y(xy_list : List[Tuple[float, float]], y_sub):
        return list(filter(lambda z : z[1] >= 0, [(x, y-y_sub) for x, y in xy_list]))

def drop_x(xy_list : List[Tuple[float, float]], x_drop):
        return list(filter(lambda z : z[0] <= x_drop, [(x, y) for x, y in xy_list]))

def drop_y(xy_list : List[Tuple[float, float]], y_drop):
        return list(filter(lambda z : z[1] <= y_drop, [(x, y) for x, y in xy_list]))

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
                        left_brow = drop_y(drop_x(clip_y(clip_x(self._landmarks.left_brow, left), top), right), bottom),
                        right_brow = drop_y(drop_x(clip_y(clip_x(self._landmarks.right_brow, left), top), right), bottom),
                        left_eye = drop_y(drop_x(clip_y(clip_x(self._landmarks.left_eye, left), top), right), bottom),
                        right_eye = drop_y(drop_x(clip_y(clip_x(self._landmarks.right_eye, left), top), right), bottom),
                        nose = drop_y(drop_x(clip_y(clip_x(self._landmarks.nose, left), top), right), bottom),
                        lower_face = drop_y(drop_x(clip_y(clip_x(self._landmarks.lower_face, left), top), right), bottom),
                        outer_lips = drop_y(drop_x(clip_y(clip_x(self._landmarks.outer_lips, left), top), right), bottom),
                        inner_lips = drop_y(drop_x(clip_y(clip_x(self._landmarks.inner_lips, left), top), right), bottom),
                        left_eye_lash = drop_y(drop_x(clip_y(clip_x(self._landmarks.left_eye_lash, left), top), right), bottom),
                        left_eye_lid = drop_y(drop_x(clip_y(clip_x(self._landmarks.left_eye_lid, left), top), right), bottom),
                        right_eye_lash = drop_y(drop_x(clip_y(clip_x(self._landmarks.right_eye_lash, left), top), right), bottom),
                        right_eye_lid = drop_y(drop_x(clip_y(clip_x(self._landmarks.right_eye_lid, left), top), right), bottom),
                        face = drop_y(drop_x(clip_y(clip_x(self._landmarks.face, left), top), right), bottom),
                )

                return type(self)(landmarks=landmark, image=image)

        def draw_bbox(self, color='red', eye=False, nose=False, lips=False):

                image_draw = deepcopy(self._image)
                draw = ImageDraw.Draw(image_draw)

                if eye:
                        left_eye_x = [x[0] for x in self._landmarks.left_eye]
                        left_eye_lash_y = [y_lash[1] for y_lash in self._landmarks.left_eye_lash]
                        left_eye_lid_y = [y_lid[1] for y_lid in self._landmarks.left_eye_lid]

                        if all([len(left_eye_x)>0, len(left_eye_lash_y)>0, len(left_eye_lid_y)]):
                                left_eye_left_localized = min(left_eye_x)
                                left_eye_right_localized = max(left_eye_x)
                                left_eye_top_localized = min(left_eye_lash_y)
                                left_eye_bottom_localized = max(left_eye_lid_y)

                                draw.rectangle((left_eye_left_localized, left_eye_top_localized, left_eye_right_localized, left_eye_bottom_localized), outline=color)

                        right_eye_x = [z[0] for z in self._landmarks.right_eye]
                        right_eye_lash_y = [z[1] for z in self._landmarks.right_eye_lash]
                        right_eye_lid_y = [z[1] for z in self._landmarks.right_eye_lid]

                        if all([len(right_eye_x)>0, len(right_eye_lash_y)>0, len(right_eye_lid_y)]):

                                right_eye_left_localized = min(right_eye_x)
                                right_eye_right_localized = max(right_eye_x)
                                right_eye_top_localized = min(right_eye_lash_y)
                                right_eye_bottom_localized = max(right_eye_lid_y)

                                draw.rectangle((right_eye_left_localized, right_eye_top_localized, right_eye_right_localized, right_eye_bottom_localized), outline=color)


                return image_draw

if __name__ == "__main__":

        example = [(9, 9), (3, 4), (1, 2)]

        # print(clip_x(example, 9))

        print(clip_y(example, 6))