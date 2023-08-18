<!-- This file is a placeholder for customizing description of your plugin 
on the napari hub if you wish. The readme file will be used by default if
you wish not to do any customization for the napari hub listing.

If you need some help writing a good description, check out our 
[guide](https://github.com/chanzuckerberg/napari-hub/wiki/Writing-the-Perfect-Description-for-your-Plugin)
-->

# Napari Large Image Viewer Plugin

The Napari Large Image Viewer Plugin is a powerful extension for the [napari](https://napari.org/) image visualization software. This plugin is designed to enable the visualization of large TIFF | TIF | CZI | LIF | JPG | PNG | ND2 files directly from disk, without the need to load the entire image into RAM. This is particularly useful when working with large datasets that exceed the available memory of your system.


## Features

- **Efficient Large Image Visualization**: The plugin allows you to open and visualize large files that are too big to fit into memory. It utilizes efficient memory-mapping techniques to display image data without fully loading it into RAM.

- **Interactive Exploration**: With the Napari Large Image Viewer Plugin, you can interactively explore large datasets using familiar zooming, panning, and slicing actions.

- **Quick Installation**: Installing the plugin is simple and straightforward, and it seamlessly integrates with the napari environment.

- **User-Friendly Interface**: The plugin provides an intuitive user interface that integrates seamlessly into the napari interface, making it easy to use for both beginners and experienced users.

## Installation

1. **Prerequisites**: Make sure you have [napari](https://napari.org/) installed on your system. If not, you can install it using:

   ```bash
   pip install napari
   ```

2. **Install the Plugin**: You can install the plugin directly from GitHub using pip:

   ```bash
   pip install git+https://github.com/WyssCenter/Large-Image-Viewer.git
   ```

3. **Launch napari**: Launch napari from your terminal:

   ```bash
   napari
   ```

4. **Activate the Plugin**: Once napari is launched, go to the `Plugins` menu and select `Large Image Viewer` to activate the plugin.

5. **Open Large TIFF File**: With the plugin activated, you can now open a large TIFF file by dragging and dropping it to the napari viewer.

## Usage

1. Open a Large File: Follow the installation instructions above to open a large file using the plugin.

2. Explore the Image: Once the image is loaded, you can use the mouse to zoom in/out, pan, and interactively explore the data. You can also adjust the colormap, contrast, and other visualization settings from the napari interface.

3. Slicing and Navigation: Use the slicing and navigation tools in napari to navigate through different sections of the large file.

4. Save Visualizations: You can save snapshots or screenshots of the current visualization using the napari interface.

## Contributions

Contributions to the Napari Large Image Viewer Plugin are welcome! If you encounter issues or have suggestions for improvements, please open an issue on the [GitHub repository](https://github.com/WyssCenter/Large-Image-Viewer.git).

## License

This plugin is licensed under the [MIT License](LICENSE).

## Contact

For any inquiries or questions, you can reach out to the author at nima.mojtahedi@wysscenter.ch
