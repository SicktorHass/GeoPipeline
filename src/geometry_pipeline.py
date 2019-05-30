import numpy as np
from util import build_t_mat
from math import tan


class PointRenderPipeline(object):
    def __init__(self, camera, viewport_geometry):
        self.camera = camera
        self.width = viewport_geometry[0]
        self.height = viewport_geometry[1]
        self.look_at_mat = self.look_at_transformation_mat()
        self.projection_mat = self.perspective_projection_mat()
        self.transformation_mat = self.combine_transformations()
        self.object_state = None

    def combine_transformations(self):
        return np.matmul(self.look_at_mat, self.projection_mat)

    def oc_transform_cc(self, point):
        build_mirror_mat('x')

    def transform_object_to_world(self):
        pass

    def grundriss_mat(self):
        M = np.eye(4)
        M[2][2] = 0
        return M

    def perspective_projection_mat(self):
        PPM = np.zeros((4, 4), dtype=np.float32)
        cot = 1 / tan(self.camera.fov)
        F, N = 2, 1
        PPM[0][0] = cot
        PPM[1][1] = cot
        PPM[2][2] = -(F+N) / (F-N)
        PPM[2][3] = -2*F*N / (F-N)
        PPM[3][2] = -1.
        return PPM

    def look_at_transformation_mat(self):
        """
            transforms object coordinates into camera coordinates
        """
        M_trans = build_t_mat(-self.camera.origin)
        M = np.eye(4)
        M[0][0], M[1][0], M[2][0] = self.camera.s[0], self.camera.s[1], self.camera.s[2]
        M[0][1], M[1][1], M[2][1] = self.camera.u[0], self.camera.u[1], self.camera.u[2]
        M[0][2], M[1][2], M[2][2] = self.camera.f[0], self.camera.f[1], self.camera.f[2]
        res = np.matmul(M.T, M_trans)
        return res

    def viewport_transformation(self, point):
        # make points positive by shifting the bounding-box into [0;2]
        viewpoint = list(map(lambda x: (x+1)*500, point[:-2]))
        # multiply points by aspect
        return viewpoint

    def pipe(self, point):
        """
            Send a point through the geometry pipeline
            @return: transformed 2d-point for screen displaying
        """
        p_transformed = np.matmul(self.transformation_mat, point)
        return self.viewport_transformation(p_transformed)
