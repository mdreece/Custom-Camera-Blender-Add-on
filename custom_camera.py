bl_info = {
    "name": "Custom Camera",
    "author": "Dave Nectariad Rome",
    "version": (0, 3, 7),
    "blender": (3, 50, 1),
    "location": "View3D > Tool Shelf > Custom Camera Add-on",
    "description": "Add a custom camera setup",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

from mathutils import Vector
import bpy
from bpy.props import EnumProperty, FloatProperty, StringProperty, BoolProperty, IntProperty
from bpy_extras.io_utils import ImportHelper
import urllib.request
import os
import subprocess

def update_camera_settings(self, context):
    props = context.scene.custom_camera_props

    camera_object = bpy.data.objects.get("CustomCamera")
    if camera_object and camera_object.type == 'CAMERA':
        camera_data = camera_object.data

        camera_data.sensor_width = float(props.sensor_size) if props.sensor_size != "CUSTOM" else props.custom_sensor_size
        camera_data.lens = float(props.focal_length.rstrip("mm")) if props.focal_length != "CUSTOM" else props.custom_focal_length

        if props.use_depth_of_field:
            dof_target_object = bpy.data.objects.get("DOF_target")
            if not dof_target_object:
                # Create DOF_target object if it doesn't exist
                dof_target_object = bpy.data.objects.new("DOF_target", None)
                bpy.data.collections.get("Camera Collection").objects.link(dof_target_object)
                dof_target_object.location = Vector((0, 0, 0))
            camera_data.dof.focus_object = dof_target_object

            # Set the distance of the DOF target empty
            dof_target_object.location = camera_object.location + camera_object.matrix_world.to_quaternion() @ Vector((0.0, 0.0, -props.dof_target_distance))
        else:
            # Remove DOF_target object if it exists
            dof_target_object = bpy.data.objects.get("DOF_target")
            if dof_target_object:
                bpy.data.objects.remove(dof_target_object)

        camera_data.dof.use_dof = props.use_depth_of_field
        camera_data.dof.aperture_fstop = float(props.aperture_size) if props.aperture_size != "CUSTOM" else props.custom_aperture_size

        if props.bokeh_shape == "CUSTOM":
            camera_data.dof.aperture_blades = int(props.custom_bokeh_size * 10)
        else:
            camera_data.dof.aperture_blades = {
                "CIRCULAR": 0,
                "TRIANGLE": 3,
                "SQUARE": 4,
                "PENTAGON": 5,
                "HEXAGONAL": 6,
                "OCTAGONAL": 8,
                "ANAMORPHIC": 100, # Value to be replaced later
            }[props.bokeh_shape]

        # Convert aperture size to a float
        if props.bokeh_shape == "ANAMORPHIC":
            camera_data.dof.aperture_blades = 100
            camera_data.dof.aperture_ratio = 2.0
        else:
            camera_data.dof.aperture_ratio = 1.0
        if props.aperture_size != "CUSTOM":
            aperture_size_float = float(props.aperture_size.split("f/")[-1])
            camera_data.dof.aperture_fstop = aperture_size_float
        else:
            camera_data.dof.aperture_fstop = props.custom_aperture_size

        # Connect the camera to the DOF_target object via a Track To constraint
        cam_target_object = props.cam_target
        if cam_target_object:
            camera_object.constraints.clear()
            cam_track_constraint = camera_object.constraints.new(type='TRACK_TO')
            cam_track_constraint.target = cam_target_object
            cam_track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
            cam_track_constraint.up_axis = 'UP_Y'

            # Update the distance of the DOF target empty based on the depth of field slider
            dof_target_object = bpy.data.objects.get("DOF_target")
            if dof_target_object:
                dof_target_object.location = camera_object.location + camera_object.matrix_world.to_quaternion() @ Vector((0.0, 0.0, -props.dof_target_distance))

        # Update the resolution properties
        context.scene.render.resolution_x = props.resolution_x
        context.scene.render.resolution_y = props.resolution_y

        # Restore DOF_Target object if depth of field is re-enabled
        if props.use_depth_of_field and not dof_target_object:
            dof_target_object = bpy.data.objects.new("DOF_target", None)
            bpy.data.collections.get("Camera Collection").objects.link(dof_target_object)
            dof_target_object.location = Vector((0, 0, 0))
            camera_data.dof.focus_object = dof_target_object

            # Set the distance of the DOF target empty
            dof_target_object.location = camera_object.location + camera_object.matrix_world.to_quaternion() @ Vector((0.0, 0.0, -props.dof_target_distance))




def update_custom_camera(self, context):
    if bpy.data.is_dirty:
        save_prompt = "Your project has unsaved changes. Do you want to save before updating the Custom Camera add-on?"
        save_options = {'CANCELLED', 'FINISHED', 'NO', 'YES'}
        save_choice = bpy.ops.wm.save_mainfile('INVOKE_DEFAULT')
        if save_choice == 'CANCELLED':
            self.report({"INFO"}, "Custom Camera add-on update cancelled.")
            return {'CANCELLED'}

    # Download the updated script
    url = "https://raw.githubusercontent.com/mdreece/Custom-Camera-Blender-Add-on/main/custom_camera.py"
    response = urllib.request.urlopen(url)
    data = response.read()

    # Write the updated script to disk
    script_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "custom_camera.py")
    with open(script_path, "wb") as f:
        f.write(data)

    # Prompt to save the project before closing Blender
    return bpy.ops.wm.quit_blender('INVOKE_DEFAULT')

    # Prompt to save the project before closing Blender
    wm = bpy.context.window_manager
    return wm.invoke_props_dialog(self.quit_blender, width=400)

def quit_blender(self, context):
    bpy.ops.wm.save_mainfile()
    self.quit_blender()


class CustomCameraPreferences(bpy.types.AddonPreferences):
    bl_idname = __name__

    def draw(self, context):
        layout = self.layout
        layout.operator("customcamera.update_custom_camera", text="Update Custom Camera")
        layout.operator("wm.url_open", text="Visit GitHub Repository").url = "https://github.com/mdreece/Custom-Camera-Blender-Add-on"
class UPDATE_CUSTOMCAMERA_OT_update_custom_camera(bpy.types.Operator):
    bl_idname = "customcamera.update_custom_camera"
    bl_label = "Update Custom Camera"
    bl_description = "Update the Custom Camera add-on with the latest version from GitHub"

    def execute(self, context):
        update_custom_camera(self, context)
        return {"FINISHED"}

class CustomCameraProperties(bpy.types.PropertyGroup):
    sensor_sizes = [
        ("6.17", "1/2.3\" (6.17 x 4.55 mm)", ""),
        ("7.6", "1/1.7\" (7.6 x 5.7 mm)", ""),
        ("17.3", "Micro Four Thirds (17.3 x 13 mm)", ""),
        ("23.5", "APS-C (23.5×15.6 mm)", ""),
        ("24.89", "Super 35 (24.89 x 18.66 mm)", ""),
        ("36", "Full-Frame (36 x 24 mm)", ""),
        ("30.7", "Red Dragon 6K (30.7 x 15.8 mm)", ""),
        ("54.12", "Arri Alexa 65 (54.12 x 25.58 mm)", ""),
        ("70", "IMAX (70 x 48.5 mm)", ""),
        ("CUSTOM", "Custom", ""),
    ]
    focal_lengths = [
        ("18mm", "18mm", ""),
        ("24mm", "24mm", ""),
        ("35mm", "35mm", ""),
        ("50mm", "50mm", ""),
        ("85mm", "85mm", ""),
        ("135mm", "135mm", ""),
        ("CUSTOM", "Custom", ""),
    ]
    sensor_size: EnumProperty(
        name="Sensor Size",
        items=sensor_sizes,
        default="36",
        update=update_camera_settings,
    )
    focal_length: EnumProperty(
        name="Focal Length",
        items=focal_lengths,
        default="50mm",
        update=update_camera_settings,
    )
    custom_sensor_size: FloatProperty(
        name="Custom Sensor Size",
        description="Set custom sensor size in millimeters",
        default=35.0,
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
    use_depth_of_field: BoolProperty(
        name="Use Depth of Field",
        description="Enable or disable depth of field",
        default=False,
        update=update_camera_settings,
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
    dof_target_distance: FloatProperty(
        name="DOF Target Distance",
        description="Set distance of the DOF target empty",
        default=5.0,
        min=0.0,
        update=update_camera_settings,
    )
    camera_collection_selected: BoolProperty(
        name="Camera Collection Selected",
        description="Whether the camera collection is selected",
        default=False,
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


class CUSTOMCAMERA_OT_select_camera_collection(bpy.types.Operator):
    bl_idname = "customcamera.select_camera_collection"
    bl_label = "Select Camera Collection"
    bl_description = "Select all objects in the Camera Collection"

    def execute(self, context):
        camera_collection = bpy.data.collections.get("Camera Collection")
        props = context.scene.custom_camera_props

        if camera_collection:
            # Deselect all objects first
            bpy.ops.object.select_all(action='DESELECT')

            # Select objects in the camera collection
            for obj in camera_collection.objects:
                obj.select_set(True)

            props.camera_collection_selected = True

            # Disable selection for other objects
            bpy.context.scene.tool_settings.mesh_select_mode[:] = (False, False, False)
            bpy.context.scene.tool_settings.mesh_select_mode[:] = (True, True, True)

            # Disable object selection
            bpy.context.scene.tool_settings.use_mesh_automerge = True

            # Change the operator name and label to "Deselect Camera Collection"
            self.bl_idname = "customcamera.deselect_camera_collection"
            self.bl_label = "Deselect Camera Collection"
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

            # Enable selection for other objects
            bpy.context.scene.tool_settings.mesh_select_mode[:] = (True, True, True)
            bpy.context.scene.tool_settings.use_mesh_automerge = False

            # Change the operator name and label back to "Select Camera Collection"
            self.bl_idname = "customcamera.select_camera_collection"
            self.bl_label = "Select Camera Collection"
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

        layout.separator()

        row = layout.row()
        row.prop(props, "sensor_size")

        if props.sensor_size == "CUSTOM":
            row = layout.row()
            row.prop(props, "custom_sensor_size")

        row = layout.row()
        row.prop(props, "focal_length")

        if props.focal_length == "CUSTOM":
            row = layout.row()
            row.prop(props, "custom_focal_length")

        row = layout.row()
        row.prop(props, "resolution_x")

        row = layout.row()
        row.prop(props, "resolution_y")

        layout.separator()

        row = layout.row()
        row.prop(props, "use_depth_of_field")

        if props.use_depth_of_field:
            row = layout.row()
            row.prop(props, "dof_target_distance")
            row = layout.row()
            row.prop(props, "bokeh_shape")

            if props.bokeh_shape == "CUSTOM":
                row = layout.row()
                row.prop(props, "custom_bokeh_size")

            row = layout.row()
            row.prop(props, "aperture_size")

            if props.aperture_size == "CUSTOM":
                row = layout.row()
                row.prop(props, "custom_aperture_size")

        if bpy.data.collections.get("Camera Collection"):
            row = layout.row()
            props = context.scene.custom_camera_props

            if props.camera_collection_selected:
                row.operator("customcamera.deselect_camera_collection", text="Deselect Camera Collection")
            else:
                row.operator("customcamera.select_camera_collection", text="Select Camera Collection")
        else:
            row = layout.row()
            row.operator("customcamera.create_camera_collection", text="Create Camera Collection")

        if bpy.data.objects.get("CustomCamera"):
            row = layout.row()
            row.operator("customcamera.delete_camera", text="Delete Camera", icon='CANCEL').action = 'DELETE_CAMERA'


        else:
            row = layout.row()
            row.operator("customcamera.create_camera", text="Create Custom Camera")

        layout.separator()

class CUSTOMCAMERA_OT_create_camera(bpy.types.Operator):
    bl_idname = "customcamera.create_camera"
    bl_label = "Create Custom Camera"
    bl_description = "Create a camera with custom settings"

    def execute(self, context):
        props = context.scene.custom_camera_props

        # Create Camera Collection
        camera_collection = bpy.data.collections.new("Camera Collection")
        bpy.context.scene.collection.children.link(camera_collection)

        # Create Camera
        camera_data = bpy.data.cameras.new("CustomCamera")
        camera_object = bpy.data.objects.new("CustomCamera", camera_data)
        camera_collection.objects.link(camera_object)
        
        # Set end clip
        camera_data.clip_end = 1000000000

        # Set Camera location
        camera_object.location = (6.5, -6.5, 4.0)

        # Create CAM_target object
        cam_target_object = bpy.data.objects.new("CAM_target", None)
        camera_collection.objects.link(cam_target_object)
        cam_target_object.location = Vector((0, 0, 0))

        # Connect camera to CAM_target object via Track To constraint
        cam_track_constraint = camera_object.constraints.new(type='TRACK_TO')
        cam_track_constraint.target = cam_target_object
        cam_track_constraint.track_axis = 'TRACK_NEGATIVE_Z'
        cam_track_constraint.up_axis = 'UP_Y'

        # Store CAM_target object in custom_camera_props
        props.cam_target = cam_target_object

        if props.use_depth_of_field:
            # Create DOF_target object
            dof_target_object = bpy.data.objects.new("DOF_target", None)
            camera_collection.objects.link(dof_target_object)
            dof_target_object.location = Vector((0, 0, 0))

            # Store the DOF_target object in the custom_camera_props
            props.dof_target = dof_target_object

            # Enable depth of field on camera
            camera_data.dof.use_dof = True

            # Connect depth of field to the DOF_target object
            camera_data.dof.focus_object = dof_target_object

            # Set the distance of the DOF target empty
            dof_target_object.location = camera_object.location + camera_object.matrix_world.to_quaternion() @ Vector((0.0, 0.0, -props.dof_target_distance))
        else:
            # Disable depth of field on camera
            camera_data.dof.use_dof = False

        # Update camera settings
        update_camera_settings(self, context)

        return {'FINISHED'}

class CUSTOMCAMERA_OT_delete_camera(bpy.types.Operator):
    bl_idname = "customcamera.delete_camera"
    bl_label = "Delete Camera"
    bl_description = "Delete the custom camera"

    action: bpy.props.StringProperty()

    def execute(self, context):
        if self.action == 'DELETE_CAMERA':
            custom_camera_obj = bpy.data.objects.get("CustomCamera")
            if custom_camera_obj:
                # If the camera exists, disable Depth of Field options
                context.scene.custom_camera_props.use_depth_of_field = False
                bpy.data.objects.remove(custom_camera_obj, do_unlink=True)
                bpy.data.objects.remove(bpy.data.objects.get("CAM_target"), do_unlink=True)
                bpy.data.collections.remove(bpy.data.collections.get("Camera Collection"), do_unlink=True)
                context.scene.custom_camera_props.dof_target = None
                context.scene.custom_camera_props.cam_target = None
        return {'FINISHED'}


    def invoke(self, context, event):
        self.report({'INFO'}, "Are you sure you want to delete the camera?")
        return context.window_manager.invoke_confirm(self, event)

def on_object_selection_change(scene):
    props = scene.custom_camera_props

    camera_collection = bpy.data.collections.get("Camera Collection")
    if camera_collection:
        # Check if any object in the camera collection is selected
        props.camera_collection_selected = any(obj.select_get() for obj in camera_collection.objects)
    else:
        props.camera_collection_selected = False

# Register the event handler when the add-on is enabled
def register():
    bpy.utils.register_class(CustomCameraProperties)
    bpy.types.Scene.custom_camera_props = bpy.props.PointerProperty(type=CustomCameraProperties)
    bpy.utils.register_class(CUSTOMCAMERA_OT_create_camera)
    bpy.utils.register_class(CUSTOMCAMERA_PT_main_panel)
    bpy.utils.register_class(CUSTOMCAMERA_OT_delete_camera)
    bpy.utils.register_class(CUSTOMCAMERA_OT_select_camera_collection)
    bpy.utils.register_class(CUSTOMCAMERA_OT_deselect_camera_collection)
    bpy.utils.register_class(UPDATE_CUSTOMCAMERA_OT_update_custom_camera)
    bpy.utils.register_class(CustomCameraPreferences)

    # Add the event handler to listen for object selection changes
    bpy.app.handlers.depsgraph_update_post.append(on_object_selection_change)

# Unregister the event handler when the add-on is disabled
def unregister():
    # Remove the event handler
    bpy.app.handlers.depsgraph_update_post.remove(on_object_selection_change)

    bpy.utils.unregister_class(CustomCameraProperties)
    del bpy.types.Scene.custom_camera_props
    bpy.utils.unregister_class(CUSTOMCAMERA_OT_create_camera)
    bpy.utils.unregister_class(CUSTOMCAMERA_PT_main_panel)
    bpy.utils.unregister_class(CUSTOMCAMERA_OT_delete_camera)
    bpy.utils.unregister_class(CUSTOMCAMERA_OT_select_camera_collection)
    bpy.utils.unregister_class(CUSTOMCAMERA_OT_deselect_camera_collection)
    bpy.utils.unregister_class(CustomCameraPreferences)
    bpy.utils.unregister_class(UPDATE_CUSTOMCAMERA_OT_update_custom_camera)

if __name__ == "__main__":
    register()
