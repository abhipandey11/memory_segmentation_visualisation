# MEMORY_SEGMENTATION-VISUALISATION
It provides a graphical user interface(GUI) for visualizing memory segmentation in a system. Users can specify the size of the main memory and the segment's name and size to be allocated within that main memory. The tool attempts to allocate memory segments randomly while ensuring that segments do not overlap and fit within the memory constraints. It also provides a visualization of the memory compaction.

## REQUIREMENTS
* Python 3.x
* **tkinter** - for GUI
* **matplotlib** - for visualisation

## USAGE
* Run the .py file
* Enter the main memory size and number of memory segments in the respective textboxes.
* Enter segment info (name and size with space in between)in the format <segment_name segment_size>
* Click on confirm to get the visualisation.
* Click on allocate memory if you need to change the segment info.
