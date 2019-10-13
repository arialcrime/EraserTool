from AppKit import NSImage
from mojo.roboFont import CreateCursor
from mojo.extensions import ExtensionBundle

eraserBundle = ExtensionBundle("EraserTool")
eraserCursor = CreateCursor(eraserBundle.get("eraserCursor"), hotSpot=(4,14))
toolbarIcon = eraserBundle.get("toolbarToolsEraser")

from mojo.events import EditingTool, installTool
from mojo.UI import UpdateCurrentGlyphView

class EraserTool (EditingTool):
    def mouseDown(self, point, clickCount):
        g = CurrentGlyph()
        self.convertToLine(g)
            
    def convertToLine(self, glyph):
        if glyph and glyph.selection != []:
            glyph.prepareUndo()
            for c_index in range(len(glyph.contours)):
                c = glyph.contours[c_index]
                for s_index in range(len(c.segments)):
                    s = c.segments[s_index]
                    if s.selected and s.type == "curve":
                        s.type = "line"
                        s.points[0].smooth = False
                        s.smooth = False
                        c.segments[s_index-1].points[-1].smooth = False

            glyph.deselect()
            UpdateCurrentGlyphView()
            glyph.changed()

    def getToolbarTip(self):
        return "Eraser Tool"
        
    def getToolbarIcon(self):
        return toolbarIcon
        
    def getDefaultCursor(self):
        return eraserCursor

installTool(EraserTool())