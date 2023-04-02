# Custom-Camera-Blender-Add-on
Add-on for Blender that allows creation/adjustments of a camera. Allows for control with DOF and where the camera is focused using Targets.

Custom Camera: v2.2 (alpha)

The "Custom Camera" add-on allows you to create a custom camera with various settings in Blender.

Installation

    Download the script as a Python file.
    Open Blender and go to "Edit" > "Preferences".
    Click on the "Add-ons" tab.
    Click the "Install..." button and navigate to the downloaded Python file.
    Select the file and click "Install Add-on".
    The add-on should now be installed and ready to use.

Setting up Cameras

    Open Blender and switch to the "3D Viewport".
    Press "N" to open the "Tool Shelf" and select the "Custom Camera" tab.
    Click on the "Create Custom Camera" button to create a new camera with default settings.
    You can adjust the camera settings in the "Custom Camera" tab, such as the sensor size, focal length, depth of field, bokeh shape, and aperture size.

Settings
Sensor Size

    Allows you to select the sensor size of the camera from a predefined list.
    You can also select "Custom" to set a custom sensor size in millimeters.

Focal Length

    Allows you to select the focal length of the camera lens from a predefined list.
    You can also select "Custom" to set a custom focal length in millimeters.

Use Depth of Field

    Allows you to enable or disable depth of field for the camera.

Depth of Field

    Allows you to set the depth of field for the camera in meters.

Bokeh Shape

    Allows you to select the shape of the bokeh for the camera from a predefined list.
    You can also select "Custom" to set a custom bokeh size.

Aperture Size

    Allows you to select the aperture size of the camera from a predefined list.
    You can also select "Custom" to set a custom aperture size.

DOF Target

    Allows you to select an object in the scene to be used as the depth of field target.
    The object must be named "DOF_target" to work properly.

Camera Target: Blender Add-on

    Allows you to select an object in the scene to be used as the camera target.
    The object must be named "CAM_target" to work properly.

DOF Target Distance

    Allows you to set the distance of the depth of field target object from the camera.

Camera Collection Selected

    Indicates whether the camera collection is currently selected.

Operators
Create Custom Camera

    Creates a new camera with the current custom camera settings.
    The camera will be added to a new collection named "Camera Collection".
    If a camera already exists, this button will not be visible.

Select Camera Collection

    Selects all objects in the "Camera Collection" collection.

Notes

    The camera created by the add-on is named "CustomCamera".
    The camera target object created by the add-on is named "CAM_target".
    The depth of field target object created by the add-on is named "DOF_target".
    You can adjust the position and rotation of the camera and target objects as needed.
    You can delete the camera, camera target, and depth of field target objects at any time, but doing so will remove all associated settings and constraints.

Limitations

    The Add-on has only been tested on Blender 3.40.1 and above.
    Custom aperture sizes are limited to a range of f/0.5 to f/90.
    ONLY SUPPORTS MICROSOFT WINDOWS (only tested in Windows 10 and 11 Pro+)
    
    
    


CHANGLOG:
4/2/2023: v2.3 (alpha)
 - New options for Camera movement
 - DOF target distance slider in Add-on panel

4/1/2023: v2.2 (alpha)
 - RELEASE!!
