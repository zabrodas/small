import bpy
import bmesh
import mathutils
from math import *
from mathutils import *

bl_info = {
    "name": "Fix face self intersection",
    "description": "Fix face self intersection after inset",
    "author": "Andrey Zabrodin",
    "version": (1, 1),
    "blender": (2, 79, 0),
    "warning": "",
    "location": "Tool Shelf > Mesh",
    "category": "Mesh"
#    "location": "Tool Shelf > Create Gear",
#    "category": "Object"
}

class FixSelfIntersectionPanel(bpy.types.Panel):
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = 'Tools'
    bl_label = "Fix self intersection"
    bl_context = "mesh_edit"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.operator(FixSelfIntersection.bl_idname, text="Fix self intersection")


def crange(s,e,n):
    r=[]
    while s>=n: s-=n
    while s<0: s+=n
    while e>=n: e-=n
    while e<0: e+=n
    while True:
        r.append(s)
        if s==e: break
        s+=1
        while s>=n: s-=n
    return r

def projectToPlane(v,n):
    return v-n*(v.dot(n))

def makePlaneBasis(o,p,n):
    v=p-o
    e1=projectToPlane(v,n).normalized()
    e2=e1.cross(n).normalized()
    print(e1,e2)
    m=Matrix((e1,e2))
    print(m)
    return (m,o)


def areCrossed(e1,e2,m,s):
    ip2d=geometry.intersect_line_line_2d(m*(e1.verts[0].co-s),m*(e1.verts[1].co-s),m*(e2.verts[0].co-s), m*(e2.verts[1].co-s))
    if ip2d is None: return None
    ip=m[0]*ip2d[0]+m[1]*ip2d[1]+s
    print (e1.verts[0].co,e1.verts[1].co,e2.verts[0].co, e2.verts[1].co)
    print (m*e1.verts[0].co,m*e1.verts[1].co,m*e2.verts[0].co, m*e2.verts[1].co)
    print (ip2d)
    print (ip)
    return ip


def keyToSortByNumEdges(planItem):
    return len(planItem["edges"])

def processFace(face, bm):
    normal=face.normal.normalized()
    edges=face.edges
    ne=len(edges)
    m,s=makePlaneBasis(edges[0].verts[0].co,edges[0].verts[1].co, normal)
    crossingPairsIndexes=[]
    for i in range(ne):
        e1=edges[i]
        for j in range(i+2,ne-(1 if i==0 else 0)):
            e2=edges[j]
            ip=areCrossed(e1,e2,m,s)
            if ip is not None:
                print("Crossing edges: %s %s ip=%s"%(i,j,ip))
                crossingPairsIndexes.append((i,j,ip))

    edgesToCollapse=set()
    plan=[]
    for cpi in crossingPairsIndexes:
        planItem={
            "ip":cpi[2],
            "edges":set()
        }
        perim1=0
        el1=set()
        for cei in crange(cpi[0]+1,cpi[1]-1,ne):
            perim1+=edges[cei].calc_length()
            el1.add(edges[cei])
        perim2=0
        el2=set()
        for cei in crange(cpi[1]+1,cpi[0]-1,ne):
            perim2+=edges[cei].calc_length()
            el2.add(edges[cei])
        if perim1<perim2:
            planItem["edges"]=el1
        else:
            planItem["edges"]=el2
        edgesToCollapse|=planItem["edges"]
        print("PlanItem %s"%planItem)
        plan.append(planItem)

    plan.sort(key=keyToSortByNumEdges) # to process nested loops from internal ones to external ones

    print("Num edges to collapse=%s"%len(edgesToCollapse))

    for planItem in plan:
        ip=planItem["ip"]
        for edge in planItem["edges"]:
            print("Collapse %s to %s"%(edge,ip))
            ev1,ev2=edge.verts
            ev1.co=ip
            ev2.co=ip

    bmesh.ops.collapse(bm, edges=list(edgesToCollapse))



class FixSelfIntersection(bpy.types.Operator):
    bl_description="Fix face self intersection"
    bl_idname="mesh.fixselfintersection"
    bl_label="az.FixSelfIntersection"

    @classmethod
    def poll(cls, context):
       ob = context.active_object
       return(ob and ob.type == 'MESH' and context.mode == 'EDIT_MESH')

    def invoke(self, context, event):
        bm = bmesh.from_edit_mesh(context.active_object.data)
        selectedFaces=[ f for f in bm.faces if f.select ]
        if len(selectedFaces)<1:
            raise Exception("Select at least 1 face")
            return

        for face in selectedFaces:
            processFace(face, bm)

        bmesh.update_edit_mesh(context.active_object.data)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(FixSelfIntersection)
    bpy.utils.register_class(FixSelfIntersectionPanel)
                                                                                        
def unregister():
    bpy.utils.unregister_class(FixSelfIntersection)
    bpy.utils.unregister_class(FixSelfIntersectionPanel)
    
if __name__ == "__main__":
    register()

bpy.app.debug = True



