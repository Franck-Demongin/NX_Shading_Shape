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
from mathutils import Matrix

class Viewport_OT_shading_shape(bpy.types.Operator):
    """Update viewport shading to see only shape"""
    bl_idname = "viewport.shading_shape"
    bl_label = "Shading Shape"
    
    def flatten(self, mat):
        dim = len(mat)
        return [mat[j][i] for i in range(dim) 
                        for j in range(dim)]

    def execute(self, context):

        area = context.screen.areas[context.screen.nx_shading_shape.area_idx]
        if area.type == 'VIEW_3D':
            space = area.spaces[0]
            context.screen.nx_shading_shape.shading_type = space.shading.type
            context.screen.nx_shading_shape.shading_light = space.shading.light
            context.screen.nx_shading_shape.shading_single_color = space.shading.single_color
            context.screen.nx_shading_shape.shading_color_type = space.shading.color_type
            context.screen.nx_shading_shape.shading_background_color = space.shading.background_color
            context.screen.nx_shading_shape.shading_background_type = space.shading.background_type
            context.screen.nx_shading_shape.show_region_ui = space.show_region_ui
            context.screen.nx_shading_shape.show_region_toolbar = space.show_region_toolbar
            context.screen.nx_shading_shape.show_overlays = space.overlay.show_overlays
            context.screen.nx_shading_shape.show_gizmo = space.show_gizmo
            context.screen.nx_shading_shape.view_perspective = space.region_3d.view_perspective
            context.screen.nx_shading_shape.view_matrix = self.flatten(space.region_3d.view_matrix.copy())

        area.type = 'VIEW_3D'

        space = area.spaces[0]        
        space.shading.type = "SOLID"
        space.shading.light = "FLAT"
        space.shading.single_color = (0, 0, 0)
        space.shading.color_type = 'SINGLE'
        space.shading.background_color = (1, 1, 1)
        space.shading.background_type = 'VIEWPORT'
        space.show_region_ui = False
        space.show_region_toolbar = False
        space.overlay.show_overlays = False
        space.show_gizmo = False
        space.region_3d.view_perspective = 'CAMERA'
                
        return {'FINISHED'}
    
    def reset_area(self, context):    
        area = context.screen.areas[context.screen.nx_shading_shape.area_idx]

        if context.screen.nx_shading_shape.area_type == 'VIEW_3D':
            space = area.spaces[0]
            space.shading.type = context.screen.nx_shading_shape.shading_type
            space.shading.light = context.screen.nx_shading_shape.shading_light
            space.shading.single_color = context.screen.nx_shading_shape.shading_single_color
            space.shading.color_type = context.screen.nx_shading_shape.shading_color_type
            space.shading.background_color = context.screen.nx_shading_shape.shading_background_color
            space.shading.background_type = context.screen.nx_shading_shape.shading_background_type
            space.show_region_ui = context.screen.nx_shading_shape.show_region_ui
            space.show_region_toolbar = context.screen.nx_shading_shape.show_region_toolbar
            space.overlay.show_overlays = context.screen.nx_shading_shape.show_overlays
            space.show_gizmo = context.screen.nx_shading_shape.show_gizmo
            space.region_3d.view_perspective = context.screen.nx_shading_shape.view_perspective
            space.region_3d.view_matrix = context.screen.nx_shading_shape.view_matrix


        area.type = context.screen.nx_shading_shape.area_type

    
    def modal(self, context, event):
        if context.screen.nx_shading_shape.area_active:
            context.screen.nx_shading_shape.area_active = False
            self.reset_area(context)
            return {'FINISHED'}

        elif event.type == 'LEFTMOUSE' and event.value == 'RELEASE':
            context.screen.nx_shading_shape.area_active = True
            for idx, area in enumerate(context.screen.areas.items()):
                if (event.mouse_x > area[1].x and event.mouse_x < area[1].x + area[1].width and
                    event.mouse_y > area[1].y and event.mouse_y < area[1].y + area[1].height):
                    context.screen.nx_shading_shape.area_type = area[1].type
                    context.screen.nx_shading_shape.area_idx = idx
                    break

            self.execute(context)            
            return {'FINISHED'}

        elif event.type in {'RIGHTMOUSE', 'ESC'}:  # Cancel
            return {'CANCELLED'}

        return {'RUNNING_MODAL'}
    
    def invoke(self, context, event):
        context.window_manager.modal_handler_add(self)
        return {'RUNNING_MODAL'}


class MyPropertyGroup(bpy.types.PropertyGroup):
    area_type: bpy.props.StringProperty()
    area_idx: bpy.props.IntProperty(default = -1)
    area_active: bpy.props.BoolProperty(default = False)
    shading_type: bpy.props.StringProperty()
    shading_light: bpy.props.StringProperty()
    shading_single_color: bpy.props.FloatVectorProperty()
    shading_color_type: bpy.props.StringProperty()
    shading_background_color: bpy.props.FloatVectorProperty()
    shading_background_type: bpy.props.StringProperty()
    show_region_ui: bpy.props.BoolProperty()
    show_region_toolbar: bpy.props.BoolProperty()
    show_overlays: bpy.props.BoolProperty() 
    show_gizmo: bpy.props.BoolProperty()
    view_perspective: bpy.props.StringProperty()
    view_matrix: bpy.props.FloatVectorProperty(
        size=16,
        subtype="MATRIX"
    )
    

bpy.utils.register_class(MyPropertyGroup)

def menu_func(self, context):
    label = 'Activate Shading shape'
    if context.screen.nx_shading_shape.area_active:
        label = 'Deactivate Shading shape'
    self.layout.operator('viewport.shading_shape', text=label, icon='SHAPEKEY_DATA')

def register():
    bpy.utils.register_class(Viewport_OT_shading_shape)
    bpy.types.VIEW3D_PT_shading.append(menu_func)
    bpy.types.Screen.nx_shading_shape = bpy.props.PointerProperty(type=MyPropertyGroup)


def unregister():
    bpy.utils.unregister_class(Viewport_OT_shading_shape)
    bpy.types.VIEW3D_PT_shading.remove(menu_func)
    del bpy.types.Screen.nx_shading_shape

if __name__ == "__main__":
    register()