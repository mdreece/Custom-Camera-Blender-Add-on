# Custom-Camera-Blender-Add-on (2.7 alpha)
Add-on for Blender that allows creation/adjustments of a camera. Allows for control with DOF and where the camera is focused using Targets.

Documentation for Custom Camera Add-on
The Custom Camera add-on is a Blender add-on that allows users to create a custom camera with a variety of settings, including sensor size, focal length, depth of field, and aperture size. The add-on also includes the ability to create a Camera Collection and connect the camera to a target object via a Track To constraint. The add-on is designed to provide users with greater control over their camera settings, and is particularly useful for those who work in the field of photography and cinematography.
Installation
To install the Custom Camera add-on, follow these steps:
    1. Download the latest release of the Custom Camera add-on from the GitHub repository.
    2. Open Blender and go to Edit > Preferences.
    3. Click on the Add-ons tab.
    4. Click on the Install... button in the top right corner of the window.
    5. Navigate to the downloaded add-on file and select it.
    6. Click on the Install Add-on button.
    7. Once the add-on has been installed, make sure to check the Custom Camera checkbox in the Add-ons list and save your preferences.
Usage
The Custom Camera add-on adds a new panel to the 3D Viewport UI named Custom Camera. The panel contains a variety of settings for customizing the camera.
To create a new custom camera, click on the Create Custom Camera button. This will create a new camera object in the scene with the specified settings. The camera will be named CustomCamera and will be located in a new collection called Camera Collection.
To adjust the settings of the camera, use the options in the Custom Camera panel. The available options are as follows:
    • Sensor Size: Select from a list of predefined sensor sizes, or enter a custom sensor size in millimeters.
    • Focal Length: Select from a list of predefined focal lengths, or enter a custom focal length in millimeters.
    • Use Depth of Field: Enable or disable depth of field for the camera.
    • Depth of Field: Set the depth of field for the camera.
    • Bokeh Shape: Select from a list of predefined bokeh shapes, or enter a custom size for the bokeh.
    • Aperture Size: Select from a list of predefined aperture sizes, or enter a custom aperture size.
    • Camera Collection Selected: Select or deselect all objects in the Camera Collection.
When depth of field is enabled, a new object called DOF_target will be created. This object can be moved to adjust the focus of the camera. The distance of the DOF target empty can be set using the DOF Target Distance property.
The camera can also be connected to a target object via a Track To constraint. To do this, select the target object and set it as the Camera Target property. The camera will automatically track to the target object.
To delete the custom camera, click on the Delete Camera button. This will remove the camera object and its associated objects from the scene.
Support
If you encounter any issues with the Custom Camera add-on, please feel free to open an issue on the GitHub repository.
Include the following in your issue:
- Screenshots if able.
- Error displayed in ‘Console’
- Error displayed in Editor Type ‘Info’.
- Current Version of Blender.exe





CHANGLOG: 
4/2/2023: v2.7 (alpha)
    • New options for Camera movement. (still janky)
    • Safety for ‘Delete Camera’ option.
      
4/2/2023: v2.3 (alpha)
    • New options for Camera movement 
    • DOF target distance slider in Add-on panel 
4/1/2023: v2.2 (alpha)
    • RELEASE!! 
