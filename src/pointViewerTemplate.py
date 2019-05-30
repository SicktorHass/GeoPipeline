from camera import Camera
from geometry_pipeline import PointRenderPipeline
from point_cloud import PointCloudObject
import sys
from tkinter import *

WIDTH = 1000  # width of canvas
HEIGHT = 1000  # height of canvas

HPSIZE = 1  # double of point size (must be integer)
COLOR = "#0000FF"  # blue

OBJ_POINTS = []

pointList = []  # list of points (used by Canvas.delete(...))


def quit(root=None):
    """ quit programm """
    if root is None:
        sys.exit(0)
    root._root().quit()
    root._root().destroy()


def draw():
    """ draw points """
    for point in OBJECT3D.normalized_points:
        viewpoint = PRP.pipe(point)
        OBJ_POINTS.append(viewpoint)
    for i in range(1, len(OBJ_POINTS)):
        x, y = OBJ_POINTS[i][0], HEIGHT-OBJ_POINTS[i][1]
        p = can.create_oval(x-HPSIZE, y-HPSIZE, x+HPSIZE, y+HPSIZE,
                            fill=COLOR, outline=COLOR)
        pointList.insert(0, p)


def rotYp():
    """ rotate counterclockwise around y axis """
    OBJ_POINTS.clear()
    OBJECT3D.rotate_object()
    can.delete(*pointList)
    draw()


def rotYn():
    """ rotate clockwise around y axis """
    OBJ_POINTS.clear()
    OBJECT3D.rotate_object()
    can.delete(*pointList)
    draw()


if __name__ == "__main__":
    # check parameters
    if len(sys.argv) != 2:
        sys.exit(-1)
    OBJECT3D = PointCloudObject(sys.argv[1])
    DISTANCE = 2*OBJECT3D.smallest_radius
    DISTANCE = 0.001
    # cam params
    loc = [0, 0, DISTANCE]
    c = [0, 0, 0]
    up = [0, 1, 0]

    CAMERA = Camera(loc, c, up)
    PRP = PointRenderPipeline(camera=CAMERA, viewport_geometry=(WIDTH, HEIGHT))
    print(PRP.perspective_projection_mat())
    # create main window
    mw = Tk()

    # create and position canvas and buttons
    cFr = Frame(mw, width=WIDTH, height=HEIGHT, relief="sunken", bd=1)
    cFr.pack(side="top")
    can = Canvas(cFr, width=WIDTH, height=HEIGHT)
    can.pack()
    bFr = Frame(mw)
    bFr.pack(side="left")
    bRotYn = Button(bFr, text="<-", command=rotYn)
    bRotYn.pack(side="left")
    bRotYp = Button(bFr, text="->", command=rotYp)
    bRotYp.pack(side="left")
    eFr = Frame(mw)
    eFr.pack(side="right")
    bExit = Button(eFr, text="Quit", command=(lambda root=mw: quit(root)))
    bExit.pack()

    # draw points
    draw()

    # start
    mw.mainloop()
