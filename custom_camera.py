bl_info = {
    "name": "Custom Camera",
    "author": "Montana Reece",
    "version": (2, 3),
    "blender": (3, 40, 1),
    "location": "View3D > Tool Shelf > Custom Camera Add-on",
    "description": "Add a custom camera setup",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

from mathutils import Vector
import bpy
from bpy.props import EnumProperty, FloatProperty, StringProperty, BoolProperty
from bpy_extras.io_utils import ImportHelper


def update_camera_settings(self, context):
    camera_object = bpy.data.objects.get("CustomCamera")
    if camera_object and camera_object.type == 'CAMERA':
        camera_data = camera_object.data
        props = context.scene.custom_camera_props

        camera_data.sensor_width = float(props.sensor_size) if props.sensor_size != "CUSTOM" else props.custom_sensor_size
        camera_data.lens = float(props.focal_length.rstrip("mm")) if props.focal_length != "CUSTOM" else props.custom_focal_length

        if props.use_depth_of_field:
            dof_target_object = bpy.data.objects.get("DOF_target")
            if not dof_target_object:
                # Create DOF_target object if it doesn't exist
                dof_target_object = bpy.data.objects.new("DOF_target", None)
                camera_object.users_collection[0].objects.link(dof_target_object)
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
                "HEXAGONAL": 6,
                "OCTAGONAL": 8,
                "STAR": 8,
            }[props.bokeh_shape]

        # Convert aperture size to a float
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
        default=True,
        update=update_camera_settings,
    )
    depth_of_field: FloatProperty(
        name="Depth of Field",
        description="Set depth of field for the camera",
        default=0.1,
        min=0.0,
        update=update_camera_settings,
    )
    bokeh_shapes = [
        ("CIRCULAR", "Circular", ""),
        ("HEXAGONAL", "Hexagonal", ""),
        ("OCTAGONAL", "Octagonal", ""),
        ("STAR", "Star", ""),
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
        description="Set custom size of bokeh",
        default=0.05,
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




class CUSTOMCAMERA_OT_select_camera_collection(bpy.types.Operator):
    bl_idname = "customcamera.select_camera_collection"
    bl_label = "Select Camera Collection"
    bl_description = "Select all objects in the Camera Collection"

    def execute(self, context):
        camera_collection = bpy.data.collections.get("Camera Collection")

        if camera_collection:
            for obj in camera_collection.objects:
                obj.select_set(True)
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

        row = layout.row()
        row.operator("customcamera.create_camera", text="Create Custom Camera")

        layout.separator()

        row = layout.row()
        row.operator("customcamera.select_camera_collection", text="Select Camera Collection")



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
        else:
            # Disable depth of field on camera
            camera_data.dof.use_dof = False

        # Update camera settings
        update_camera_settings(self, context)

        return {'FINISHED'}





def register():
    bpy.utils.register_class(CustomCameraProperties)
    bpy.types.Scene.custom_camera_props = bpy.props.PointerProperty(type=CustomCameraProperties)
    bpy.utils.register_class(CUSTOMCAMERA_OT_create_camera)
    bpy.utils.register_class(CUSTOMCAMERA_PT_main_panel)
    bpy.utils.register_class(CUSTOMCAMERA_OT_select_camera_collection)

def unregister():
    bpy.utils.unregister_class(CustomCameraProperties)
    del bpy.types.Scene.custom_camera_props
    bpy.utils.unregister_class(CUSTOMCAMERA_OT_create_camera)
    bpy.utils.unregister_class(CUSTOMCAMERA_PT_main_panel)
    bpy.utils.unregister_class(CUSTOMCAMERA_OT_select_camera_collection)

if __name__ == "__main__":
    register()
