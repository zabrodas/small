import bpy
import bmesh
import mathutils
from math import *
from mathutils import *

bl_info = {
    "name": "Find center of circumscribed circle",
    "description": "Find center of circumscribed circle",
    "author": "Andrey Zabrodin",
    "version": (1, 1),
    "blender": (2, 78, 0),
    "warning": "",
    "location": "Tool Shelf > Mesh",
    "category": "Mesh"
#    "location": "Tool Shelf > Create Gear",
#    "category": "Object"
}


def dist2(x,y) :
    s=0
    for i in range(len(x)): s+=(x[i]-y[i])*(x[i]-y[i])
    return s

def dist(x,y): return sqrt(dist2(x,y))

def norm2(x) :
    s=0
    for i in range(len(x)): s+=x[i]*x[i]
    return s

def norm(x): return sqrt(norm2(x))

def midpoint(xl):
    n=len(xl)
    dim=len(xl[0])
    m=[0 for i in range(dim)]
    for j in range(dim):
        s=0;
        for x in xl: s+=x[j]
        m[j]=s/n
    return m

def direct(f,t):
    return [t[i]-f[i] for i in range(len(f))]

def vadd(f,t):
    return [t[i]+f[i] for i in range(len(f))]

def vmul(f,m):
    return [f[i]*m for i in range(len(f))]
            
def findCenter(xl): 
    n=len(xl)
    dim=len(xl[0])

    xc=midpoint(xl)
    itercnt=10000
    while True:

        s=0
        for x in xl: s+=dist(xc,x)
        middist=s/n

        #print xc+[middist]

        step=[0 for i in range(dim)]
        for x in xl:
            v=direct(xc,x)    
            d=norm(v)
            dd=d-middist
            vv=vmul(v,dd/d/n)
            step=vadd(step,vv)

        ds=norm(step)
#        print (middist,ds)
        itercnt-=1
        if ds<0.0001/n: return xc
        if itercnt<0: raise Exception("Too many interations")

        xc=vadd(xc,step)

class FindCenterPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Tools'
    bl_label = "Find center"
    bl_context = "mesh_edit"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.operator(FindCenter.bl_idname, text="Find center")


class FindCenter(bpy.types.Operator):
    bl_description="Find center of circumscribed circle"
    bl_idname="mesh.findcenter"
    bl_label="az.FindCenter"

    @classmethod
    def poll(cls, context):
       ob = context.active_object
       return(ob and ob.type == 'MESH' and context.mode == 'EDIT_MESH')

    def invoke(self, context, event):
        bm = bmesh.from_edit_mesh(context.active_object.data)
        vl=[ [v.co.x,v.co.y,v.co.z] for v in bm.verts if v.select ]
        if len(vl) <= 1:
            raise Exception("Select at least 2 points")
            return
#        print(vl)
        vc=findCenter(vl)
        mw=context.active_object.matrix_world
        vcw=mw*Vector(vc)
        context.scene.cursor_location=vcw
#        print(vc)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(FindCenter)
    bpy.utils.register_class(FindCenterPanel)
                                                                                        
def unregister():
    bpy.utils.unregister_class(FindCenter)
    bpy.utils.unregister_class(FindCenterPanel)
    
if __name__ == "__main__":
    register()




