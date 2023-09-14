from PIL import ImageOps

from .image import FaceLandmarkImage, Landmark
from ..utils.converters import mirror_

class FaceLandmarkImageOps:
    
        @staticmethod
        def mirror(fl : FaceLandmarkImage):

                width, height = fl.image.size
                
                mirrored_image = ImageOps.mirror(fl.image)

                landmark = Landmark(
                        left_brow = mirror_(fl.landmarks.left_brow, width),
                        right_brow = mirror_(fl.landmarks.right_brow, width),
                        left_eye = mirror_(fl.landmarks.left_eye, width),
                        right_eye = mirror_(fl.landmarks.right_eye, width),
                        nose = mirror_(fl.landmarks.nose, width),
                        lower_face = mirror_(fl.landmarks.lower_face, width),
                        outer_lips = mirror_(fl.landmarks.outer_lips, width),
                        inner_lips = mirror_(fl.landmarks.inner_lips, width),
                        left_eye_lash = mirror_(fl.landmarks.left_eye_lash, width),
                        left_eye_lid = mirror_(fl.landmarks.left_eye_lid, width),
                        right_eye_lash = mirror_(fl.landmarks.right_eye_lash, width),
                        right_eye_lid = mirror_(fl.landmarks.right_eye_lid, width),
                        face = mirror_(fl.landmarks.face, width),
                )

                return FaceLandmarkImage(landmarks=landmark, image=mirrored_image)
