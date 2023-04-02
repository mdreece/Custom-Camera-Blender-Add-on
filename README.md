# Custom-Camera-Blender-Add-on
Add-on for Blender that allows creation/adjustments of a camera. Allows for control with DOF and where the camera is focused using Targets.

Custom Camera Add-on Documentation
Description
The Custom Camera Add-on allows Blender users to create and configure a custom camera with various sensor sizes, focal lengths, depth of field, and bokeh settings. It is designed to simplify the process of setting up a camera for complex scenes, providing an easy-to-use interface for adjusting camera settings.
Installation
    1. Download the Add-on file.
    2. Open Blender and navigate to Edit > Preferences > Add-ons.
    3. Click on Install and locate the downloaded Add-on file.
    4. Activate the Add-on by checking the box next to Object: Custom Camera.
Usage
The Add-on is located in the 3D viewport's Tool Shelf under the "Custom Camera" tab.
Main Panel
The main panel is divided into several sections:
    • Sensor Size: Choose from a list of common sensor sizes or enter a custom size in millimeters.
    • Focal Length: Select from a list of common focal lengths or enter a custom focal length in millimeters.
    • Depth of Field: Enable or disable depth of field, and adjust the bokeh shape and size.
    • Aperture Size: Choose from a list of common aperture sizes or enter a custom aperture size.
Click on the "Create Custom Camera" button to create the camera object with the specified settings.
Sensor Sizes
The following sensor sizes are available:
    1. 1/2.3" (6.17 x 4.55 mm)
    2. 1/1.7" (7.6 x 5.7 mm)
    3. Micro Four Thirds (17.3 x 13 mm)
    4. APS-C (23.5 x 15.6 mm)
    5. Super 35 (24.89 x 18.66 mm)
    6. Full-Frame (36 x 24 mm)
    7. Red Dragon 6K (30.7 x 15.8 mm)
    8. Arri Alexa 65 (54.12 x 25.58 mm)
    9. IMAX (70 x 48.5 mm)
    10. Custom
Focal Lengths
The following focal lengths are available:
    1. 18mm     5. 85mm
    2. 24mm     6. 135mm
    3. 35mm     7. Custom
    4. 50mm
       
Depth of Field and Bokeh Settings
    • Use Depth of Field: Enable or disable depth of field for the camera.
    • Bokeh Shape: Choose from Circular, Hexagonal, Octagonal, Star, or Custom shapes for the bokeh.
    • Custom Bokeh Size: If the bokeh shape is set to Custom, this setting allows you to specify the size of the bokeh.
Aperture Sizes
The following aperture sizes are available:
    1. f/0.5      9. f/11
    2. f/1.0    10. f/16
    3. f/1.4    11. f/22
    4. f/2.0    12. f/32
    5. f/2.8    13. f/45
    6. f/4.0    14. f/64
    7. f/5.6    15. f/90
    8. f/8.0    16. Custom

Limitations
    • The Add-on has only been tested on Blender 3.40.1.
    • Custom aperture sizes are limited to a range of f/0.5 to f/90.
