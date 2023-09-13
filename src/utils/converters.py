from typing import Union, List, Tuple


def landmarks2bbox(landmarks):
        bbox_box = {
                'left_eye' : (),
                'right_eye' : (),
                'nose' : (),
                'mouth' : (),
                }

        # LEFT EYE
        left_eye_x = [x[0] for x in landmarks.left_eye]
        left_eye_lash_y = [y_lash[1] for y_lash in landmarks.left_eye_lash]
        left_eye_lid_y = [y_lid[1] for y_lid in landmarks.left_eye_lid]

        if all([len(left_eye_x)>0, len(left_eye_lash_y)>0, len(left_eye_lid_y)]):
                bbox_box['left_eye'] = (min(left_eye_x), min(left_eye_lash_y), max(left_eye_x), max(left_eye_lid_y))

        # RIGHT EYE
        right_eye_x = [x[0] for x in landmarks.right_eye]
        right_eye_lash_y = [y_lash[1] for y_lash in landmarks.right_eye_lash]
        right_eye_lid_y = [y_lid[1] for y_lid in landmarks.right_eye_lid]

        if all([len(right_eye_x)>0, len(right_eye_lash_y)>0, len(right_eye_lid_y)]):
                bbox_box['right_eye'] = (min(right_eye_x), min(right_eye_lash_y), max(right_eye_x), max(right_eye_lid_y))

        return bbox_box


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
