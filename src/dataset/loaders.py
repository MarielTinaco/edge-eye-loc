import os
import numpy as np

from abc import ABC, abstractmethod
from pathlib import Path
from typing import Union

from .image import FaceLandmarkImage, Landmark

class FaceLandmarkDataset(ABC):

        def __init__(self, src : Union[Path, str]):
                self._src = Path(src)

                if not self._src:
                        raise IOError("Dataset Path not found")

                if not self.test_path:
                        raise IOError("Test path doesn't exist")
                
                if not self.train_path:
                        raise IOError("Train path doesn't exist")

        @abstractmethod
        def generate_img(self, src_path):
                raise NotImplementedError

class LFPWDataset(FaceLandmarkDataset):

        @property
        def landmark_indices(self) -> dict:
                # NOTE: LFPW Landmarks annotations start with 1, so it has been adjusted
                return {
                        "left_brow":      list(range(17, 22)),
                        "right_brow":     list(range(22, 27)),                    
                        "left_eye":       list(range(36, 42)),
                        "right_eye":      list(range(42, 48)),
                        "nose":           list(range(27, 35)),
                        "lower_face":     list(range(0, 17)),
                        "outer_lips":     [48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59],
                        "inner_lips":     [60, 61, 62, 63, 64, 65, 66, 67],
                        "left_eye_lash":  [36, 37, 38, 39],
                        "left_eye_lid":   [36, 41, 40, 39],
                        "right_eye_lash": [42, 43, 44, 45],
                        "right_eye_lid":  [42, 47, 46, 45],
                        "face":           list(range(0, 27)),
                }
        @property
        def test_path(self) -> Path:
                return self._src / 'testset'
        
        @property
        def train_path(self) -> Path:
                return self._src / 'trainset'

        def generate_img(self, src_path):
                src_iter = iter(sorted(os.listdir(src_path)))
                for data in src_iter:
                        img = data
                        pts = next(src_iter)

                        img_path = src_path / img
                        pts_path = src_path / pts

                        full_pts = np.loadtxt(pts_path, comments=("version:", "n_points:", "{", "}")).tolist()
                        lm = Landmark(**{k : [tuple(full_pts[idx]) for idx in v] for k, v in self.landmark_indices.items()})

                        yield FaceLandmarkImage(image_path=img_path, landmarks=lm)

class HelenDataset(FaceLandmarkDataset):

        @property
        def landmark_indices(self) -> dict:
                return {
                        "left_brow" :      list(range(174, 193)),
                        "right_brow" :     list(range(154, 173)),
                        "left_eye" :       list(range(134, 153)),
                        "right_eye" :      list(range(114, 133)),
                        "nose" :           list(range(41, 57)),
                        "lower_face" :     list(range(0, 39)),
                        "outer_lips" :     list(range(58, 85)),
                        "inner_lips" :     list(range(86, 113)),
                        "left_eye_lash" :  [144, 143, 142, 141, 140, 139, 138, 137, 136, 135, 134],
                        "left_eye_lid" :   [145, 146, 147, 148, 149, 150, 151, 152, 153],
                        "right_eye_lash" : [114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124],
                        "right_eye_lid" :  [133, 132, 131, 130, 129, 128, 127, 126, 125, 125],
                        "face" :           list(range(0, 184)),
                }

        @property
        def test_path(self) -> Path:
                return self._src / 'test'

        @property
        def train_path(self) -> Path:
                return self._src / 'train'

        def generate_img(self, src_path):

                annotation_path = self._src / "annotation" / "annotation"

                for txt_file in os.listdir(annotation_path):
                        with open(annotation_path / txt_file, 'r') as annotation_txt:
                                lines = annotation_txt.readlines()

                                img_name = lines.pop(0).strip('\n')

                                points_list = []
                                for coord in lines:
                                        x, y = tuple(coord.rstrip('\n').split(','))
                                        points_list.append((float(x), float(y)))
                        
                        lm = Landmark(**{k : [points_list[idx] for idx in v] for k, v in self.landmark_indices.items()})

                        yield FaceLandmarkImage(image_path= src_path / f"{img_name}.jpg", landmarks=lm)

class FaceLandmarkDataloaderContext:

        def __init__(self, dloader : FaceLandmarkDataset = None):
                self._dloader = dloader

        @property
        def dloader(self):
                return self._dloader

        @dloader.setter
        def dloader(self, value):
                self._dloader = value

        def check_valid(self):
                return self._dloader.test_path.exists() and self._dloader.train_path.exists()

        def load(self, tset: str = 'train'):

                if tset == "test":
                        src_path = self.dloader.test_path
                else:
                        src_path = self.dloader.train_path

                for src in self._dloader.generate_img(src_path):
                        yield src

if __name__ == "__main__":

        from ..utils.paths_manager import LFPW_RAW_SOURCE_PATH, HELEN_RAW_SOURCE_PATH

        dloader_ctx = FaceLandmarkDataloaderContext(LFPWDataset(LFPW_RAW_SOURCE_PATH))
        print(dloader_ctx.check_valid())
        # dloader_ctx.dloader = HelenDataset(HELEN_RAW_SOURCE_PATH)
        # print(dloader_ctx.check_valid())

        for i in dloader_ctx.load("train"):
                print(i)