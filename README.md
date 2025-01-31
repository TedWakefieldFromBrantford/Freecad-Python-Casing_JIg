Linux proceedure:  (maybe someone smarter can me can post other OS directions)

After downloading code, and installing any required dependencies, 
which may include python3, freecad, pyside...
Simply run as an argument when opening FreeCAD in terminal, E.g:
freecad /home/user/freecad_Jig.py

FreeCAD will open, prompt for trim width 
(as inches in decimal format, so [2.75] or [3.5]), and reveal 
(as number of 1/16ths, so [2] would be 1/8th), then make a left and right version. 
From here you can export as whatever file type 
your slicer loves best, or cancel and tweak from there.
this program does not save or export anything, 
and only calls the export function once.

If you make changes to model, be sure to use the FreeCAD Gui to 
save and/or export manually. 

your slicer can also be opened the same way, with the path to you exported
file used as an argment.
