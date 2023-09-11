

from abc import ABC, abstractmethod
from dataclasses import dataclass
from collections import namedtuple
from pathlib import Path
from typing import Union

LandmarkIndex = namedtuple('LandmarkIndex', 
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
        @property
        def landmarks(self) -> namedtuple:
                return NotImplementedError

        @abstractmethod
        @property
        def test_path(self) -> Path:
                return NotImplementedError
        
        @abstractmethod
        @property
        def train_path(self) -> Path:
                return NotImplementedError

class LFPWDataset(FaceLandmarkDataset):

        @property
        def landmarks(self) -> LandmarkIndex:
                return LandmarkIndex (
                        left_brow=      list(range(17, 22)),
                        right_brow=     list(range(22, 27)),                    
                        left_eye=       list(range(36, 42)),
                        right_eye=      list(range(42, 48)),
                        nose=           list(range(27, 35)),
                        lower_face=     list(range(0, 17)),
                        outer_lips=     [49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60],
                        inner_lips=     [61, 62, 63, 64, 65, 66, 67, 68],
                        left_eye_lash=  [36, 37, 38, 39],
                        left_eye_lid=   [36, 41, 40, 39],
                        right_eye_lash= [42, 43, 44, 45],
                        right_eye_lid=  [42, 47, 46, 45],
                        face=           list(range(0, 27)),
                )

        @property
        def test_path(self) -> Path:
                return self._src / 'testset'
        
        @property
        def train_path(self) -> Path:
                return self._src / 'trainset'

class HelenDataset(FaceLandmarkDataset):

        @property
        def landmarks(self) -> LandmarkIndex:
                return LandmarkIndex(
                        left_brow=      list(range(174, 193)),
                        right_brow=     list(range(154, 173)),
                        left_eye=       list(range(134, 153)),
                        right_eye=      list(range(114, 133)),
                        nose=           list(range(41, 57)),
                        lower_face=     list(range(0, 39)),
                        outer_lips=     list(range(58, 85)),
                        inner_lips=     list(range(86, 113)),
                        left_eye_lash=  [144, 143, 142, 141, 140, 139, 138, 137, 136, 135, 134],
                        left_eye_lid=   [145, 146, 147, 148, 149, 150, 151, 152, 153],
                        right_eye_lash= [114, 115, 116, 117, 118, 119, 120, 121, 122, 123, 124],
                        right_eye_lid=  [133, 132, 131, 130, 129, 128, 127, 126, 125, 125],
                        face=           list(range(0, 184)),
                )

        @property
        def test_path(self) -> Path:
                return self._src / 'test'

        @property
        def train_path(self) -> Path:
                return self._src / 'train'

if __name__ == "__main__":

        ...