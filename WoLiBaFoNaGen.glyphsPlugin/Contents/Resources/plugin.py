import objc

from AppKit import NSMenuItem
from GlyphsApp import DOCUMENTOPENED, WINDOW_MENU, Glyphs
from GlyphsApp.plugins import GeneralPlugin

key = "de.kutilek.glyphs.WoLiBaFoNaGen.%s"


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
        Glyphs.menu[WINDOW_MENU].append(newMenuItem)
        self.load_defaults()

    @objc.python_method
    def load_defaults(self):
        self.word_list_name = Glyphs.defaults[key % "word_list"]
        self.min_length = Glyphs.defaults[key % "min_length"]
        self.max_length = Glyphs.defaults[key % "max_length"]
        self.ideal_length = Glyphs.defaults[key % "ideal_length"]
        self.length_influence = Glyphs.defaults[key % "length_influence"]
        self.first_letters = Glyphs.defaults[key % "first_letters"]
        self.other_letters = Glyphs.defaults[key % "other_letters"]
        self.prefix = Glyphs.defaults[key % "prefix"]
        self.suffix = Glyphs.defaults[key % "suffix"]
        self.cutoff_score = Glyphs.defaults[key % "cutoff_score"]

    def showWindow_(self, sender):
        """Do something like show a window"""
        print("show Windows")

    @objc.python_method
    def __file__(self):
        """Please leave this method unchanged"""
        return __file__
