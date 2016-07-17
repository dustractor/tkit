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


class TAPU_OT_ie(EdgeSelectMode,bpy.types.Operator):
    bl_options = {'REGISTER','UNDO'}
    bl_label = "ie"
    bl_idname = 'tapu.ie'
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


class TAPU_OT_oe(EdgeSelectMode,bpy.types.Operator):
    bl_options = {'REGISTER','UNDO'}
    bl_label = "oe"
    bl_idname = 'tapu.oe'
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


class TAPU_OT_lon(EdgeSelectMode,bpy.types.Operator):
    bl_options = {'REGISTER','UNDO'}
    bl_label = "lon"
    bl_idname = 'tapu.lon'
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


class TAPU_OT_lun(EdgeSelectMode,bpy.types.Operator):
    bl_options = {'REGISTER','UNDO'}
    bl_label = "lun"
    bl_idname = 'tapu.lun'
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


class TAPU_OT_epz(EdgeSelectMode,bpy.types.Operator):
    bl_options = {'REGISTER','UNDO'}
    bl_label = "epz"
    bl_idname = 'tapu.epz'
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


class TAPU_OT_ef1n(EdgeSelectMode,bpy.types.Operator):
    bl_options = {'REGISTER','UNDO'}
    bl_label = "ef1n"
    bl_idname = 'tapu.ef1n'
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


class TAPU_OT_ef2n(EdgeSelectMode,bpy.types.Operator):
    bl_options = {'REGISTER','UNDO'}
    bl_label = "ef2n"
    bl_idname = 'tapu.ef2n'
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


class TAPU_OT_ef2np(EdgeSelectMode,bpy.types.Operator):
    bl_options = {'REGISTER','UNDO'}
    bl_label = "ef2np"
    bl_idname = 'tapu.ef2np'
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


class TAPU_OT_ef2nx(EdgeSelectMode,bpy.types.Operator):
    bl_options = {'REGISTER','UNDO'}
    bl_label = "ef2nx"
    bl_idname = 'tapu.ef2nx'
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


class TAPU_OT_huh(bpy.types.Operator):
    bl_label = "tkit quickhelp"
    bl_idname = "tkit.huh"
    bl_options = {"REGISTER","UNDO"}
    def draw(self,context):
        box = self.layout.box()
        box.label("in edit mode")
        box.label("with edge selection")
        box.label("C=ctrl")
        box.label("S=shift")
        box.label("A=alt")
        box.separator()
        split = box.split()
        a,b = split.column(),split.column()
        a.label("ie")
        b.label("'")
        a.label("oe")
        b.label('"')
        a.label("lon")
        b.label("]")
        a.label("lun")
        b.label("[")
        a.label("epz")
        b.label("C-S-A-END")
        a.label("ef1n")
        b.label("\\")
        a.label("ef2n")
        b.label("|")
        a.label("ef2np")
        b.label("C-|")
        a.label("ef2nx")
        b.label("C-A-|")

    def execute(self,context):
        return {'FINISHED'}

classes = (
        TAPU_OT_huh,
        TAPU_OT_ie,
        TAPU_OT_oe,
        TAPU_OT_lon,
        TAPU_OT_lun,
        TAPU_OT_epz,
        TAPU_OT_ef1n,
        TAPU_OT_ef2n,
        TAPU_OT_ef2np,
        TAPU_OT_ef2nx)


def register():
    list(map(bpy.utils.register_class,classes))
    keymaps = bpy.context.window_manager.keyconfigs['Blender'].keymaps
    km = keymaps['Mesh'].keymap_items.new

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
    list(map(bpy.utils.unregister_class,classes))


