import numpy as np
from util import build_t_mat, build_scale_mat, build_rot_mat


class PointCloudObject(object):
    """
        Representation of an 3D-Object as a cluster of points
        @param: filehandle  path to a file with point coordinates (each line
                            is one point) of the object
    """
    def __init__(self, filehandle):
        self.raw_coords = self.read_object_points(filehandle)
        self.normalized_points = self.normalize_points()
        self.smallest_radius

    def read_object_points(self, filehandle):
        with open(filehandle) as coordinates:
            obj_points = []
            for line in coordinates.readlines():
                line = line.strip()
                entry = [x for x in line.split()]
                entry.append(1)  # [x, y, z, 1] Homogenisierung
                obj_points.append(entry)
            obj_points = np.array(obj_points, dtype=np.float32)
        return obj_points

    def normalize_points(self):
        t_vec = self._calculate_obj_mid_v()
        t_mat = build_t_mat(-t_vec)  # trans matrix for moving the objects mid point into 0,0,0
        # getting list with the current max coordinates and translating this coords with the given vector
        # than getting the maximum value of one component: this is our most far point from 0,0,0
        largest_dist_after_t = max(self.raw_coords.max(axis=0)[:-1] - t_vec)
        self.smallest_radius = largest_dist_after_t
        # for fitting into [-1, 1] box we need the scale factor
        scale_fac = 1 / largest_dist_after_t
        s_mat = build_scale_mat([scale_fac, scale_fac, scale_fac])
        # multiplying the transformation matrices (translation, scaling) into one transformation
        norm_mat = np.matmul(s_mat, t_mat)
        normalized_points = []
        for point in self.raw_coords:  # normalizing each point
            pn = np.matmul(norm_mat, point)
            normalized_points.append(pn)
        return np.array(normalized_points)

    def _calculate_obj_mid_v(self):
        # lists with max (x,y,z) and min(x,y,z)
        maxima, minima = self.raw_coords.max(
            axis=0)[:-1], self.raw_coords.min(axis=0)[:-1]
        # the vector from min xyz to max xyz
        dist = maxima - minima
        # adding half of the objects diagonal vector to the min point
        # for relative mid of the object
        return minima + list(map(lambda x: x*0.5, dist))

    def rotate_object(self):
        rotated_points = []
        RM = build_rot_mat()
        for point in self.normalized_points:
            rp = np.matmul(RM, point)
            rotated_points.append(rp)
        self.normalized_points = np.array(rotated_points)
