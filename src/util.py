import numpy as np
from math import sin, cos, pi


def build_t_mat(t_vec):
    M = np.eye(4)
    M[0][3], M[1][3], M[2][3] = t_vec[0], t_vec[1], t_vec[2]
    return M


def build_rot_mat():
    M = np.eye(4)
    M[0][0], M[0][2] = cos(pi/8), sin(pi/8)
    M[2][0], M[2][2] = -sin(pi/8), cos(pi/8)
    return M


def build_scale_mat(scale_vec):
    M = np.eye(4)
    M[0, 0], M[1, 1], M[2, 2] = scale_vec[0], scale_vec[1], scale_vec[2]
    return M


def build_mirror_mat(axis):
    M = np.eye(4)
    if axis is 'x':
        M[0][0] = -1.
    elif axis is 'y':
        M[1][1] = -1.
    elif axis is 'z':
        M[2][2] = -1
    return M
