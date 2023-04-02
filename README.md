# Custom-Camera-Blender-Add-on
Add-on for Blender that allows creation/adjustments of a camera. Allows for control with DOF and where the camera is focused using Targets.


Custom Camera Add-on Documentation
Description

The Custom Camera Add-on allows Blender users to create and configure a custom camera with various sensor sizes, focal lengths, depth of field, and bokeh settings. It is designed to simplify the process of setting up a camera for complex scenes, providing an easy-to-use interface for adjusting camera settings.
Installation

    Download the Add-on file.
    Open Blender and navigate to Edit > Preferences > Add-ons.
    Click on Install and locate the downloaded Add-on file.
    Activate the Add-on by checking the box next to Object: Custom Camera.

Usage

The Add-on is located in the 3D viewport's Tool Shelf under the "Custom Camera" tab.
Main Panel

The main panel is divided into several sections:

    Sensor Size: Choose from a list of common sensor sizes or enter a custom size in millimeters.
    Focal Length: Select from a list of common focal lengths or enter a custom focal length in millimeters.
    Depth of Field: Enable or disable depth of field, and adjust the bokeh shape and size.
    Aperture Size: Choose from a list of common aperture sizes or enter a custom aperture size.

Click on the "Create Custom Camera" button to create the camera object with the specified settings.
Sensor Sizes

The following sensor sizes are available:

    1/2.3" (6.17 x 4.55 mm)
    1/1.7" (7.6 x 5.7 mm)
    Micro Four Thirds (17.3 x 13 mm)
    APS-C (23.5 x 15.6 mm)
    Super 35 (24.89 x 18.66 mm)
    Full-Frame (36 x 24 mm)
    Red Dragon 6K (30.7 x 15.8 mm)
    Arri Alexa 65 (54.12 x 25.58 mm)
    IMAX (70 x 48.5 mm)
    Custom

Focal Lengths

The following focal lengths are available:

    18mm
    24mm
    35mm
    50mm
    85mm
    135mm
    Custom

Depth of Field and Bokeh Settings

    Use Depth of Field: Enable or disable depth of field for the camera.
    Bokeh Shape: Choose from Circular, Hexagonal, Octagonal, Star, or Custom shapes for the bokeh.
    Custom Bokeh Size: If the bokeh shape is set to Custom, this setting allows you to specify the size of the bokeh.

Aperture Sizes

The following aperture sizes are available:

    f/0.5
    f/1.0
    f/1.4
    f/2.0
    f/2.8
    f/4.0
    f/5.6
    f/8.0
    f/11
    f/16
    f/22
    f/32
    f/45
    f/64
    f/90
    Custom
    
    
Dpeth of Field and Camera Target Focus are controlled by Emptys. (DOF_target, CAM_target)

Limitations

    The Add-on has only been tested on Blender 3.40.1 and above.
    Custom aperture sizes are limited to a range of f/0.5 to f/90.
    ONLY SUPPORTS MICROSOFT WINDOWS (only tested in Windows 10 and 11 Pro+)
    
    
    
