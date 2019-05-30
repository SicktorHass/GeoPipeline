import numpy as np
from numpy import linalg as la


class Camera(object):
    def __init__(self, location, center, up):
        assert(isinstance(location, list))
        assert(isinstance(center, list))
        assert(isinstance(up, list))
        location.append(1)
        center.append(1)
        up.append(0)
        self.fov = np.pi / 3
        self.origin = np.array(location, dtype=np.float64)
        self.center = np.array(center, dtype=np.float64)
        self.up = np.array(up, dtype=np.float64)
        oc = np.subtract(self.center, self.origin)
        self.up = self.up / la.norm(self.up)
        # z-dir
        self.f = oc / la.norm(oc)
        self.f = self.f[:-1]
        # x- dir
        self.s = np.cross(self.f, self.up[:-1])
        # y - dir
        self.u = np.cross(self.s, self.f)
        print('CAMERA s, u, f : ', self.s, self.u, self.f)
