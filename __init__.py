# Topokit v1.0 Several functions to select neighboring elements in a topology.
# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name" : "Topology Kit",
    "author" : "dustractor",
    "version" : (2, 3),
    "blender" : (2, 5, 9),
    "api" : 39355,
    "location" : "View3d > Ui > topokit",
    "description" : "Variouf wayf to felect neighboring elementf.",
    "warning" : "",
    "wiki_url" : "",
    "tracker_url" : "",
    "category" : "Mesh"
}
import bpy
import bgl
import blf

from math import degrees,radians,sin,cos,pi
from mathutils import Vector,Euler

class R:pass

def true(x):
    x.select=True

@property
def eki(mesh):
    return {e.key:e.index for e in mesh.edges}
@eki.setter
def eki(mesh,x):
    raise AttributeError
@property
def vsel(mesh):
    return {v.index for v in mesh.vertices if v.select}
@vsel.setter
def vsel(mesh,L):
    list(map(true,map(lambda i:mesh.vertices[i],L)))

@property
def esel(mesh):
    return {e.index for e in mesh.edges if e.select}
@esel.setter
def esel(mesh,L):
    list(map(true,map(lambda i:mesh.edges[i],L)))

@property
def fsel(mesh):
    return {f.index for f in mesh.faces if f.select}
@fsel.setter
def fsel(mesh,L):
    list(map(true,map(lambda i:mesh.faces[i],L)))

@property
def vv(mesh):
    d = {i:set() for i in range(len(mesh.vertices))}
    for v1,v2 in mesh.edge_keys:
        d[v1].add(v2)
        d[v2].add(v1)
    return d
@vv.setter
def vv(mesh,L):
    raise AttributeError

@property
def ve(mesh):
    d = {i:set() for i in range(len(mesh.vertices))}
    for e in mesh.edges:
        for v in e.vertices:
            d[v].add(e.index)
    return d
@ve.setter
def ve(mesh,L):
    raise AttributeError

@property
def vf(mesh):
    d={i:set() for i in range(len(mesh.vertices))}
    for f in mesh.faces:
        for v in f.vertices:
            d[v].add(f.index)
    return d
@vf.setter
def vf(mesh,L):
    raise AttributeError

@property
def ee(mesh):
    eki = mesh.eki
    d={i:set() for i in range(len(mesh.edges))}
    for f in mesh.faces:
        ed=[eki[ek] for ek in f.edge_keys]
        for k in f.edge_keys:
            d[eki[k]].update(ed)
    return d
@ee.setter
def ee(mesh,L):
    raise AttributeError

@property
def ef(mesh):
    eki = mesh.eki
    d = {i:set() for i in range(len(mesh.edges))}
    for f in mesh.faces:
        for k in f.edge_keys:
            d[eki[k]].add(f.index)
    return d
@ef.setter
def ef(mesh,L):
    raise AttributeError

@property
def ff(mesh):
    eki=mesh.eki
    ef=mesh.ef
    d={i:set() for i in range(len(mesh.faces))}
    for f in mesh.faces:
        for ek in f.edge_keys:
            d[f.index].update(ef[eki[ek]])
    return d
@ff.setter
def ff(mesh,L):
    raise AttributeError

@property
def svv(mesh):
    n=set()
    s=mesh.vsel
    m=mesh.vv
    d=filter(lambda x:x in s,m)
    for v in d:
        n.update(m[v])
    return n-s
@svv.setter
def svv(mesh,L):
    raise AttributeError

@property
def see(mesh):
    n=set()
    s=mesh.esel
    m=mesh.ee
    d=filter(lambda x:x in s,m)
    for e in d:
        n.update(m[e])
    return n-s
@see.setter
def see(mesh,L):
    raise AttributeError

@property
def sff(mesh):
    n=set()
    s=mesh.fsel
    m=mesh.ff
    d=filter(lambda x:x in s,m)
    for f in d:
        n.update(m[f])
    return n-s
@sff.setter
def sff(mesh,L):
    raise AttributeError

@property
def je(mesh):
    eki=mesh.eki
    fs=mesh.fsel
    es={i:0 for i in mesh.esel}
    for f in fs:
        for k in mesh.faces[f].edge_keys:
            es[eki[k]]+=1
    return list(filter(lambda x:es[x]<1,es))
@je.setter
def je(mesh,L):
    raise AttributeError

@property
def jei(mesh):
    es=mesh.esel
    a={i:False for i in es}
    z=set()
    ef=mesh.ef
    for e in es:
        for f in ef[e]:
            if mesh.faces[f].select:
                if not a[e]:
                    a[e]=True
                else:
                    z.add(e)
    for e in a:
        if a[e]:
            es.remove(e)
    es.update(z)
    return es
@jei.setter
def jei(mesh,L):
    raise AttributeError

@property
def e_lat(mesh):
    ts=set()
    eki=mesh.eki
    es=mesh.esel
    ef=mesh.ef
    for e in es:
        for f in ef[e]:
            for k in mesh.faces[f].edge_keys:
                vin=False
                for v in mesh.edges[e].key:
                    if v in k:
                        vin = True
                if vin:
                    continue
                else:
                    ts.add(eki[k])
    if ts.issubset(es):
        return []
    return ts-es
@e_lat.setter
def e_lat(mesh,L):
    raise AttributeError

@property
def e_lon(mesh):
    ts=set()
    ef=mesh.ef
    vv=mesh.vv
    ve=mesh.ve
    es=mesh.esel
    pts={}
    for v in mesh.vsel:
        pts[v]=False
    impfs=set()
    for e in es:
        for v in mesh.edges[e].key:
            pts[v] = not pts[v]
        for f in ef[e]:
            impfs.add(f)
    evs=[pt for pt in pts if pts[pt] == True]
    implicated_face_verts=set()
    epneighbors=set()
    for f in impfs:
        for v in mesh.faces[f].vertices:
            implicated_face_verts.add(v)
    for v in evs:
        for vn in vv[v]:
            epneighbors.add(vn)
    them=epneighbors.difference(implicated_face_verts)
    for v in them:
        for e in ve[v]:
            for vi in mesh.edges[e].key:
                if vi in evs:
                    ts.add(e)
    if ts.issubset(es):
        return []
    return ts-es
@e_lon.setter
def e_lon(mesh,L):
    raise AttributeError

@property
def life(mesh):
    ts=set()
    tx=set()
    vf=mesh.vf
    fs=mesh.fsel
    r=len(mesh.faces)
    d={i:set() for i in range(r)}
    for f in mesh.faces:
        for v in f.vertices:
            for n in vf[v]-{f.index}:
                if mesh.faces[n].select:
                    d[f.index].add(n)
    for i in d:
        L=len(d[i])
        if L ==3:
            ts.add(i)
        elif L !=2:
            tx.add(i)
    fs.update(ts)
    return fs-tx
@life.setter
def life(mesh,L):
    print(42)
    raise AttributeError

def kit_register():
    bpy.types.Mesh.eki=eki
    bpy.types.Mesh.vsel=vsel
    bpy.types.Mesh.esel=esel
    bpy.types.Mesh.fsel=fsel
    bpy.types.Mesh.vv=vv
    bpy.types.Mesh.ve=ve
    bpy.types.Mesh.vf=vf
    bpy.types.Mesh.ee=ee
    bpy.types.Mesh.ef=ef
    bpy.types.Mesh.ff=ff
    bpy.types.Mesh.svv=svv
    bpy.types.Mesh.see=see
    bpy.types.Mesh.sff=sff
    bpy.types.Mesh.je=je
    bpy.types.Mesh.jei=jei
    bpy.types.Mesh.e_lat=e_lat
    bpy.types.Mesh.e_lon=e_lon
    bpy.types.Mesh.life=life

def kit_unregister():
    del bpy.types.Mesh.eki
    del bpy.types.Mesh.vsel
    del bpy.types.Mesh.esel
    del bpy.types.Mesh.fsel
    del bpy.types.Mesh.vv
    del bpy.types.Mesh.ve
    del bpy.types.Mesh.vf
    del bpy.types.Mesh.ee
    del bpy.types.Mesh.ef
    del bpy.types.Mesh.ff
    del bpy.types.Mesh.svv
    del bpy.types.Mesh.see
    del bpy.types.Mesh.sff
    del bpy.types.Mesh.je
    del bpy.types.Mesh.jei
    del bpy.types.Mesh.e_lat
    del bpy.types.Mesh.e_lon
    del bpy.types.Mesh.life

class ArcMenuOp(bpy.types.Operator):
    arc_resolution=12
    arc_radius=64
    arc_font='/Library/Fonts/Osaka.ttf'
    arc_textsize=11
    arc_textdpi=109
    tmp=bpy.props.StringProperty()
    def init(self):
        self.UP=Vector((0,1,0))
        self.sector_count=len(self.sector_list)
        self.arc_length=(pi*2)/self.sector_count
        self.arc_stepsize=1/self.arc_resolution
        self.font_id=blf.load(self.arc_font)
    def text(self,text,pos):
        blf.position(self.font_id, pos.x, pos.y, 0)
        blf.size(self.font_id, self.arc_textsize, self.arc_textdpi)
        blf.draw(self.font_id, text)
    def draw_sectors(self,draw_position,active_position):
        a=active_position-draw_position
        a.normalize()
        if active_position.x>draw_position.x:
            angleC=pi+a.to_track_quat('-Y','Z').angle
        else:
            angleC=a.to_track_quat('Y','Z').angle
        for i in range(self.sector_count):
            angleA=i*self.arc_length
            angleB=angleA+self.arc_length
            if (angleC > angleA) and (angleC < angleB):            
                bgl.glColor4f(1.0,0.0,0.0,0.5)
                self.tmp=self.sector_list[i]
            else:
                bgl.glColor4f(0.0,1.0,0.0,0.2)
            A=Euler((0,0,angleA)).to_quaternion()
            B=Euler((0,0,angleB)).to_quaternion()
            bgl.glBegin(bgl.GL_LINE_STRIP)
            for j in range(self.arc_resolution):
                pos=self.UP*self.arc_radius
                rot=A.slerp(B,j*self.arc_stepsize)
                pos.rotate(rot)
                pos+=draw_position
                bgl.glVertex2f(pos.x,pos.y)
            bgl.glEnd()
            Tp=self.UP*(2*self.arc_radius)
            Tr=A.slerp(B,0.5)
            Tp.rotate(Tr)
            Tp+=draw_position
            self.text(self.sector_list[i],Tp)
    def dpx(self,context):
        self.draw_sectors(self.initv,self.mouse)
    def modal(self, context, event):
        context.area.tag_redraw()
        if event.type == 'MOUSEMOVE':
            self.mouse=Vector((event.mouse_region_x, event.mouse_region_y,0))
        elif event.type == 'LEFTMOUSE':
            context.region.callback_remove(self._handle)
            if self.tmp:
                exec("bpy.ops.%s('INVOKE_DEFAULT')"%self.tmp)
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:
            context.region.callback_remove(self._handle)
            return {'CANCELLED'}
        return {'RUNNING_MODAL'}
    def invoke(self, context, event):
        if context.area.type == 'VIEW_3D':
            self.init()
            context.window_manager.modal_handler_add(self)
            self.initv=Vector((event.mouse_region_x, event.mouse_region_y,0))
            self._handle = context.region.callback_add(self.dpx, (context,), 'POST_PIXEL')
            return {'RUNNING_MODAL'}
        else:
            self.report({'WARNING'}, "View3D not found, cannot run operator")
            return {'CANCELLED'}

class TK_ArcMenu_SelectMeshElemNeighbors(ArcMenuOp,R):
    bl_idname = "view3d.arcmenu_nns"
    bl_label = "arcmenu -Neighboring Element Selection"
    sector_list=['object.svv','object.see','object.sff','object.jsvv','object.jsee','object.jsff']

class TK_ArcMenu_EdgeSelectors_lnr(ArcMenuOp,R):
    bl_idname = "view3d.arcmenu_ees"
    bl_label = "arcmenu -Edge Selection  - Inclusive"
    sector_list=['object.e_lat','object.e_lon','object.je_lat','object.je_lon']

class TK_ArcMenu_EdgeSelectors_stat(ArcMenuOp,R):
    bl_idname = "view3d.arcmenu_nns"
    bl_label = "arcmenu -Edge Selection state calculations"
    sector_list=['object.je','object.jei']

class TK_ArcMenu_ConwaysLife(ArcMenuOp,R):
    bl_idname = "view3d.arcmenu_conway"
    bl_label = "arcmenu -conway"
    sector_list=['object.life']

def _clear():
    bpy.ops.object.editmode_toggle()
    bpy.ops.mesh.select_all(action='DESELECT')
    bpy.ops.object.editmode_toggle()

class MESH_OT_svv(bpy.types.Operator,R):
    '''The set of selected verts AND their vert neighbors.'''
    bl_idname = "object.svv"
    bl_label = "V>V"
    bl_options = {'REGISTER','UNDO'}
    def execute(self,context):
        bpy.context.tool_settings.mesh_select_mode=(True,False,False)
        bpy.ops.object.editmode_toggle()
        context.active_object.data.vsel=context.active_object.data.svv
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

class MESH_OT_see(bpy.types.Operator,R):
    '''The set of selected edges AND their edge neighbors.'''
    bl_idname="object.see"
    bl_label="E>E"
    bl_options={'REGISTER','UNDO'}
    def execute(self,context):
        bpy.context.tool_settings.mesh_select_mode=(False,True,False)
        bpy.ops.object.editmode_toggle()
        context.active_object.data.esel=context.active_object.data.see
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

class MESH_OT_sff(bpy.types.Operator,R):
    '''The set of selected face AND their face neighbors*.'''
    bl_idname="object.sff"
    bl_label="F>F"
    bl_options={'REGISTER','UNDO'}
    def execute(self,context):
        bpy.context.tool_settings.mesh_select_mode=(False,False,True)
        bpy.ops.object.editmode_toggle()
        context.active_object.data.fsel=context.active_object.data.sff
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

class MESH_OT_jsvv(bpy.types.Operator,R):
    '''Just the neigbors of the selected vertices.'''
    bl_idname="object.jsvv"
    bl_label="jV>V"
    bl_options={'REGISTER','UNDO'}
    def execute(self,context):
        bpy.context.tool_settings.mesh_select_mode=(True,False,False)
        bpy.ops.object.editmode_toggle()
        t=context.active_object.data.svv
        _clear()
        context.active_object.data.vsel=t
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

class MESH_OT_jsee(bpy.types.Operator,R):
    '''Just the neigbors of the selected edges'''
    bl_idname="object.jsee"
    bl_label="jE>E"
    bl_options={'REGISTER','UNDO'}
    def execute(self,context):
        bpy.context.tool_settings.mesh_select_mode=(False,True,False)
        bpy.ops.object.editmode_toggle()
        t=context.active_object.data.see
        _clear()
        context.active_object.data.esel=t
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

class MESH_OT_jsff(bpy.types.Operator,R):
    '''Just the neighbors of the selected faces*'''
    bl_idname="object.jsff"
    bl_label="jF>F"
    bl_options={'REGISTER','UNDO'}
    def execute(self,context):
        bpy.context.tool_settings.mesh_select_mode=(False,False,True)
        bpy.ops.object.editmode_toggle()
        t=context.active_object.data.sff
        _clear()
        context.active_object.data.fsel=t
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

class MESH_OT_je(bpy.types.Operator,R):
    bl_idname="object.je"
    bl_label="jE"
    bl_options={'REGISTER','UNDO'}
    def execute(self,context):
        bpy.context.tool_settings.mesh_select_mode=(False,True,False)
        bpy.ops.object.editmode_toggle()
        t=context.active_object.data.je
        _clear()
        context.active_object.data.esel=t
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

class MESH_OT_jei(bpy.types.Operator,R):
    bl_idname="object.jei"
    bl_label="iE"
    bl_options={'REGISTER','UNDO'}
    def execute(self,context):
        bpy.context.tool_settings.mesh_select_mode=(False,True,False)
        bpy.ops.object.editmode_toggle()
        t=context.active_object.data.jei
        _clear()
        context.active_object.data.esel=t
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

class MESH_OT_e_lat(bpy.types.Operator,R):
    bl_idname="object.e_lat"
    bl_label="+Lat E"
    bl_options={'REGISTER','UNDO'}
    def execute(self,context):
        bpy.context.tool_settings.mesh_select_mode=(False,True,False)
        bpy.ops.object.editmode_toggle()
        context.active_object.data.esel=context.active_object.data.e_lat
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

class MESH_OT_e_lon(bpy.types.Operator,R):
    bl_idname="object.e_lon"
    bl_label="+Lon E"
    bl_options={'REGISTER','UNDO'}
    def execute(self,context):
        bpy.context.tool_settings.mesh_select_mode=(False,True,False)
        bpy.ops.object.editmode_toggle()
        context.active_object.data.esel=context.active_object.data.e_lon
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

class MESH_OT_je_lat(bpy.types.Operator,R):
    bl_idname="object.je_lat"
    bl_label="jLat e"
    bl_options={'REGISTER','UNDO'}
    def execute(self,context):
        bpy.context.tool_settings.mesh_select_mode=(False,True,False)
        bpy.ops.object.editmode_toggle()
        t=context.active_object.data.e_lat
        _clear()
        context.active_object.data.esel=t
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

class MESH_OT_je_lon(bpy.types.Operator,R):
    bl_idname="object.je_lon"
    bl_label="jLon e"
    bl_options={'REGISTER','UNDO'}
    def execute(self,context):
        bpy.context.tool_settings.mesh_select_mode=(False,True,False)
        bpy.ops.object.editmode_toggle()
        t=context.active_object.data.e_lon
        _clear()
        context.active_object.data.esel=t
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

class MESH_OT_life(bpy.types.Operator,R):
    '''Apply life* algorithm to face selection.'''
    bl_idname="object.life"
    bl_label="Conway"
    bl_options={'REGISTER','UNDO'}
    def execute(self,context):
        bpy.context.tool_settings.mesh_select_mode=(False,False,True)
        bpy.ops.object.editmode_toggle()
        t=context.active_object.data.life
        _clear()
        context.active_object.data.fsel=t
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

class AddDelta(bpy.types.Operator,R):
    '''Three faces and four verts (one center vert)'''
    bl_idname='mesh.primitive_delt_add'
    bl_label='Add Delta'
    bl_options={'REGISTER','UNDO'}

    def execute(self,context):
        v=[(0.0,0.0,0.0)]
        f=[]
        side=(pi*2)/3
        for i in range(3):
            s=i*side
            x=(cos(s),sin(s),0.0)
            v.append(x)
        for i in range(1,3):
            f.append((0,i,i+1))
        f.append((0,3,1))
        mesh=bpy.data.meshes.new('Tri')
        mesh.from_pydata(v,[],f)
        mesh.update()
        obj=bpy.data.objects.new('Tri',mesh)
        context.scene.objects.link(obj)
        obj.location=context.space_data.cursor_location
        obj.select=True
        context.scene.objects.active=obj
        return {'FINISHED'}

class AddTriangle(bpy.types.Operator,R):
    '''Adds a triangle'''
    bl_idname='mesh.primitive_tri_add'
    bl_label='Add Triangle'
    bl_options={'REGISTER','UNDO'}
    def execute(self,context):
        mesh=bpy.data.meshes.new('Tri')
        mesh.from_pydata(
            [(sin(t),cos(t),0.0) for t in [(i*pi*2.0)/3.0 for i in [0,1,2]]],
            [],
            [(0,1,2)]
            )
        mesh.update()
        obj=bpy.data.objects.new('Tri',mesh)
        context.scene.objects.link(obj)
        obj.location=context.space_data.cursor_location
        obj.select=True
        context.scene.objects.active=obj
        return {'FINISHED'}

class exmerge(bpy.types.Operator,R):
    bl_idname='object.exmerge'
    bl_label='Extrude+Merge'
    bl_options={'REGISTER','UNDO'}
    def execute(self,context):
        if len(context.object.data.vertices) > 3:
            bpy.context.tool_settings.mesh_select_mode=(False,False,True)
            bpy.ops.mesh.extrude(type='FACES')
            bpy.ops.mesh.merge(type='COLLAPSE')
        return {'FINISHED'}

def topokit_buttons(self,context):
    Vm,Em,Fm=context.tool_settings.mesh_select_mode
    self.layout.row().label("TopoKit:")
    b=self.layout.box()
    s=b.split(align=True)
    c1,c2,c3=s.column(),s.column(),s.column()
    c1.active,c2.active,c3.active=(Vm,Em,Fm)
    c1.operator("object.svv")
    c2.operator("object.see")
    c3.operator("object.sff")

    c1.operator("object.jsvv")
    c2.operator("object.jsee")
    c3.operator("object.jsff")

    s=b.split(align=True)
    s.active=Em
    c1,c2=(s.column(),s.column())

    c1.operator("object.je")
    c2.operator("object.jei")

    c1.operator("object.je_lat")
    c2.operator("object.je_lon")

    c1.operator("object.e_lat")
    c2.operator("object.e_lon")

    r=b.row()
    r.active=Fm
    r.operator("object.life")

class tk_buttons_on(bpy.types.Operator,R):
    bl_idname="object.tk_on"
    bl_label="put buttons in v3dMT panel"
    def execute(self,context):
        bpy.types.VIEW3D_PT_tools_meshedit.append(topokit_buttons)
        return {'FINISHED'}

class tk_buttons_off(bpy.types.Operator,R):
    bl_idname="object.tk_off"
    bl_label="remove buttons from v3dMT panel"
    def execute(self,context):
        bpy.types.VIEW3D_PT_tools_meshedit.remove(topokit_buttons)
        return {'FINISHED'}

def exmerge_menu(self,context):
    self.layout.operator('object.exmerge')

class TopoKitAuxMenu(bpy.types.Menu,R):
    bl_idname="VIEW3D_MT_topokit_aux_menu"
    bl_label="Aux"
    def draw(self,context):
        l=self.layout
        l.operator('object.exmerge')

class TopoKitMenu(bpy.types.Menu,R):
    bl_idname="VIEW3D_MT_topokit_menu"
    bl_label="TopoKit"
    def draw(self,context):
        l=self.layout

        l.operator("object.svv")
        l.operator("object.see")
        l.operator("object.sff")
        l.separator()
        l.operator("object.jsvv")
        l.operator("object.jsee")
        l.operator("object.jsff")
        l.separator()
        l.operator("object.je")
        l.operator("object.jei")
        l.separator()
        l.operator("object.e_lat")
        l.operator("object.e_lon")
        l.separator()
        l.operator("object.je_lat")
        l.operator("object.je_lon")
        l.separator()
        l.operator("object.life")


def topokit_mainmenu(self,context):
    self.layout.menu("VIEW3D_MT_topokit_menu")

def tri_menu_func(self,context):
    self.layout.operator(AddTriangle.bl_idname,icon='MESH_DATA')

def delt_menu_func(self,context):
    self.layout.operator(AddDelta.bl_idname,icon='PLAY')

def ui_register():
    bpy.types.VIEW3D_MT_edit_mesh_specials.append(topokit_mainmenu)
    bpy.types.INFO_MT_mesh_add.append(tri_menu_func)
    bpy.types.INFO_MT_mesh_add.append(delt_menu_func)

def ui_unregister():
    bpy.types.INFO_MT_mesh_add.remove(tri_menu_func)
    bpy.types.INFO_MT_mesh_add.remove(delt_menu_func)
    bpy.types.VIEW3D_MT_edit_mesh_specials.remove(topokit_mainmenu)


def register():
    kit_register()
    list(map(bpy.utils.register_class, R.__subclasses__()))
    ui_register()

def unregister():
    kit_unregister()
    list(map(bpy.utils.unregister_class,R.__subclasses__()))
    ui_unregister()

if __name__=="__main__":
    register()

