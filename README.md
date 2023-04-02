Custom Camera Blender Add-on Documentation
Overview
The Custom Camera Add-on is a Blender add-on that allows users to create a custom camera setup with various settings, such as sensor size, focal length, depth of field, and aperture size. This add-on is designed to streamline the process of configuring a camera in Blender, making it easier for artists to achieve the desired look for their renders.
Compatibility
This add-on is compatible with Blender 3.40.1.
Installation
    1. Download the script file (custom_camera.py).
    2. Open Blender and go to Edit > Preferences.
    3. In the Preferences window, navigate to the Add-ons tab.
    4. Click on Install and locate the downloaded custom_camera.py file.
    5. Activate the add-on by checking the checkbox next to "Object: Custom Camera".
Usage
After installing the add-on, you will find the Custom Camera panel in the 3D Viewport, under the Tool Shelf in a new tab called Custom Camera.
Custom Camera Panel
The Custom Camera panel provides options to configure the camera settings:
    • Sensor Size: Choose from a list of predefined sensor sizes or select Custom to set a custom sensor size in millimeters.
    • Focal Length: Choose from a list of predefined focal lengths or select Custom to set a custom focal length in millimeters.
    • Use Depth of Field: Enable or disable depth of field for the camera.
    • Bokeh Shape: Choose from a list of predefined bokeh shapes or select Custom to set a custom bokeh size.
    • Aperture Size: Choose from a list of predefined aperture sizes or select Custom to set a custom aperture size.
Click on the Create Custom Camera button to create a new camera with the specified settings.
Custom Camera Object
After creating a custom camera, the add-on will generate a new Camera object in the 3D Viewport with the specified settings. The Camera object is named "CustomCamera" and is placed in a collection called "Camera Collection".
The add-on also creates two helper objects:
    1. CAM_target: An empty object that the camera is aimed at via a Track To constraint.
    2. DOF_target (optional): An empty object that defines the focus point for depth of field, if depth of field is enabled.
These helper objects can be moved to change the camera's orientation and focus.
Uninstallation
To uninstall the Custom Camera Add-on, follow these steps:
    1. Open Blender and go to Edit > Preferences.
    2. In the Preferences window, navigate to the Add-ons tab.
    3. Search for "Custom Camera" in the search bar.
    4. Click on the add-on and then click on the Remove button.
License
This add-on is created by Montana Reece and is licensed under the terms of the MIT License.
