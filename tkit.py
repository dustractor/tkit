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
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110 - 1301, USA.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "tkit",
    "author": "shams kitz aka dustractor",
    "version": (5,0),
    "blender": (2,6,7),
    "api": 56794,
    "location": "Hotkeys \\, [, ],\", & ' ",
    "description": "various edge selection operators",
    "warning": "",
    "wiki_url": "",
    "tracker_url": "",
    "category": "Mesh"}

import bpy
import bmesh

selected = lambda _: _.select
notselected = lambda _: not _.select
tagged = lambda _: _.tag
nottagged = lambda _: not _.tag

class these_ops:
    bl_options = {'REGISTER','UNDO'}
    def execute(self,context):
        self.f(bmesh.from_edit_mesh(context.active_object.data))
        context.area.tag_redraw()
        return {'FINISHED'}
    @classmethod
    def poll(self,context):
        return context.active_object and \
        context.active_object.type == 'MESH' and \
        context.active_object.mode == 'EDIT' and \
        context.scene.tool_settings.mesh_select_mode[1]

def op(f):
    return type('TAPU_OT_' + f.__name__,
    (these_ops,bpy.types.Operator),{
        'bl_label': f.__name__,
        'bl_idname': 'tapu.' + f.__name__,
        'f': f})

@op
def dbg(s,bm):
    tags,sels,xo = [[],[],[]],[[],[],[]],{0:'-',1:'+'}
    list(map(tags[0].append,[xo[_.tag] for _ in bm.verts]))
    list(map(sels[0].append,[xo[_.select] for _ in bm.verts]))
    list(map(tags[1].append,[xo[_.tag] for _ in bm.edges]))
    list(map(sels[1].append,[xo[_.select] for _ in bm.edges]))
    list(map(tags[2].append,[xo[_.tag] for _ in bm.faces]))
    list(map(sels[2].append,[xo[_.select] for _ in bm.faces]))
    list(map(print,["".join(_) for _ in tags]))
    list(map(print,["".join(_) for _ in sels]))

@op
def ie(s,bm):
    for e in bm.edges:
        e.tag = len(list(filter(selected,e.link_faces))) == 1
    for e in filter(tagged,bm.edges):
        e.select_set(0)
        e.tag = 0
    bm.select_flush_mode()
@op
def oe(s,bm):
    for e in bm.edges:
        e.tag = len(list(filter(selected,e.link_faces))) == 2
    for e in filter(tagged,bm.edges):
        e.select_set(0)
        e.tag = 0
    bm.select_flush_mode()
@op
def lon(s,bm):
    for e in filter(selected,bm.edges):
        for v in e.verts:
            v.tag ^= 1
        for f in e.link_faces:
            f.tag = 1
    efs = {f.index for f in filter(tagged,bm.faces)}
    for v in filter(tagged,bm.verts):
        v.tag = 0
        for e in filter(notselected,v.link_edges):
            e.tag = {f.index for f in e.link_faces}.isdisjoint(efs)
    for e in filter(tagged,bm.edges):
        e.tag = 0
        e.select_set(1)
    for f in bm.faces:
        f.tag = 0
@op
def lun(s,bm):
    for e in filter(selected,bm.edges):
        for v in e.verts:
            v.tag ^= 1
    for v in filter(tagged,bm.verts):
        v.tag = 0
        for e in filter(selected,v.link_edges):
            e.select_set(0)
@op
def epz(s,bm):
    for e in filter(selected,bm.edges):
        for v in e.verts:
            v.tag ^= 1
    for v in filter(tagged,bm.verts):
        for e in v.link_edges:
            e.select ^=1
    for e in bm.edges:
        e.select_set(e.select)
    for v in bm.verts:
        v.tag = 0
@op
def ef1n(s,bm):
    for e in filter(selected,bm.edges):
        for f in filter(notselected,e.link_faces):
            for fe in filter(notselected,f.edges):
                fe.tag = len(list(filter(selected,fe.verts))) == 1
    for e in bm.edges:
        e.select_set(e.tag)
        e.tag = 0
@op
def ef2n(s,bm):
    for e in filter(selected,bm.edges):
        for f in filter(notselected,e.link_faces):
            for fe in filter(notselected,f.edges):
                fe.tag = len(list(filter(notselected,fe.verts))) == 2
    for e in bm.edges:
        e.select_set(e.tag)
        e.tag = 0
@op
def ef2np(s,bm):
    for e in filter(selected,bm.edges):
        for f in filter(notselected,e.link_faces):
            for fe in filter(notselected,f.edges):
                fe.tag ^= len(list(filter(notselected,fe.verts))) == 2
    for e in bm.edges:
        e.select_set(e.tag)
        e.tag = 0
@op
def ef2nx(s,bm):
    for e in filter(selected,bm.edges):
        for f in filter(notselected,e.link_faces):
            for fe in filter(notselected,f.edges):
                fe.tag = 1
    for e in bm.edges:
        e.select_set(e.tag)
        e.tag = 0

def register():
    list(map(bpy.utils.register_class,these_ops.__subclasses__()))
    km = bpy.context.window_manager.keyconfigs.active.keymaps['Mesh'].keymap_items.new
    km('tapu.dbg',type='SLASH',shift=True,value='PRESS')
    km('tapu.ie',type='QUOTE',value='PRESS')
    km('tapu.oe',type='QUOTE',shift=True,value='PRESS')
    km('tapu.lon',type='RIGHT_BRACKET',value='PRESS')
    km('tapu.lun',type='LEFT_BRACKET',value='PRESS')
    km('tapu.epz',type='END',ctrl=True,alt=True,shift=True,value='PRESS')
    km('tapu.ef1n',type='BACK_SLASH',value='PRESS')
    km('tapu.ef2n',type='BACK_SLASH',shift=True,value='PRESS')
    km('tapu.ef2np',type='BACK_SLASH',ctrl=True,shift=True,value='PRESS')
    km('tapu.ef2nx',type='BACK_SLASH',ctrl=True,alt=True,shift=True,value='PRESS')

def unregister():
    list(map(bpy.utils.unregister_class,these_ops.__subclasses__()))
if __name__ == '__main__':
    register()

