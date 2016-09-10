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
        "description": "edgemode select ops plus hotkeys",
        "author":      "Shams Kitz <dustractor@gmail.com>",
        "version":     (5,1),
        "blender":     (2,78,0),
        "location":    "Mesh Edit Tools Panel and <C-e> Edge Menu",
        "warning":     "",
        "tracker_url": "https://github.com/dustractor/tkit",
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


classes = (
        TKIT_OT_ie,
        TKIT_OT_oe,
        TKIT_OT_lon,
        TKIT_OT_lun,
        TKIT_OT_epz,
        TKIT_OT_ef1n,
        TKIT_OT_ef2n,
        TKIT_OT_ef2np,
        TKIT_OT_ef2nx)

class tkitmenu(bpy.types.Menu):
    bl_idname = "tkit.menu"
    bl_label = "tkit"
    def draw(self,context):
        if EdgeSelectMode.poll(context):
            box = self.layout.box()
            col = box.column(align=True)
            for c in classes:
                col.operator(c.bl_idname)

def tkit_menudraw(self,context):
    self.layout.menu("tkit.menu")

def register():
    bpy.utils.register_module(__name__)
    bpy.types.VIEW3D_MT_edit_mesh_edges.append(tkit_menudraw)
    bpy.types.VIEW3D_PT_tools_meshedit.append(tkitmenu.draw)

def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_edges.remove(tkit_menudraw)
    bpy.types.VIEW3D_PT_tools_meshedit.remove(tkitmenu.draw)
    bpy.utils.unregister_module(__name__)

