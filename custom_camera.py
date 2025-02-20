bl_info = {
    "name": "Custom Camera",
    "author": "Dave Nectariad Rome",
    "version": (0, 3, 8),
    "blender": (4, 0, 0),
    "location": "View3D > Tool Shelf > Custom Camera Add-on",
    "description": "Add a custom camera setup",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

import bpy
from bpy.props import EnumProperty, FloatProperty, StringProperty, BoolProperty, IntProperty
from bpy_extras.io_utils import ImportHelper
from mathutils import Vector
import urllib.request
import os
import subprocess

# Central source for all camera presets
CAMERA_PRESETS = {
    "1_INCH": {"name": "1 inch", "dimensions": (13.2, 8.8)},
    "1_1_8_INCH": {"name": "1/1.8 inch", "dimensions": (7.6, 5.7)},
    "1_2_3_INCH": {"name": "1/2.3 inch", "dimensions": (6.17, 4.55)},
    "1_2_5_INCH": {"name": "1/2.5 inch", "dimensions": (5.76, 4.29)},
    "1_2_7_INCH": {"name": "1/2.7 inch", "dimensions": (5.37, 4.04)},
    "1_3_2_INCH": {"name": "1/3.2 inch", "dimensions": (4.54, 3.42)},
    "2_3_INCH": {"name": "2/3 inch", "dimensions": (8.8, 6.6)},
    "ANALOG_16MM": {"name": "Analog 16mm", "dimensions": (10.26, 7.49)},
    "ANALOG_35MM": {"name": "Analog 35mm", "dimensions": (36, 24)},
    "ANALOG_65MM": {"name": "Analog 65mm", "dimensions": (52.48, 23.01)},
    "ANALOG_IMAX": {"name": "Analog IMAX", "dimensions": (69.6, 48.5)},
    "ANALOG_SUPER_16": {"name": "Analog Super 16", "dimensions": (12.52, 7.41)},
    "ANALOG_SUPER_35": {"name": "Analog Super 35", "dimensions": (24.89, 18.66)},
    "APS_C": {"name": "APS-C", "dimensions": (23.5, 15.6)},
    "APS_C_CANON": {"name": "APS-C (Canon)", "dimensions": (22.2, 14.8)},
    "APS_H_CANON": {"name": "APS-H (Canon)", "dimensions": (27.9, 18.6)},
    "ARRI_ALEXA_65": {"name": "Arri Alexa 65", "dimensions": (54.12, 25.58)},
    "ARRI_ALEXA_LF": {"name": "Arri Alexa LF", "dimensions": (36.70, 25.54)},
    "ARRI_ALEXA_MINI_SXT": {"name": "Arri Alexa Mini & SXT", "dimensions": (28.25, 18.17)},
    "BLACKMAGIC_POCKET_4K": {"name": "Blackmagic Pocket 4K", "dimensions": (18.96, 10)},
    "BLACKMAGIC_POCKET_6K": {"name": "Blackmagic Pocket 6K", "dimensions": (23.10, 12.99)},
    "BLACKMAGIC_POCKET_STUDIO": {"name": "Blackmagic Pocket & Studio", "dimensions": (13.056, 7.344)},
    "BLACKMAGIC_URSA_4_6K": {"name": "Blackmagic URSA 4.6K", "dimensions": (25.34, 14.25)},
    "FOVEON_SIGMA": {"name": "Foveon (Sigma)", "dimensions": (23.5, 15.7)},
    "FULLFRAME": {"name": "Fullframe", "dimensions": (36, 24)},
    "MEDIUM_FORMAT_HASSELBLAD": {"name": "Medium-format (Hasselblad)", "dimensions": (43.8, 32.9)},
    "MFT": {"name": "MFT", "dimensions": (17.3, 13)},
    "RED_DRAGON_5K": {"name": "RED Dragon 5K", "dimensions": (28.192, 15.48)},
    "RED_DRAGON_6K": {"name": "RED Dragon 6K", "dimensions": (30.7, 15.8)},
    "RED_HELIUM_8K": {"name": "RED Helium 8K", "dimensions": (29.90, 15.77)},
    "RED_MONSTRO_8K": {"name": "RED Monstro 8K", "dimensions": (40.96, 21.60)},
}

def update_camera_settings(self, context):
    props = context.scene.custom_camera_props
    camera_object = bpy.data.objects.get("CustomCamera")
    
    if camera_object and camera_object.type == 'CAMERA':
        camera_data = camera_object.data

        # Update sensor size
        if props.sensor_size != "CUSTOM":
            width, height = CAMERA_PRESETS[props.sensor_size]["dimensions"]
            camera_data.sensor_width = width
            camera_data.sensor_height = height
        else:
            camera_data.sensor_width = props.custom_sensor_width
            camera_data.sensor_height = props.custom_sensor_height

        # Update focal length
        camera_data.lens = float(props.focal_length.rstrip("mm")) if props.focal_length != "CUSTOM" else props.custom_focal_length

        # Handle DOF settings
        if props.use_depth_of_field:
            dof_target_object = bpy.data.objects.get("DOF_target")
            if not dof_target_object:
                dof_target_object = bpy.data.objects.new("DOF_target", None)
                bpy.data.collections.get("Camera Collection").objects.link(dof_target_object)
                dof_target_object.location = Vector((0, 0, 0))
            camera_data.dof.focus_object = dof_target_object
            dof_target_object.location = camera_object.location + camera_object.matrix_world.to_quaternion() @ Vector((0.0, 0.0, -props.dof_target_distance))
        else:
            dof_target_object = bpy.data.objects.get("DOF_target")
            if dof_target_object:
                bpy.data.objects.remove(dof_target_object)

        # Update DOF and aperture settings
        camera_data.dof.use_dof = props.use_depth_of_field
        if props.aperture_size != "CUSTOM":
            aperture_size_float = float(props.aperture_size.split("f/")[-1])
            camera_data.dof.aperture_fstop = aperture_size_float
        else:
            camera_data.dof.aperture_fstop = props.custom_aperture_size

        # Set bokeh shape
        bokeh_blades = {
            "CIRCULAR": 0,
            "TRIANGLE": 3,
            "SQUARE": 4,
            "PENTAGON": 5,
            "HEXAGONAL": 6,
            "OCTAGONAL": 8,
            "ANAMORPHIC": 100,
        }
        
        if props.bokeh_shape == "CUSTOM":
            camera_data.dof.aperture_blades = int(props.custom_bokeh_size * 10)
        else:
            camera_data.dof.aperture_blades = bokeh_blades[props.bokeh_shape]
            camera_data.dof.aperture_ratio = 2.0 if props.bokeh_shape == "ANAMORPHIC" else 1.0

        # Update resolution
        context.scene.render.resolution_x = props.resolution_x
        context.scene.render.resolution_y = props.resolution_y

        # Handle camera target
        if props.cam_target:
            camera_object.constraints.clear()
            track_constraint = camera_object.constraints.new(type='TRACK_TO')
            track_constraint.target = props.cam_target
            track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
            track_constraint.up_axis = 'UP_Y'
class CustomCameraPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        layout.operator("customcamera.update_custom_camera", text="Update Custom Camera")
        layout.operator("wm.url_open", text="Visit GitHub Repository").url = "https://github.com/mdreece/Custom-Camera-Blender-Add-on"
        
class CUSTOMCAMERA_OT_open_preferences(bpy.types.Operator):
    bl_idname = "customcamera.open_preferences"
    bl_label = ""
    bl_description = "Open the Custom Camera add-on preferences"
    
    def execute(self, context):
        bpy.ops.screen.userpref_show('INVOKE_DEFAULT')
        bpy.context.preferences.active_section = 'ADDONS'
        bpy.context.window_manager.addon_search = "Custom Camera"
        return {'FINISHED'}

class UPDATE_CUSTOMCAMERA_OT_update_custom_camera(bpy.types.Operator):
    bl_idname = "customcamera.update_custom_camera"
    bl_label = "Update Custom Camera"
    bl_description = "Update the Custom Camera add-on with the latest version from GitHub"

    def execute(self, context):
        update_custom_camera(self, context)
        return {"FINISHED"}
        
class CustomCameraProperties(bpy.types.PropertyGroup):
    sensor_size: EnumProperty(
        name="Sensor Size",
        items=[(key, preset["name"], f"Set sensor size to {preset['name']}") 
               for key, preset in CAMERA_PRESETS.items()] + 
              [("CUSTOM", "Custom", "Use custom sensor dimensions")],
        default="FULLFRAME",
        update=update_camera_settings,
    )

    focal_lengths = [
        ("18mm", "18mm", ""),
        ("24mm", "24mm", ""),
        ("35mm", "35mm", ""),
        ("50mm", "50mm", ""),
        ("85mm", "85mm", ""),
        ("135mm", "135mm", ""),
        ("CUSTOM", "Custom", ""),
    ]

    focal_length: EnumProperty(
        name="Focal Length",
        items=focal_lengths,
        default="50mm",
        update=update_camera_settings,
    )

    custom_sensor_width: FloatProperty(
        name="Sensor Width",
        description="Set custom sensor width in millimeters",
        default=35.0,
        min=1.0,
        update=update_camera_settings,
    )
    
    custom_sensor_height: FloatProperty(
        name="Sensor Height",
        description="Set custom sensor height in millimeters",
        default=24.0,
        min=1.0,
        update=update_camera_settings,
    )

    custom_focal_length: FloatProperty(
        name="Custom Focal Length",
        description="Set custom focal length in millimeters",
        default=50.0,
        min=1.0,
        update=update_camera_settings,
    )

    resolution_x: IntProperty(
        name="Resolution X",
        description="X resolution of the camera",
        default=1920,
        min=1,
        update=update_camera_settings,
    )

    resolution_x: IntProperty(
        name="Resolution X",
        description="X resolution of the camera",
        default=1920,
        min=1,
        update=update_camera_settings,
    )

    resolution_y: IntProperty(
        name="Resolution Y",
        description="Y resolution of the camera",
        default=1080,
        min=1,
        update=update_camera_settings,
    )

    use_depth_of_field: BoolProperty(
        name="Use Depth of Field",
        description="Enable or disable depth of field",
        default=False,
        update=update_camera_settings,
    )

    dof_target_distance: FloatProperty(
        name="DOF Target Distance",
        description="Set distance of the DOF target empty",
        default=5.0,
        min=0.0,
        update=update_camera_settings,
    )

    aperture_sizes = [
        ("0.5", "f/0.5", ""),
        ("1.0", "f/1.0", ""),
        ("1.4", "f/1.4", ""),
        ("2.0", "f/2.0", ""),
        ("2.8", "f/2.8", ""),
        ("4.0", "f/4.0", ""),
        ("5.6", "f/5.6", ""),
        ("8.0", "f/8.0", ""),
        ("11", "f/11", ""),
        ("16", "f/16", ""),
        ("22", "f/22", ""),
        ("32", "f/32", ""),
        ("45", "f/45", ""),
        ("64", "f/64", ""),
        ("90", "f/90", ""),
        ("CUSTOM", "Custom", ""),
    ]

    aperture_size: EnumProperty(
        name="Aperture Size",
        items=aperture_sizes,
        default="2.8",
        update=update_camera_settings,
    )

    custom_aperture_size: FloatProperty(
        name="Custom Aperture Size",
        description="Set custom aperture size",
        default=2.8,
        min=0.5,
        max=90.0,
        update=update_camera_settings,
    )

    bokeh_shapes = [
        ("CIRCULAR", "Circular", ""),
        ("TRIANGLE", "Triangle", ""),
        ("SQUARE", "Square", ""),
        ("PENTAGON", "Pentagon", ""),
        ("HEXAGONAL", "Hexagonal", ""),
        ("OCTAGONAL", "Octagonal", ""),
        ("ANAMORPHIC", "Anamorphic", ""),
        ("CUSTOM", "Custom", ""),
    ]

    bokeh_shape: EnumProperty(
        name="Bokeh Shape",
        items=bokeh_shapes,
        default="CIRCULAR",
        update=update_camera_settings,
    )

    custom_bokeh_size: FloatProperty(
        name="Custom Bokeh Size",
        description="Set custom bokeh size",
        default=0.1,
        min=0.0,
        max=1.0,
        update=update_camera_settings,
    )

    camera_collection_selected: BoolProperty(
        name="Camera Collection Selected",
        description="Whether the camera collection is selected",
        default=False,
    )

    dof_target: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="DOF Target",
        description="Object for Depth of Field",
    )

    cam_target: bpy.props.PointerProperty(
        type=bpy.types.Object,
        name="Camera Target",
        description="Object for Camera Target",
    )

class CUSTOMCAMERA_OT_select_camera_collection(bpy.types.Operator):
    bl_idname = "customcamera.select_camera_collection"
    bl_label = "Select Camera Collection"
    bl_description = "Select all objects in the Camera Collection"

    def execute(self, context):
        camera_collection = bpy.data.collections.get("Camera Collection")
        props = context.scene.custom_camera_props

        if camera_collection:
            bpy.ops.object.select_all(action='DESELECT')
            
            for obj in camera_collection.objects:
                obj.select_set(True)

            props.camera_collection_selected = True

            # Update mesh select mode
            bpy.context.scene.tool_settings.mesh_select_mode[:] = (False, False, False)
            bpy.context.scene.tool_settings.mesh_select_mode[:] = (True, True, True)
            bpy.context.scene.tool_settings.use_mesh_automerge = True

        else:
            self.report({'WARNING'}, "Camera Collection not found")
            props.camera_collection_selected = False

        return {'FINISHED'}

class CUSTOMCAMERA_OT_deselect_camera_collection(bpy.types.Operator):
    bl_idname = "customcamera.deselect_camera_collection"
    bl_label = "Deselect Camera Collection"
    bl_description = "Deselect all objects in the Camera Collection"

    def execute(self, context):
        camera_collection = bpy.data.collections.get("Camera Collection")
        props = context.scene.custom_camera_props

        if camera_collection:
            for obj in camera_collection.objects:
                obj.select_set(False)
            props.camera_collection_selected = False

            # Reset mesh select mode
            bpy.context.scene.tool_settings.mesh_select_mode[:] = (True, True, True)
            bpy.context.scene.tool_settings.use_mesh_automerge = False

        else:
            self.report({'WARNING'}, "Camera Collection not found")

        return {'FINISHED'}

class CUSTOMCAMERA_PT_main_panel(bpy.types.Panel):
    bl_label = "Custom Camera"
    bl_idname = "CUSTOMCAMERA_PT_main_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Custom Camera"

    def draw(self, context):
        layout = self.layout
        props = context.scene.custom_camera_props

        # Camera Creation/Management
        if not bpy.data.objects.get("CustomCamera"):
            # When no camera exists, show create and preferences buttons side by side
            row = layout.row(align=True)
            row.scale_y = 1.35
            row.operator("customcamera.create_camera", text="Create Camera", icon='ADD')
            row.operator("customcamera.open_preferences", text="", icon='PREFERENCES')
            return

        # Camera Settings UI
        quick_box = layout.box()
        quick_box.label(text="Quick Settings", icon='SETTINGS')
        row = quick_box.row()
        row.prop(props, "sensor_size", text="")
        
        row = quick_box.row(align=True)
        sub = row.row(align=True)
        sub.prop(props, "resolution_x", text="")
        sub.label(text="x")
        sub.prop(props, "resolution_y", text="")
        quick_box.prop(props, "focal_length", text="Lens")
        
        if props.sensor_size == "CUSTOM" or props.focal_length == "CUSTOM":
            custom_box = quick_box.box()
            custom_box.label(text="Custom Values", icon='MODIFIER')
            if props.sensor_size == "CUSTOM":
                col = custom_box.column(align=True)
                col.prop(props, "custom_sensor_width")
                col.prop(props, "custom_sensor_height")
            if props.focal_length == "CUSTOM":
                custom_box.prop(props, "custom_focal_length")

        # Depth of Field Compact Box
        dof_box = layout.box()
        row = dof_box.row()
        row.prop(props, "use_depth_of_field", text="")
        sub = row.row()
        sub.active = props.use_depth_of_field
        sub.label(text="Depth of Field", icon='CAMERA_DATA')
        
        if props.use_depth_of_field:
            col = dof_box.column(align=True)
            
            # Distance and target
            flow = col.grid_flow(row_major=True, columns=2, even_columns=True)
            flow.prop(props, "dof_target_distance", text="Distance")
            flow.prop(props, "cam_target", text="")
            
            # Bokeh settings in a sub-box
            bokeh_box = dof_box.box()
            bokeh_box.label(text="Bokeh Settings", icon='LIGHT')
            
            # Bokeh shape and aperture in two columns
            row = bokeh_box.row()
            left_col = row.column()
            right_col = row.column()
            
            left_col.prop(props, "bokeh_shape", text="")
            if props.bokeh_shape == "CUSTOM":
                left_col.prop(props, "custom_bokeh_size", text="Size")
                
            right_col.prop(props, "aperture_size", text="")
            if props.aperture_size == "CUSTOM":
                right_col.prop(props, "custom_aperture_size", text="f/")

        # Camera Collection Box
        collection_box = layout.box()
        collection_box.label(text="Collection Management", icon='OUTLINER')
        
        if bpy.data.collections.get("Camera Collection"):
            row = collection_box.row()
            if props.camera_collection_selected:
                row.operator("customcamera.deselect_camera_collection", 
                           text="Deselect Collection", 
                           icon='RESTRICT_SELECT_ON')
            else:
                row.operator("customcamera.select_camera_collection", 
                           text="Select Collection", 
                           icon='RESTRICT_SELECT_OFF')

        # Advanced Settings (collapsible)
        advanced_box = layout.box()
        row = advanced_box.row()
        row.prop(props, "camera_collection_selected", 
                text="", 
                icon='TRIA_DOWN' if props.camera_collection_selected else 'TRIA_RIGHT',
                emboss=False)
        row.label(text="Advanced Settings", icon='PREFERENCES')
        
        if props.camera_collection_selected:
            col = advanced_box.column(align=True)
            row = col.row(align=True)
            row.operator("view3d.view_camera", text="View Through Camera", icon='CAMERA_DATA')
            row.operator("view3d.camera_to_view", text="Camera to View", icon='VIEW_CAMERA')

        # Info footer
        footer = layout.box()
        footer.scale_y = 0.6
        footer.label(text="Camera Info:", icon='INFO')
        if props.cam_target:
            footer.label(text=f"Target: {props.cam_target.name}")
        row = footer.row()
        row.label(text=f"Sensor: {props.sensor_size}")
        row.label(text=f"Lens: {props.focal_length}")

        # Delete and Preferences buttons side by side
        layout.separator()
        row = layout.row(align=True)
        row.scale_y = 1.2
        delete_sub = row.row()
        delete_sub.alert = True
        delete_sub.operator("customcamera.delete_camera", text="Remove Camera", icon='TRASH')
        row.operator("customcamera.open_preferences", text="", icon='PREFERENCES')

class CUSTOMCAMERA_OT_create_camera(bpy.types.Operator):
    bl_idname = "customcamera.create_camera"
    bl_label = "Create Custom Camera"
    bl_description = "Create a camera with custom settings"

    def execute(self, context):
        props = context.scene.custom_camera_props

        # Create camera collection
        camera_collection = bpy.data.collections.new("Camera Collection")
        bpy.context.scene.collection.children.link(camera_collection)

        # Create camera
        camera_data = bpy.data.cameras.new("CustomCamera")
        camera_object = bpy.data.objects.new("CustomCamera", camera_data)
        camera_collection.objects.link(camera_object)
        
        # Set initial camera position
        camera_object.location = (6.5, -6.5, 4.0)
        
        # Create target empty
        cam_target_object = bpy.data.objects.new("CAM_target", None)
        camera_collection.objects.link(cam_target_object)
        cam_target_object.location = Vector((0, 0, 0))
        
        # Setup track constraint
        track_constraint = camera_object.constraints.new(type='TRACK_TO')
        track_constraint.target = cam_target_object
        track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
        track_constraint.up_axis = 'UP_Y'
        
        # Set target in properties
        props.cam_target = cam_target_object

        # Update all camera settings
        update_camera_settings(self, context)

        return {'FINISHED'}

class CUSTOMCAMERA_OT_delete_camera(bpy.types.Operator):
    bl_idname = "customcamera.delete_camera"
    bl_label = "Delete Camera"
    bl_description = "Delete the custom camera"

    def execute(self, context):
        custom_camera = bpy.data.objects.get("CustomCamera")
        if custom_camera:
            # Disable DOF before deletion
            context.scene.custom_camera_props.use_depth_of_field = False
            
            # Remove camera and related objects
            bpy.data.objects.remove(custom_camera, do_unlink=True)
            cam_target = bpy.data.objects.get("CAM_target")
            if cam_target:
                bpy.data.objects.remove(cam_target, do_unlink=True)
            
            # Remove collection
            collection = bpy.data.collections.get("Camera Collection")
            if collection:
                bpy.data.collections.remove(collection, do_unlink=True)
            
            # Clear property references
            context.scene.custom_camera_props.dof_target = None
            context.scene.custom_camera_props.cam_target = None
            
        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_confirm(self, event)

def register():
    bpy.utils.register_class(CustomCameraProperties)
    bpy.types.Scene.custom_camera_props = bpy.props.PointerProperty(type=CustomCameraProperties)
    bpy.utils.register_class(CUSTOMCAMERA_PT_main_panel)
    bpy.utils.register_class(CUSTOMCAMERA_OT_create_camera)
    bpy.utils.register_class(CUSTOMCAMERA_OT_delete_camera)
    bpy.utils.register_class(CUSTOMCAMERA_OT_select_camera_collection)
    bpy.utils.register_class(CUSTOMCAMERA_OT_deselect_camera_collection)
    bpy.utils.register_class(UPDATE_CUSTOMCAMERA_OT_update_custom_camera)
    bpy.utils.register_class(CustomCameraPreferences)
    bpy.utils.register_class(CUSTOMCAMERA_OT_open_preferences)

def unregister():
    bpy.utils.unregister_class(CustomCameraProperties)
    del bpy.types.Scene.custom_camera_props
    bpy.utils.unregister_class(CUSTOMCAMERA_PT_main_panel)
    bpy.utils.unregister_class(CUSTOMCAMERA_OT_create_camera)
    bpy.utils.unregister_class(CUSTOMCAMERA_OT_delete_camera)
    bpy.utils.unregister_class(CUSTOMCAMERA_OT_select_camera_collection)
    bpy.utils.unregister_class(CUSTOMCAMERA_OT_deselect_camera_collection)
    bpy.utils.unregister_class(UPDATE_CUSTOMCAMERA_OT_update_custom_camera)
    bpy.utils.unregister_class(CustomCameraPreferences)
    bpy.utils.unregister_class(CUSTOMCAMERA_OT_open_preferences)

if __name__ == "__main__":
    register()
