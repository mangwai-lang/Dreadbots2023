import json
import math

def getYawRotation(rotation_matrix):
    """
    Returns the yaw rotation (around the camera Y-axis) of a given combined rotation matrix
    Combined 3d rotation matrix:
        Y: Yaw Rotation (In Camera Space)
        X: Pitch Rotation
        Z: Roll Rotation
        [
            [cos(Y)cos(X), cos(Y)sin(X)sin(Z)-sin(Y)cos(Z), cos(Y)sin(X)cos(Z)+sin(Y)sin(Z)],
            [sin(Y)cos(x), sin(Y)sin(X)sin(Z)+cos(Y)cos(Z), sin(Y)sin(X)cos(Z)-cos(Y)sin(Z)],
            [-sin(X), cos(X)sin(Z), cos(X)cos(Z)]
        ]

    :param rotation_matrix: Rotation matrix
    :return: Rotation in radians
    :rtype: float
    """

    pitch = -1 * math.asin(rotation_matrix[2][0])
    return math.acos(rotation_matrix[0][0] / math.cos(pitch))


def getRotation(rotation_matrix):
    """
    Returns the individual rotations of a given combined rotation matrix
    Combined 3d rotation matrix:
        Y: Yaw Rotation (In Camera Space)
        X: Pitch Rotation
        Z: Roll Rotation
        [
            [cos(Y)cos(X), cos(Y)sin(X)sin(Z)-sin(Y)cos(Z), cos(Y)sin(X)cos(Z)+sin(Y)sin(Z)],
            [sin(Y)cos(x), sin(Y)sin(X)sin(Z)+cos(Y)cos(Z), sin(Y)sin(X)cos(Z)-cos(Y)sin(Z)],
            [-sin(X), cos(X)sin(Z), cos(X)cos(Z)]
        ]

    :param rotation_matrix: Rotation matrix
    :return: Rotations about all axis (Yaw, Pitch, Roll) in radians
    :rtype: tuple[float, float, float]
    """
    pitch = -1 * math.asin(rotation_matrix[2][0])

    cos_pitch = math.cos(pitch)
    yaw = math.acos(rotation_matrix[0][0] / cos_pitch)
    roll = math.acos(rotation_matrix[2][2] / cos_pitch)
    
    return (yaw, pitch, roll)


def getPosition(dist_tuple: tuple[float, float], rot: tuple[float, float, float], tag_id: int):
    """
    Returns the current position of the camera on the game field

    :param dist_tuple: The relative distance from the camera to the tag (X, Z)
    :param rot: The rotation of the april tag from its various axis in radians (Yaw, Pitch, Roll)
    :param tag_id: The ID of the detected tag
    :type dist_tuple: tuple[float, float]
    :type rot: tuple[float, float, float]
    :type tag_id: int
    :return: (X, Z)
    :rtype: tuple[float, float]
    """
    
    # Solves for both the X and Z displacement while solving for the Pitch and Roll rotations
    dist_z_solved = dist_tuple[1] / math.cos(rot[1])
    dist_x_solved = dist_tuple[0] / math.cos(rot[2])

    dist_hyp_rel = math.sqrt((dist_x_solved**2) + (dist_z_solved**2))
    dist_x_abs = dist_hyp_rel * math.cos(rot_yaw) * (-1 * (dist_tuple[0] / abs(dist_tuple[0])))
    # Opposite sign of the rel_x

    dist_z_abs = dist_hyp_rel * math.sin(rot_yaw)

    if tag_id <= 4 and tag_id >= 1:
        dist_x_abs *= -1
        dist_z_abs *= -1
    
    f = open('apriltag_positions.json')
    tag_coord_object = json.load(f)["points"][str(tag_id)]
    tag_coord = (int(tag_coord_object["x"]), int(tag_coord_object["z"]))
    return (tag_coord[0] + dist_x_abs, tag_coord[1] + dist_z_abs)

