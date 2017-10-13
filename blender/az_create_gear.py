import bpy
import bmesh
import mathutils
import math
from math import *
from mathutils import *

bl_info = {
    "name": "Create gear",
    "description": "Create a gear with parameters",
    "author": "Andrey Zabrodin",
    "version": (1, 1),
    "blender": (2, 78, 0),
    "location": "Tool Shelf > Create Gear",
    "warning": "",
    "category": "Object"
}

class MyPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Create'
    bl_label = "Create gear"
    bl_context = "objectmode"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.operator(CreateGearOperator.bl_idname, text="Create gear")
        layout.prop(context.scene, "az_create_gear_operator_n")
        layout.prop(context.scene, "az_create_gear_operator_h")
        layout.prop(context.scene, "az_create_gear_operator_w")

def createGear(n,h,w) :
        a1=math.radians(360)/n
        l2=h*tan(math.radians(30))
        r1=l2/sin(a1/2)
        r2=r1+h

        pa=Vector((r2-h/15,0,0))
        pa1=Vector((r2-h/10,h/20,0))
        pa2=Vector((r2-h/10,-h/20,0))
        pb=Vector((r1*cos(a1/2),r1*sin(a1/2),0))
        pc=Vector((r1*cos(a1/2),-r1*sin(a1/2),0))
        pw=Vector((0,0,w))

        vl=[]
        fl=[]
        fcu=[]
        fcb=[]
        for i in range(0,n):
            a=a1*i
            m=Matrix.Rotation(a,3,"Z")
            vi=len(vl)
            vl1=[m*pa2,m*pa,m*pa1,m*pb, m*pa2+pw,m*pa+pw,m*pa1+pw,m*pb+pw]
            fl1=[ [0,1,5,4],[1,2,6,5], [2,3,7,6],[3,8,12,7] ]
            for j in range(0,len(fl1)) :
                fl1[j][0]+=vi
                fl1[j][1]+=vi
                fl1[j][2]+=vi
                fl1[j][3]+=vi
            vl+=vl1
            fl+=fl1
            fcu+=[ 0+vi,1+vi,2+vi,3+vi ]
            fcb+=[ 4+vi,5+vi,6+vi,7+vi ]

        for j in range(0,len(fl)) :
            fl[j][0]%=len(vl)
            fl[j][1]%=len(vl)
            fl[j][2]%=len(vl)
            fl[j][3]%=len(vl)

        for j in range(0,len(fcu)) : fcu[j]%=len(vl)
        for j in range(0,len(fcb)) : fcb[j]%=len(vl)

#        print ("Create gear",vl1,el1,fl1)
        mesh = bpy.data.meshes.new("gear")
        mesh.from_pydata(vl, [], fl+[fcu]+[fcb])
        mesh.update()

        return mesh

class CreateGearOperator(bpy.types.Operator):
    bl_idname = "az.create_gear_operator"
    bl_label = "Create gear"
    bl_register = True
    bl_undo = True
    
    @classmethod
    def poll(cls, context):
        return context.object.mode == 'OBJECT'

    def execute(self, context):
        scene = context.scene
        n=scene.az_create_gear_operator_n
        h=scene.az_create_gear_operator_h
        w=scene.az_create_gear_operator_w
        mesh=createGear(n,h,w)

        ob_new = bpy.data.objects.new("gear", mesh)
        scene.objects.link(ob_new)
        ob_new.select = True
        return {'FINISHED'}

def register():
    bpy.utils.register_module(__name__)
    bpy.types.Scene.az_create_gear_operator_n = bpy.props.IntProperty(name="Nt",description="Количество зубьев",default=15)
    bpy.types.Scene.az_create_gear_operator_h = bpy.props.IntProperty(name="Ht",description="Высота зубьев",default=5)
    bpy.types.Scene.az_create_gear_operator_w = bpy.props.IntProperty(name="W",description="Толщина шестерни",default=6)

def unregister():
    bpy.utils.register_module(__name__)
    del bpy.types.Scene.az_create_gear_operator_n
    del bpy.types.Scene.az_create_gear_operator_h
    del bpy.types.Scene.az_create_gear_operator_w
    
if __name__ == "__main__":
    register()