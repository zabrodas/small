import bpy
import bmesh
import mathutils
import math
from math import *
from mathutils import *

bl_info = {
    "name": "Formula deformation",
    "description": "Create a deformated copy of object",
    "author": "Andrey Zabrodin",
    "version": (1, 1),
    "blender": (2, 78, 0),
    "warning": "",
    "location": "View3D > Add > Mesh",
    "category": "Add Mesh"
#    "location": "Tool Shelf > Create Gear",
#    "category": "Object"
}

class FormulaDeformationPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Tools'
    bl_label = "Formula deformation"
    bl_context = "objectmode"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.operator(createMeshOperator.bl_idname, text="Create deformated copy")
        layout.prop(context.scene, "formula_deformation_a")
        layout.prop(context.scene, "formula_deformation_b")
        layout.prop(context.scene, "formula_deformation_c")
        layout.prop(context.scene, "formula_deformation_d")
        layout.prop(context.scene, "formula_deformation_p")
        layout.prop(context.scene, "formula_deformation_q")
        layout.prop(context.scene, "formula_deformation_r")
        layout.prop(context.scene, "formula_deformation_s")
        layout.prop(context.scene, "formula_deformation_x")
        layout.prop(context.scene, "formula_deformation_y")
        layout.prop(context.scene, "formula_deformation_z")
        xx=selectObjects(context)
        if len(xx)==2 :layout.label(text="%s->%s" % (xx[0].name,xx[1].name))

def meEval(s,gbl,lcl) :
    try :
        return eval(s,gbl,lcl)
    except :
        return 0


def createMesh(context,src,a,b,c,d,p,q,r,s,x,y,z) :

        scene = context.scene
        newMesh=bpy.data.meshes.new_from_object(scene, src, True, 'PREVIEW', calc_tessface=True, calc_undeformed=False)

        gbl={'__builtins__':{}}
        lcl={'a':a,'b':b,'c':c,'d':d}
        fl=['ceil','fabs','factorial','floor','fmod','trunc','exp','expm1','log','log1p','log10','pow','sqrt','acos','atan','atan2','cos','hypot','sin','tan','degrees','radians','pi']
        for f in fl: lcl[f]=math.__dict__[f]

        vl=newMesh.vertices
        for v in vl :
            lcl['x']=v.co.x
            lcl['y']=v.co.y
            lcl['z']=v.co.z

            lcl['p']=0
            lcl['q']=0
            lcl['r']=0
            lcl['s']=0

            lcl['p']=meEval(p,gbl,lcl)
            lcl['q']=meEval(q,gbl,lcl)
            lcl['r']=meEval(r,gbl,lcl)
            lcl['s']=meEval(s,gbl,lcl)
            v.co.x = meEval(x,gbl,lcl)
            v.co.y = meEval(y,gbl,lcl)
            v.co.z = meEval(z,gbl,lcl)

        newMesh.update()
        return newMesh

def selectObjects(context) :
        if context.active_object is None : return []
        if len(context.selected_objects) in [1,2] and context.selected_objects[0].name != context.active_object.name : return [ context.selected_objects[0],context.active_object ]
        if len(context.selected_objects)==2 and context.selected_objects[1].name != context.active_object.name : return [ context.selected_objects[1],context.active_object ]
        return []


class createMeshOperator(bpy.types.Operator):
    bl_idname = "mesh.formula_deformation"
    bl_label = "formula_deformation"
    bl_register = True
    bl_undo = True

#    def draw(self, context):
#        layout = self.layout
#        col = layout.column()
#        col.prop(self, 'formula_deformation_x')
#        col.prop(self, 'formula_deformation_y')
#       col.prop(self, 'formula_deformation_z')
#        return {'FINISHED'}

    
    @classmethod
    def poll(cls, context):
        return context.object.mode == 'OBJECT' and len(selectObjects(context))==2

#    def invoke():
#        return {'FINISHED'}

    def execute(self, context):

        scene = context.scene
        obj = context.active_object

        a=scene.formula_deformation_a
        b=scene.formula_deformation_b
        c=scene.formula_deformation_c
        d=scene.formula_deformation_d
        p=scene.formula_deformation_p
        q=scene.formula_deformation_q
        r=scene.formula_deformation_r
        s=scene.formula_deformation_s
        x=scene.formula_deformation_x
        y=scene.formula_deformation_y
        z=scene.formula_deformation_z

        twoObjects=selectObjects(context)
        sourceObj=twoObjects[0]
        targetObj=twoObjects[1]

        # Clear target object
        oldMesh = targetObj.data
        targetObj.data = None
#        oldMesh.user_clear()
#        if (oldMesh.users == 0): bpy.data.meshes.remove(oldMesh)
        
        # setup target objetc with new mesh
        mesh=createMesh(context,sourceObj,a,b,c,d,p,q,r,s,x,y,z)
        targetObj.data = mesh
        mesh.update()
        scene.update()

        return {'FINISHED'}


def add_mesh_distorted_copy(self, context):
    self.layout.operator(createMeshOperator.bl_idname, text="Distorted copy", icon="PLUGIN")

def register():
    bpy.types.Scene.formula_deformation_a = bpy.props.FloatProperty(name="a",description="a",default=0)         
    bpy.types.Scene.formula_deformation_b = bpy.props.FloatProperty(name="b",description="b",default=0)         
    bpy.types.Scene.formula_deformation_c = bpy.props.FloatProperty(name="c",description="c",default=0)         
    bpy.types.Scene.formula_deformation_d = bpy.props.FloatProperty(name="d",description="d",default=0)         

    bpy.types.Scene.formula_deformation_p = bpy.props.StringProperty(name="p=",description="p=",default="x+y")  
    bpy.types.Scene.formula_deformation_q = bpy.props.StringProperty(name="q=",description="q=",default="x-y")  
    bpy.types.Scene.formula_deformation_r = bpy.props.StringProperty(name="r=",description="r=",default="x*y")  
    bpy.types.Scene.formula_deformation_s = bpy.props.StringProperty(name="s=",description="s=",default="x/y")  
                                                                             
    bpy.types.Scene.formula_deformation_x = bpy.props.StringProperty(name="x=",description="x=",default="y+1")  
    bpy.types.Scene.formula_deformation_y = bpy.props.StringProperty(name="y=",description="y=",default="y+1")  
    bpy.types.Scene.formula_deformation_z = bpy.props.StringProperty(name="z=",description="z=",default="z+1")  
    bpy.utils.register_class(FormulaDeformationPanel)
    bpy.utils.register_class(createMeshOperator)
#    bpy.types.INFO_MT_mesh_add.append(add_mesh_distorted_copy)

                                                                                        
def unregister():
    bpy.utils.unregister_class(FormulaDeformationPanel)
    bpy.utils.unregister_class(createMeshOperator)
#    bpy.types.INFO_MT_mesh_add.remove(add_mesh_distorted_copy)
    del bpy.types.Scene.formula_deformation_a
    del bpy.types.Scene.formula_deformation_b
    del bpy.types.Scene.formula_deformation_c
    del bpy.types.Scene.formula_deformation_d
    del bpy.types.Scene.formula_deformation_p
    del bpy.types.Scene.formula_deformation_q
    del bpy.types.Scene.formula_deformation_r
    del bpy.types.Scene.formula_deformation_s
    del bpy.types.Scene.formula_deformation_x
    del bpy.types.Scene.formula_deformation_y
    del bpy.types.Scene.formula_deformation_z
    
if __name__ == "__main__":
    register()




