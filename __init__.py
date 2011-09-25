# tkit v1.4 sep 25 2011
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
    "name" : "tkit",
    "author" : "Shams Kitz / dustractor@gmail.com",
    "version" : (1, 0),
    "blender" : (2, 5, 9),
    "api" : 39355,
    "location" : "View3d > tkit",
    "description" : "Variouf wayf to felect neighboring elementf.",
    "warning" : "",
    "wiki_url" : "",
    "tracker_url" : "github.com/dustractor/tkit",
    "category" : "Mesh"
}

import bpy

from array import array
from math import trunc
from random import random

m = 'heavy'
tk = None
inames = []

def meshsize(data):
    return list(map(len,[data.vertices,data.edges,data.faces]))


class TK:
    this_tk = bpy.props.IntVectorProperty()
    def __init__(self,context):
        me = context.object.data
        self.name = me.name
        self.vcount,self.ecount,self.fcount = meshsize(me)
        self.this_tk = (self.vcount,self.ecount,self.fcount)
        self.eki = {}
        self.eik = array('I',[0]*self.ecount*2)
        for e in me.edges:
            self.eki[e.key] = e.index
            self.eik[e.index],self.eik[e.index+self.ecount] = e.vertices[0],e.vertices[1]
        self.vstate,self.estate,self.fstate = (bytearray([0]*self.vcount),bytearray([0]*self.ecount),bytearray([0]*self.fcount))
        self.vxmask,self.exmask,self.fxmask = (bytearray([0]*self.vcount),bytearray([0]*self.ecount),bytearray([0]*self.fcount))
        self.vv = {i:set() for i in range(self.vcount)}
        for v1,v2 in me.edge_keys:
            self.vv[v1].add(v2)
            self.vv[v2].add(v1)
        self.ve = {i:set() for i in range(self.vcount)}
        for e in me.edges:
            for v in e.vertices:
                self.ve[v].add(e.index)
        self.vf = {i:set() for i in range(self.vcount)}
        for f in me.faces:
            for v in f.vertices:
                self.vf[v].add(f.index)
        self.ee = {i:set() for i in range(self.ecount)}
        for f in me.faces:
            ed=[self.eki[ek] for ek in f.edge_keys]
            for k in f.edge_keys:
                self.ee[self.eki[k]].update(ed)
        self.ef = {i:set() for i in range(self.ecount)}
        for f in me.faces:
            for k in f.edge_keys:
                self.ef[self.eki[k]].add(f.index)
        self.ff = {i:set() for i in range(self.fcount)}
        for f in me.faces:
            for ek in f.edge_keys:
                self.ff[f.index].update(self.ef[self.eki[ek]])

    def get_state(self,v=False,e=False,f=False):
        if v:
            bpy.data.meshes[self.name].vertices.foreach_get("select",self.vstate)
        if e:
            bpy.data.meshes[self.name].edges.foreach_get("select",self.estate)
        if f:        
            bpy.data.meshes[self.name].faces.foreach_get("select",self.fstate)
    def put_state(self,v=False,e=False,f=False):
        if v:
            bpy.data.meshes[self.name].vertices.foreach_set("select",self.vstate)
        elif e:
            bpy.data.meshes[self.name].edges.foreach_set("select",self.estate)
        elif f: 
            bpy.data.meshes[self.name].faces.foreach_set("select",self.fstate)

    def put_mask(self,v=False,e=False,f=False):
        if v:
            bpy.data.meshes[self.name].vertices.foreach_set("select",self.vxmask)
        elif e:
            bpy.data.meshes[self.name].edges.foreach_set("select",self.exmask)
        elif f: 
            bpy.data.meshes[self.name].faces.foreach_set("select",self.fxmask)

    def mask_state(self,v=False,e=False,f=False):
        if v:
            for i in range(self.vcount):
                self.vstate[i] ^= self.vxmask[i]
        if e:
            for i in range(self.ecount):
                self.estate[i] ^= self.exmask[i]
        if f: 
            for i in range(self.fcount):
                self.fstate[i] ^= self.fxmask[i]

    def reset_mask(self,v=False,e=False,f=False):
        if v:
            self.vxmask = bytearray([0]*self.vcount)
        if e:
            self.exmask = bytearray([0]*self.ecount)
        if f:
            self.fxmask = bytearray([0]*self.fcount)

    def svv(self):
        if not bpy.context.tool_settings.mesh_select_mode[0]:
            bpy.context.tool_settings.mesh_select_mode = (True,False,False)
        else:
            self.get_state(v=True)
            self.reset_mask(v=True)
            for i in range(self.vcount):
                if self.vstate[i]:
                    for j in self.vv[i]:
                        self.vxmask[j] = 1
            self.mask_state(v=True)
            self.put_state(v=True)
        
    def see(self):
        if not bpy.context.tool_settings.mesh_select_mode[1]:
            bpy.context.tool_settings.mesh_select_mode = (False,True,False)
        else:
            self.get_state(e=True)
            self.reset_mask(e=True)
            for i in range(self.ecount):
                if self.estate[i]:
                    hey = {self.eik[i],self.eik[i+self.ecount]}
                    for j in self.ee[i]:
                        lit = {self.eik[j],self.eik[j+self.ecount]}
                        if not hey.isdisjoint(lit):
                            self.exmask[j] = 1
            self.mask_state(e=True)
            self.put_state(e=True)
        
    def sff(self):
        if not bpy.context.tool_settings.mesh_select_mode[2]:
            bpy.context.tool_settings.mesh_select_mode = (False,False,True)
        else:
            self.get_state(f=True)
            self.reset_mask(f=True)
            for i in range(self.fcount):
                if self.fstate[i]:
                    for j in self.ff[i]:
                        self.fxmask[j] = 1
            self.mask_state(f=True)
            self.put_state(f=True)
        
    def je(self):
        self.get_state(f=True)
        self.get_state(e=True)
        self.reset_mask(e=True)
        for i in range(self.fcount):
            if self.fstate[i]:
                for k in bpy.data.meshes[self.name].faces[i].edge_keys:
                    self.exmask[self.eki[k]] = 1
        self.mask_state(e=True)
        self.put_state(e=True)
        
    def ie(self):
        te = {}
        self.get_state(e=True)
        self.reset_mask(e=True)
        self.get_state(f=True)
        for i in filter(lambda n: self.estate[n],range(self.ecount)):
            for j in self.ef[i]:
                if self.fstate[j]:
                    if not self.exmask[i]:
                        self.exmask[i] = 1
                    else:
                        self.estate[i] = 0        
        self.mask_state(e=True)
        self.put_state(e=True)
        
    def e_lat(self):
        self.get_state(e=True)
        orig = list(filter(lambda n:self.estate[n], range(self.ecount)))
        self.reset_mask(e=True)
        for e in filter(lambda n: self.estate[n],range(self.ecount)):
            for f in self.ef[e]:
                for k in bpy.data.meshes[self.name].faces[f].edge_keys:
                    vin = False
                    for v in bpy.data.meshes[self.name].edges[e].key:
                        if v in k:
                            vin = True
                    if vin:
                        continue
                    else:
                        self.exmask[self.eki[k]] = 1
        self.mask_state(e=True)
        for e in orig:
            self.estate[e] = 1
        self.put_state(e=True)

    def e_lon(self):
        self.get_state(v=True,e=True,f=True)
        self.reset_mask(v=True,e=True,f=True)
        for e in filter(lambda n: self.estate[n],range(self.ecount)):
            for v in bpy.data.meshes[self.name].edges[e].key:
                self.vxmask[v] ^= 1
            for f in self.ef[e]:
                for v in bpy.data.meshes[self.name].faces[f].vertices_raw:
                    self.vstate[v] = 1
        for v in list(filter(lambda n: self.vxmask[n],range(self.vcount))):
            for vn in self.vv[v]:
                if not self.vstate[vn] and (vn != v):
                    self.estate[self.eki[(min(v,vn),max(v,vn))]] = 1
        self.put_state(e=True)

    def life(self):
        self.get_state(f=True)
        F = {}
        s = set()
        x = set()
        for f in range(self.fcount):
            F[f] = set()
            for v in bpy.data.meshes[self.name].faces[f].vertices_raw:
                for fn in filter(lambda n: self.fstate[n] and f != n,self.vf[v]):
                    F[f].add(fn)
        for f in F:
            if len(F[f]) == 3:
                s.add(f)
            elif len(F[f]) != 2:
                x.add(f)
        for f in range(self.fcount):
            if f in s:
                self.fstate[f] = 1
            if f in x:
                self.fstate[f] = 0
        self.put_state(f=True)

    def rand(self):
        v,e,f = bpy.context.tool_settings.mesh_select_mode
        x,n = {
            (True,False,False):(self.vstate,self.vcount),
            (False,True,False):(self.estate,self.ecount),
            (False,False,True):(self.fstate,self.fcount)
        }[(v,e,f)]
        for i in range(n):
            x[i] = trunc(0.499+random())
        if v:
            self.put_state(v=True)
        if e:
            self.put_state(e=True)
        if f:
            self.put_state(f=True)


    def __repr__(self):
        kz = list(self.__dict__.keys())
        kz.sort()
        return "\n".join(["%s:%s"%(a,self.__dict__[a]) for a in kz]) 
        

class R:pass


class op:
    def execute(self,context):
        self.f(context)
        return {'FINISHED'}


class tk_op:
    @classmethod
    def poll(self,context):
        global tk
        if tk is not None:
            a,b,c = meshsize(context.object.data)
            d,e,f = tk.this_tk
            return (a == d) and (b == e) and (c == f)
    def execute(self,context):
        global tk
        bpy.ops.object.mode_set(mode='OBJECT')
        try:
            self.f(context,tk)
        except RuntimeError:
            print('heavy error.  attempting rebuild of internal maps.  (mesh size must have changed.)')
            tk.__init__(context)
            self.f(context,tk)
        bpy.ops.object.mode_set(mode='EDIT')
        return {'FINISHED'}


def OT(f):
    global inames
    label = {1:f.__doc__,0:f.__name__.replace("_"," ").title()}[f.__doc__ is not None]
    rname = "_".join([m.upper(),"OT",f.__name__])
    iname = ".".join([m,f.__name__])
    inames.append(iname)
    return type( rname, (op,bpy.types.Operator,R), { 'bl_idname':iname, 'bl_label':label, 'f':f })

def TK_OT(f):
    global inames
    label = {1:f.__doc__,0:f.__name__.replace("_"," ").title()}[f.__doc__ is not None]
    rname = "_".join([m.upper(),"OT",f.__name__])
    iname = ".".join([m,f.__name__])
    inames.append(iname)
    return type( rname, (tk_op,bpy.types.Operator,R), { 'bl_idname':iname, 'bl_label':label, 'f':f })

 
@OT
def build_maps(self,context):
    global tk
    tk = TK(context)
    bpy.ops.object.mode_set(mode="EDIT")

@TK_OT
def print_debug(self,context,_tk):
    print(_tk)

@TK_OT
def svv(self,context,_tk):
    _tk.svv()

@TK_OT
def see(self,context,_tk):
    _tk.see()

@TK_OT
def sff(self,context,_tk):
    _tk.sff()

@TK_OT
def je(self,context,_tk):
    _tk.je()

@TK_OT
def ie(self,context,_tk):
    _tk.ie()

@TK_OT
def e_lat(self,context,_tk):
    _tk.e_lat()

@TK_OT
def e_lon(self,context,_tk):
    _tk.e_lon()

@TK_OT
def conway(self,context,_tk):
    _tk.life()

@TK_OT
def rand(self,context,_tk):
    _tk.rand()

def heavy_draw(self,context):
    list(map(self.layout.operator,inames))

class HEAVY_PT_heavypanel(bpy.types.Panel,R):
    bl_label = "Heavy"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "object"
    draw = heavy_draw

class HEAVY_OT_tapu(bpy.types.Operator,R):
    bl_idname = "heavy.tapu"
    bl_label = "tapu"
    evtdict ={
        "R": bpy.ops.heavy.rand,
        "V": bpy.ops.heavy.svv,
        "E": bpy.ops.heavy.see,
        "F": bpy.ops.heavy.sff,
        "J": bpy.ops.heavy.je,
        "I": bpy.ops.heavy.ie,
        "L": bpy.ops.heavy.e_lat,
        "K": bpy.ops.heavy.e_lon,
        "C": bpy.ops.heavy.life}
    
    @classmethod
    def poll(self,context):
        return context.active_object != None
        
    def modal(self,context,event):
        wrongval = event.value not in {'PRESS'}
        mouse = event.type.endswith('MOUSE')
        na = event.type not in self.evtdict.keys()    
        if event.type in {'Q','ESC'}:
            return {'FINISHED'}
        elif wrongval|mouse|na:
            return {'PASS_THROUGH'}
        else:
            global tk
            bpy.ops.object.mode_set(mode='OBJECT')
            opx = self.evtdict.get(event.type,lambda:None)
            try:
                opx()
            except RuntimeError:
                tk.__init__(context)
                opx()
            bpy.ops.object.mode_set(mode='EDIT')
            return {'RUNNING_MODAL'}

    def invoke(self,context,event):
        global tk
        if tk is None:
            bpy.ops.object.mode_set(mode='OBJECT')
            tk = TK(context)
            bpy.ops.object.mode_set(mode='EDIT')
            
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


def register():
    list(map(bpy.utils.register_class,R.__subclasses__()))
    bpy.data.window_managers['WinMan'].keyconfigs['Blender'].keymaps['Mesh'].keymap_items.new(type='T',alt=True,idname='heavy.tapu',value='PRESS')

def unregister():
    list(map(bpy.utils.unregister_class,R.__subclasses__()))

if __name__ == "__main__":
    register()

