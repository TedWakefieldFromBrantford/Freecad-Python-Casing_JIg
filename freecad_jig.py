import FreeCAD as App
import Part
import FreeCADGui as Gui
from PySide2 import QtWidgets
import time

def show_message(title, text):
    dialog = QtWidgets.QMessageBox()
    dialog.setWindowTitle(title)
    dialog.setText(text)
    dialog.exec_()

def get_float_input(prompt, min_val=0.0, max_val=1000.0, decimals=3):
    dialog = QtWidgets.QInputDialog()
    dialog.setInputMode(QtWidgets.QInputDialog.DoubleInput)
    dialog.setLabelText(prompt)
    dialog.setDoubleMinimum(min_val)
    dialog.setDoubleMaximum(max_val)
    dialog.setDoubleDecimals(decimals)
    if dialog.exec_():
        return dialog.doubleValue()
    return None

def create_component(doc, name, shape, color=None):
    obj = doc.addObject("Part::Feature", name)
    obj.Shape = shape
    if color:
        obj.ViewObject.ShapeColor = color
    doc.recompute()
    Gui.SendMsgToActiveView("ViewFit")
    return obj

# Initialize
doc = App.ActiveDocument or App.newDocument()
Gui.activateWorkbench("PartWorkbench")

# Get user input
triangle_width = get_float_input("Enter trim width (inches):\nExample: 2¾\" = 2.750")
if not triangle_width: raise ValueError("Operation cancelled")
triangle_width *= 25.4  # Convert to mm

reveal = get_float_input("Enter reveal as number of sixteenths:\nExample: 3/16\" = 3")
if not reveal: raise ValueError("Operation cancelled")
reveal = (reveal / 16) * 25.4  # Convert to mm

# Create 2d triangle
vertices = [
    App.Vector(0, 0, 0),
    App.Vector(triangle_width, 0, 0),
    App.Vector(0, triangle_width, 0)
]
wire = Part.makePolygon(vertices + [vertices[0]])
triangle = create_component(doc, "BaseTriangle", Part.Face(wire), (1.0, 0.0, 0.0))

# Extrude triangle.
pad_shape = triangle.Shape.extrude(App.Vector(0, 0, 10))
pad = create_component(doc, "Pad", pad_shape, (0.0, 1.0, 0.0))

# Create flat jamb-hook component
box1 = Part.makeBox(30, 50 + reveal, 10, App.Vector(triangle_width - 30 + 2*reveal, -50 - reveal, 0))
box1_obj = create_component(doc, "FrameHook", box1, (0.0, 0.0, 1.0))
box2 = Part.makeBox(reveal, reveal, 10, App.Vector(triangle_width + reveal, -reveal, 0))
box2_obj = create_component(doc, "CutTool", box2, (1.0, 1.0, 0.0))

# Perform cut operation
cut_shape = box1_obj.Shape.cut(box2_obj.Shape)
cut = create_component(doc, "CutResult", cut_shape, (0.5, 0.0, 0.5))

# Create jamb-hook return
box3 = Part.makeBox(3, 50, 25, App.Vector(triangle_width + reveal *2 - 3, -50 - reveal, 0))
jamb_hook = create_component(doc, "JambHook", box3, (0.0, 1.0, 1.0))

# Merge components
fuse_shape = pad.Shape.fuse(cut.Shape).fuse(jamb_hook.Shape)
merged = create_component(doc, "Merged", fuse_shape, (0.8, 0.8, 0.8))

# Create mirror copy
mirror_transform = App.Matrix()
mirror_transform.scale(App.Vector(-1, 1, 1))
mirror_shape = merged.Shape.transformGeometry(mirror_transform)
mirror_shape.translate(App.Vector(-10, 0, 0))
mirror = create_component(doc, "MirrorCopy", mirror_shape, (0.5, 0.5, 0.0))

# Final assembly
final_shape = merged.Shape.fuse(mirror.Shape)
final = create_component(doc, "FinalDesign", final_shape, (0.2, 0.8, 0.2))

# Cleanup
for obj in [triangle, pad, box1_obj, box2_obj, cut, jamb_hook, merged, mirror]:
    obj.ViewObject.Visibility = False

# Display final design
Gui.activeDocument().activeView().viewAxometric()
Gui.SendMsgToActiveView("ViewFit")

# would user like to make manual adjustments?
if QtWidgets.QMessageBox.question(None, "Manual Adjustments", "Would you like to make manual adjustments?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No) == QtWidgets.QMessageBox.Yes:
    Gui.activateWorkbench("PartDesignWorkbench")
    Gui.SendMsgToActiveView("ViewFit")
    show_message("Manual Adjustments", "Make your manual adjustments and then export the final design.")

#export as 3D printable file
Gui.Selection.addSelection('Unnamed','FinalDesign')
Gui.runCommand('Std_Export',0)
#




  