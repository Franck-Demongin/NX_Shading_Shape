# ##### BEGIN GPL LICENSE BLOCK #####
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTIBILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# ##### END GPL LICENSE BLOCK #####

bl_info = {
    "name": "Shading Shape",
    "author": "Franck Demongin",
    "version": (1, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Shading",
    "description": "Display shape of the objects",
    "category": "3D View",
}

import bpy

class Viewport_OT_shading_shape(bpy.types.Operator):
    """Update viewport shading to see only shape"""
    bl_idname = "viewport.shading_shape"
    bl_label = "Shading Shape"
    
    def execute(self, context):
        
        context.space_data.shading.type = "SOLID"
        context.space_data.shading.light = "FLAT"
        context.space_data.shading.single_color = (0, 0, 0)
        context.space_data.shading.color_type = 'SINGLE'
        context.space_data.shading.background_color = (1, 1, 1)
        context.space_data.shading.background_type = 'VIEWPORT'
        context.space_data.show_region_ui = False
        context.space_data.show_region_toolbar = False
        context.space_data.overlay.show_overlays = False
        context.space_data.show_gizmo = False
        context.region_data.view_perspective = 'CAMERA'
                
        return {'FINISHED'}
    
    def modal(self, context, event):
        if event.type == 'LEFTMOUSE':  # Confirm
            print(event)
            self.execute(context)
            return {'FINISHED'}
        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancel
            context.object.location.x = self.init_loc_x
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}
    
    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}

def menu_func(self, context):
    self.layout.operator('viewport.shading_shape', text='Shading Shape', icon='SHAPEKEY_DATA')

def register():
    bpy.utils.register_class(Viewport_OT_shading_shape)
    bpy.types.VIEW3D_PT_shading.append(menu_func)

def unregister():
    bpy.utils.unregister_class(Viewport_OT_shading_shape)
    bpy.types.VIEW3D_PT_shading.remove(menu_func)

if __name__ == "__main__":
    register()