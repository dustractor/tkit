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
        "name":        "tkit",
        "description": "edgemode select ops and hotkeys",
        "author":      "dustractor",
        "version":     (4,3),
        "blender":     (2,77,0),
        "location":    "",
        "warning":     "",
        "wiki_url":    "",
        "category":    "Mesh"}

import bpy
import bmesh

selected = lambda _: _.select
notselected = lambda _: not _.select
tagged = lambda _: _.tag
nottagged = lambda _: not _.tag

class EdgeSelectMode:
    @classmethod
    def poll(self,context):
        return context.active_object and \
        context.active_object.type == 'MESH' and \
        context.active_object.mode == 'EDIT' and \
        context.scene.tool_settings.mesh_select_mode[1]


class TKIT_OT_ie(EdgeSelectMode,bpy.types.Operator):
    bl_options = {'REGISTER','UNDO'}
    bl_label = "ie"
    bl_idname = 'tkit.ie'
    def execute(self,context):
        bm = bmesh.from_edit_mesh(context.active_object.data)
        for e in bm.edges:
            e.tag = len(list(filter(selected,e.link_faces))) == 1
        for e in filter(tagged,bm.edges):
            e.select_set(0)
            e.tag = 0
        bm.select_flush_mode()
        context.area.tag_redraw()
        return {'FINISHED'}


class TKIT_OT_oe(EdgeSelectMode,bpy.types.Operator):
    bl_options = {'REGISTER','UNDO'}
    bl_label = "oe"
    bl_idname = 'tkit.oe'
    def execute(self,context):
        bm = bmesh.from_edit_mesh(context.active_object.data)
        for e in bm.edges:
            e.tag = len(list(filter(selected,e.link_faces))) == 2
        for e in filter(tagged,bm.edges):
            e.select_set(0)
            e.tag = 0
        bm.select_flush_mode()
        context.area.tag_redraw()
        return {'FINISHED'}


class TKIT_OT_lon(EdgeSelectMode,bpy.types.Operator):
    bl_options = {'REGISTER','UNDO'}
    bl_label = "lon"
    bl_idname = 'tkit.lon'
    def execute(self,context):
        bm = bmesh.from_edit_mesh(context.active_object.data)
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
        bm.select_flush_mode()
        context.area.tag_redraw()
        return {'FINISHED'}


class TKIT_OT_lun(EdgeSelectMode,bpy.types.Operator):
    bl_options = {'REGISTER','UNDO'}
    bl_label = "lun"
    bl_idname = 'tkit.lun'
    def execute(self,context):
        bm = bmesh.from_edit_mesh(context.active_object.data)
        for e in filter(selected,bm.edges):
            for v in e.verts:
                v.tag ^= 1
        for v in filter(tagged,bm.verts):
            v.tag = 0
            for e in filter(selected,v.link_edges):
                e.select_set(0)
        bm.select_flush_mode()
        context.area.tag_redraw()
        return {'FINISHED'}


class TKIT_OT_epz(EdgeSelectMode,bpy.types.Operator):
    bl_options = {'REGISTER','UNDO'}
    bl_label = "epz"
    bl_idname = 'tkit.epz'
    def execute(self,context):
        bm = bmesh.from_edit_mesh(context.active_object.data)
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
        bm.select_flush_mode()
        context.area.tag_redraw()
        return {'FINISHED'}


class TKIT_OT_ef1n(EdgeSelectMode,bpy.types.Operator):
    bl_options = {'REGISTER','UNDO'}
    bl_label = "ef1n"
    bl_idname = 'tkit.ef1n'
    def execute(self,context):
        bm = bmesh.from_edit_mesh(context.active_object.data)
        for e in filter(selected,bm.edges):
            for f in filter(notselected,e.link_faces):
                for fe in filter(notselected,f.edges):
                    fe.tag = len(list(filter(selected,fe.verts))) == 1
        for e in bm.edges:
            e.select_set(e.tag)
            e.tag = 0
        bm.select_flush_mode()
        context.area.tag_redraw()
        return {'FINISHED'}


class TKIT_OT_ef2n(EdgeSelectMode,bpy.types.Operator):
    bl_options = {'REGISTER','UNDO'}
    bl_label = "ef2n"
    bl_idname = 'tkit.ef2n'
    def execute(self,context):
        bm = bmesh.from_edit_mesh(context.active_object.data)
        for e in filter(selected,bm.edges):
            for f in filter(notselected,e.link_faces):
                for fe in filter(notselected,f.edges):
                    fe.tag = len(list(filter(notselected,fe.verts))) == 2
        for e in bm.edges:
            e.select_set(e.tag)
            e.tag = 0
        bm.select_flush_mode()
        context.area.tag_redraw()
        return {'FINISHED'}


class TKIT_OT_ef2np(EdgeSelectMode,bpy.types.Operator):
    bl_options = {'REGISTER','UNDO'}
    bl_label = "ef2np"
    bl_idname = 'tkit.ef2np'
    def execute(self,context):
        bm = bmesh.from_edit_mesh(context.active_object.data)
        for e in filter(selected,bm.edges):
            for f in filter(notselected,e.link_faces):
                for fe in filter(notselected,f.edges):
                    fe.tag ^= len(list(filter(notselected,fe.verts))) == 2
        for e in bm.edges:
            e.select_set(e.tag)
            e.tag = 0
        bm.select_flush_mode()
        context.area.tag_redraw()
        return {'FINISHED'}


class TKIT_OT_ef2nx(EdgeSelectMode,bpy.types.Operator):
    bl_options = {'REGISTER','UNDO'}
    bl_label = "ef2nx"
    bl_idname = 'tkit.ef2nx'
    def execute(self,context):
        bm = bmesh.from_edit_mesh(context.active_object.data)
        for e in filter(selected,bm.edges):
            for f in filter(notselected,e.link_faces):
                for fe in filter(notselected,f.edges):
                    fe.tag = 1
        for e in bm.edges:
            e.select_set(e.tag)
            e.tag = 0
        bm.select_flush_mode()
        context.area.tag_redraw()
        return {'FINISHED'}


class TKIT_OT_help(bpy.types.Operator):
    """ ie '
        oe "
        lon ]
        lun [
        ef1n \\
        ef2n |
        ef2np C-|
        ef2nx C-A-|
        epz C-S-A-END """
    bl_label = "tkit quickhelp"
    bl_idname = "tkit.huh"
    bl_options = {"REGISTER","UNDO"}
    def draw(self,context):
        layout = self.layout
        box = layout.box()
        split = box.split()
        a,b = split.column(),split.column()
        for ln in filter(None,self.__doc__.splitlines()):
            p,ign,q = ln.strip().partition(" ")
            a.label(p)
            b.label(q)
        layout.label("in edit mode")
        layout.label("with edge selection")
        layout.label("C=ctrl")
        layout.label("S=shift")
        layout.label("A=alt")
    def execute(self,context):
        return {'FINISHED'}


classes = (
        TKIT_OT_help,
        TKIT_OT_ie,
        TKIT_OT_oe,
        TKIT_OT_lon,
        TKIT_OT_lun,
        TKIT_OT_epz,
        TKIT_OT_ef1n,
        TKIT_OT_ef2n,
        TKIT_OT_ef2np,
        TKIT_OT_ef2nx)


def register():
    list(map(bpy.utils.register_class,classes))
    keymaps = bpy.context.window_manager.keyconfigs['Blender'].keymaps
    km = keymaps['Mesh'].keymap_items.new
    km('tkit.ie',type='QUOTE',value='PRESS')
    km('tkit.oe',type='QUOTE',shift=True,value='PRESS')
    km('tkit.lon',type='RIGHT_BRACKET',value='PRESS')
    km('tkit.lun',type='LEFT_BRACKET',value='PRESS')
    km('tkit.ef1n',type='BACK_SLASH',value='PRESS')
    km('tkit.ef2n',type='BACK_SLASH',shift=True,value='PRESS')
    km('tkit.ef2np',type='BACK_SLASH',ctrl=True,shift=True,value='PRESS')
    km('tkit.ef2nx',type='BACK_SLASH',ctrl=True,alt=True,shift=True,value='PRESS')
    km('tkit.epz',type='END',ctrl=True,alt=True,shift=True,value='PRESS')

def unregister():
    list(map(bpy.utils.unregister_class,classes))

