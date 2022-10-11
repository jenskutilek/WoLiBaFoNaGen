import objc

from AppKit import NSMenuItem
from GlyphsApp import EDIT_MENU, Glyphs
from GlyphsApp.plugins import GeneralPlugin


class WoLiBaFoNaGen(GeneralPlugin):
    @objc.python_method
    def settings(self):
        self.name = Glyphs.localize(
            {
                "en": "WoLiBaFoNaGen",
            }
        )

    @objc.python_method
    def start(self):
        newMenuItem = NSMenuItem(self.name, self.showWindow_)
        Glyphs.menu[EDIT_MENU].append(newMenuItem)

    def showWindow_(self, sender):
        """Do something like show a window"""
        print("show Windows")

    @objc.python_method
    def __file__(self):
        """Please leave this method unchanged"""
        return __file__
