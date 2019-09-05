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
        "description": "Edge mode selection operators",
        "author":      "Shams Kitz <dustractor@gmail.com>",
        "version":     (5,4),
        "blender":     (2,80,0),
        "location":    "Mesh Tools, Edge Menu, and hotkeys in edge-select mode",
        "warning":     "",
        "tracker_url": "https://github.com/dustractor/tkit",
        "wiki_url":    "",
        "category":    "Mesh"
        }

import bpy
import bmesh


class TKIT_MT_menu(bpy.types.Menu):
    bl_label = "tkit ops"
    def draw(self,context):
        layout = self.layout
        layout.operator("tkit.ie")
        layout.operator("tkit.oe")
        layout.operator("tkit.lon")
        layout.operator("tkit.lun")
        layout.operator("tkit.epz")
        layout.operator("tkit.ef1n")
        layout.operator("tkit.ef2n")
        layout.operator("tkit.ef2np")
        layout.operator("tkit.ef2nx")

selected = lambda _: _.select
notselected = lambda _: not _.select
tagged = lambda _: _.tag
nottagged = lambda _: not _.tag


class TKIT_OT_lon(bpy.types.Operator):
    bl_idname = "tkit.lon"
    bl_label = "lon"
    bl_options = {"UNDO"}
    @classmethod
    def poll(self,context):
        return (context.active_object and
                context.active_object.type == 'MESH' and
                context.active_object.mode == 'EDIT' and
                context.scene.tool_settings.mesh_select_mode[1])
    def execute(self,context):
        bm = bmesh.from_edit_mesh(context.active_object.data)
        print(bm)
        for e in filter(selected,bm.edges):
            for v in e.verts:
                v.tag ^= 1
            for f in e.link_faces:
                f.tag = 1
        efs = {f.index for f in filter(tagged,bm.faces)}
        print("efs:",efs)
        for v in filter(tagged,bm.verts):
            v.tag = 0
            for e in filter(notselected,v.link_edges):
                e.tag = {f.index for f in e.link_faces}.isdisjoint(efs)
        for e in filter(tagged,bm.edges):
            e.tag = 0
            e.select_set(1)
            print("e:",e)
        for f in bm.faces:
            f.tag = 0
        bm.select_flush_mode()
        bmesh.update_edit_mesh(context.active_object.data,loop_triangles=False,destructive=False)
        context.area.tag_redraw()
        return {"FINISHED"}


class TKIT_OT_ie(bpy.types.Operator):
    bl_idname = "tkit.ie"
    bl_label = "ie"
    bl_options = {"UNDO"}
    @classmethod
    def poll(self,context):
        return (context.active_object and
                context.active_object.type == 'MESH' and
                context.active_object.mode == 'EDIT' and
                context.scene.tool_settings.mesh_select_mode[1])
    def execute(self,context):
        bm = bmesh.from_edit_mesh(context.active_object.data)
        for e in bm.edges:
            e.tag = len(list(filter(selected,e.link_faces))) == 1
        for e in filter(tagged,bm.edges):
            e.select_set(0)
            e.tag = 0
        bm.select_flush_mode()
        bmesh.update_edit_mesh(context.active_object.data,loop_triangles=False,destructive=False)
        context.area.tag_redraw()
        return {'FINISHED'}


class TKIT_OT_oe(bpy.types.Operator):
    bl_idname = "tkit.oe"
    bl_label = "oe"
    bl_options = {"UNDO"}
    @classmethod
    def poll(self,context):
        return (context.active_object and
                context.active_object.type == 'MESH' and
                context.active_object.mode == 'EDIT' and
                context.scene.tool_settings.mesh_select_mode[1])
    def execute(self,context):
        bm = bmesh.from_edit_mesh(context.active_object.data)
        for e in bm.edges:
            e.tag = len(list(filter(selected,e.link_faces))) == 2
        for e in filter(tagged,bm.edges):
            e.select_set(0)
            e.tag = 0
        bm.select_flush_mode()
        bmesh.update_edit_mesh(context.active_object.data,loop_triangles=False,destructive=False)
        context.area.tag_redraw()
        return {'FINISHED'}


class TKIT_OT_lun(bpy.types.Operator):
    bl_idname = "tkit.lun"
    bl_label = "lun"
    bl_options = {"UNDO"}
    @classmethod
    def poll(self,context):
        return (context.active_object and
                context.active_object.type == 'MESH' and
                context.active_object.mode == 'EDIT' and
                context.scene.tool_settings.mesh_select_mode[1])
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
        bmesh.update_edit_mesh(context.active_object.data,loop_triangles=False,destructive=False)
        context.area.tag_redraw()
        return {'FINISHED'}


class TKIT_OT_epz(bpy.types.Operator):
    bl_idname = "tkit.epz"
    bl_label = "epz"
    bl_options = {"UNDO"}
    @classmethod
    def poll(self,context):
        return (context.active_object and
                context.active_object.type == 'MESH' and
                context.active_object.mode == 'EDIT' and
                context.scene.tool_settings.mesh_select_mode[1])
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
        bmesh.update_edit_mesh(context.active_object.data,loop_triangles=False,destructive=False)
        context.area.tag_redraw()
        return {'FINISHED'}


class TKIT_OT_ef1n(bpy.types.Operator):
    bl_idname = "tkit.ef1n"
    bl_label = "ef1n"
    bl_options = {"UNDO"}
    @classmethod
    def poll(self,context):
        return (context.active_object and
                context.active_object.type == 'MESH' and
                context.active_object.mode == 'EDIT' and
                context.scene.tool_settings.mesh_select_mode[1])
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
        bmesh.update_edit_mesh(context.active_object.data,loop_triangles=False,destructive=False)
        context.area.tag_redraw()
        return {'FINISHED'}


class TKIT_OT_ef2n(bpy.types.Operator):
    bl_idname = "tkit.ef2n"
    bl_label = "ef2n"
    bl_options = {"UNDO"}
    @classmethod
    def poll(self,context):
        return (context.active_object and
                context.active_object.type == 'MESH' and
                context.active_object.mode == 'EDIT' and
                context.scene.tool_settings.mesh_select_mode[1])
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
        bmesh.update_edit_mesh(context.active_object.data,loop_triangles=False,destructive=False)
        context.area.tag_redraw()
        return {'FINISHED'}


class TKIT_OT_ef2np(bpy.types.Operator):
    bl_idname = "tkit.ef2np"
    bl_label = "ef2np"
    bl_options = {"UNDO"}
    @classmethod
    def poll(self,context):
        return (context.active_object and
                context.active_object.type == 'MESH' and
                context.active_object.mode == 'EDIT' and
                context.scene.tool_settings.mesh_select_mode[1])
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
        bmesh.update_edit_mesh(context.active_object.data,loop_triangles=False,destructive=False)
        context.area.tag_redraw()
        return {'FINISHED'}


class TKIT_OT_ef2nx(bpy.types.Operator):
    bl_idname = "tkit.ef2nx"
    bl_label = "ef2nx"
    bl_options = {"UNDO"}
    @classmethod
    def poll(self,context):
        return (context.active_object and
                context.active_object.type == 'MESH' and
                context.active_object.mode == 'EDIT' and
                context.scene.tool_settings.mesh_select_mode[1])
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
        bmesh.update_edit_mesh(context.active_object.data,loop_triangles=False,destructive=False)
        context.area.tag_redraw()
        return {'FINISHED'}


km = None
kmis = []

def register():
    global km
    kmis.clear()
    bpy.utils.register_class(TKIT_OT_ie)
    bpy.utils.register_class(TKIT_OT_oe)
    bpy.utils.register_class(TKIT_OT_lon)
    bpy.utils.register_class(TKIT_OT_lun)
    bpy.utils.register_class(TKIT_OT_epz)
    bpy.utils.register_class(TKIT_OT_ef1n)
    bpy.utils.register_class(TKIT_OT_ef2n)
    bpy.utils.register_class(TKIT_OT_ef2np)
    bpy.utils.register_class(TKIT_OT_ef2nx)
    bpy.utils.register_class(TKIT_MT_menu)
    bpy.types.VIEW3D_MT_select_edit_mesh.append(lambda s,c:s.layout.menu("TKIT_MT_menu"))
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if kc:
        km = kc.keymaps.new("Mesh",space_type="EMPTY")
        kmis.append(km.keymap_items.new("tkit.ie",type="QUOTE",value="PRESS"))
        kmis.append(km.keymap_items.new("tkit.oe",type="QUOTE",shift=True,value="PRESS"))
        kmis.append(km.keymap_items.new("tkit.lon",type="RIGHT_BRACKET",value="PRESS"))
        kmis.append(km.keymap_items.new("tkit.lun",type="LEFT_BRACKET",value="PRESS"))
        kmis.append(km.keymap_items.new("tkit.epz",type="END",ctrl=True,alt=True,shift=True,value="PRESS"))
        kmis.append(km.keymap_items.new("tkit.ef1n",type="BACK_SLASH",value="PRESS"))
        kmis.append(km.keymap_items.new("tkit.ef2n",type="BACK_SLASH",shift=True,value="PRESS"))
        kmis.append(km.keymap_items.new("tkit.ef2np",type="BACK_SLASH",ctrl=True,shift=True,value="PRESS"))
        kmis.append(km.keymap_items.new("tkit.ef2nx",type="BACK_SLASH",alt=True,ctrl=True,shift=True,value="PRESS"))

def unregister():
    for kmi in kmis:
        km.keymap_items.remove(kmi)
    bpy.utils.unregister_class(TKIT_MT_menu)
    bpy.utils.unregister_class(TKIT_OT_ie)
    bpy.utils.unregister_class(TKIT_OT_oe)
    bpy.utils.unregister_class(TKIT_OT_lon)
    bpy.utils.unregister_class(TKIT_OT_lun)
    bpy.utils.unregister_class(TKIT_OT_epz)
    bpy.utils.unregister_class(TKIT_OT_ef1n)
    bpy.utils.unregister_class(TKIT_OT_ef2n)
    bpy.utils.unregister_class(TKIT_OT_ef2np)
    bpy.utils.unregister_class(TKIT_OT_ef2nx)

