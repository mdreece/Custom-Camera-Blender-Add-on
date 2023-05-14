# Custom-Camera-Blender-Add-on (0.3.3 alpha)
Add-on for Blender that allows creation/adjustments of a camera. Allows for control with DOF and where the camera is focused using Targets.
Documentation for Custom Camera Add-on
(Tested in Blender v3.4 and up)

v0.3.0 (alpha) DEMO: https://youtu.be/Tjn5XVe6H-o 

Custom Camera Add-on User Documentation

Introduction:

The Custom Camera Add-on is a tool for Blender that allows you to create and customize cameras with various settings for your scenes. With this add-on, you can easily set up custom sensor size, focal length, depth of field, bokeh shape, aperture size, and more.
Installation:
To install the Custom Camera Add-on, follow these steps:
    1. Launch Blender.
    2. Open the Preferences window by clicking on "Edit" in the top menu and selecting "Preferences."
    3. In the Preferences window, click on the "Add-ons" tab.
    4. Click on the "Install..." button located at the top right corner of the window.
    5. In the file browser, navigate to the location where you saved the Custom Camera Add-on script file.
    6. Select the script file and click on the "Install Add-on" button.
    7. Once the add-on is installed, you can enable it by checking the checkbox next to its name in the add-ons list.
    8. The Custom Camera Add-on should now be available in the Blender interface.
User Interface:
The Custom Camera Add-on adds a new panel called "Custom Camera" to the Tool Shelf in the 3D Viewport. To access the add-on's settings, make sure you are in the "Object" mode and activate the Tool Shelf by pressing the "T" key.
In the "Custom Camera" panel, you will find the following settings:
Sensor Size:
    • This setting allows you to choose the sensor size for the camera. By default, a list of predefined sensor sizes is available, ranging from small to large formats. You can select a specific sensor size from the list.
    • If you choose "Custom" from the list, an additional input field will appear where you can enter a custom sensor size in millimeters.
Focal Length:
    • This setting allows you to choose the focal length of the camera lens. Similar to the sensor size setting, you can select a focal length from the predefined list or enter a custom focal length.
Use Depth of Field:
    • This option enables or disables depth of field for the camera. When enabled, the camera will simulate the effect of a shallow depth of field, where objects in front or behind the focus point appear blurred.
Depth of Field:
    • This setting controls the depth of field value for the camera. It determines the distance range within which objects will appear in focus when depth of field is enabled.
Bokeh Shape:
    • This setting allows you to choose the shape of the bokeh effect produced by the camera's aperture. Bokeh refers to the aesthetic quality of the out-of-focus areas in an image. You can select from predefined shapes such as circular, triangle, pentagon, hexagonal, octagonal, or anamorphic.
    • If you choose "Custom," an additional input field will appear where you can enter a custom size for the bokeh shape.
Aperture Size:
    • This setting determines the size of the camera's aperture. A smaller aperture size (larger f-stop value) results in a greater depth of field, while a larger aperture size (smaller f-stop value) creates a shallower depth of field.
    • Similar to other settings, you can choose a predefined aperture size from the list or enter a custom value.
DOF Target Distance:
    • This setting determines the distance of the depth of field target object from the camera. The depth of field effect will be based on this distance.
Camera Collection:
    • This section provides options to select or deselect the camera collection. The camera collection is a collection of objects related to the camera setup.
    • The "Select Camera Collection" button selects all objects in the camera collection, making it easier to work with them as a group. The "Deselect Camera Collection" button deselects all objects in the camera collection.
Create Custom Camera:
    • This button creates a new custom camera based on the selected settings. It creates a camera object with the specified sensor size, focal length, and other parameters.
Delete Camera:
    • This button deletes the custom camera and its associated objects, such as the camera target and depth of field target.
Updating the Add-on:
The Custom Camera Add-on can be updated to the latest version from the GitHub repository. To update the add-on, follow these steps:
    1. In the "Custom Camera" panel, click on the "Update Custom Camera" button.
    2. The add-on will download the updated script from the GitHub repository.
    3. After downloading, the add-on will prompt you to save the project before closing Blender.
    4. Choose whether to save or cancel the project and close Blender.
    5. Restart Blender, and the Custom Camera Add-on will be updated to the latest version.
Additional Resources:
    • You can visit the GitHub repository for the Custom Camera Add-on to access more information, updates, and documentation.
Conclusion
The Custom Camera Add-on provides an easy and convenient way to create and customize cameras with various settings in Blender. With its intuitive user interface and options, you can achieve the desired camera setup for your scenes. Enjoy using the Custom Camera Add-on and unleash your creativity in Blender!



Support:
If you encounter any issues with the Custom Camera add-on, please feel free to open an issue on the GitHub repository. Include the following in your issue:

    Screenshots if able.
    Error displayed in ‘Console’
    Error displayed in Editor Type ‘Info’.
    Current Version of Blender.exe
    
   

Changelog:

5/13/2023: v0.3.3 (alpha)

    Selecting other objects completely deselects the camera collection and vicaversa. 


4/4/2023: v0.3.2 (alpha)

    Additional Bokeh opions added:
         - Triangle
         - Pentagon
         - Anamorphic (Oval)

4/2/2023: v0.3.0 (alpha)
    
    Blender prompts to save the current project prior to closing the program post updates

4/2/2023: v0.2.9 (alpha)
    
    Button in Preferences to automatically update the addon (restart of Blender required).
    Button in Preferences linking to the Add-on GITHUB.

4/2/2023: v0.2.7 (alpha)

    New options for Camera movement (still janky)
    Safety feature added for the 'Delete Camera' option.

4/2/2023: v0.2.3 (alpha)

    New options for Camera movement
    DOF target distance slider in Add-on panel

4/1/2023: v0.2.2 (alpha)

    RELEASE!!

"Dave Nectariad Rome" is just my full name all mixed up. (Entire Script is made for fun)
