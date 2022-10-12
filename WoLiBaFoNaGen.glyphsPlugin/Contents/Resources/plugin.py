from __future__ import annotations

from random import choice
import objc

from AppKit import NSMenuItem
from GlyphsApp import DOCUMENTOPENED, EDIT_MENU, WINDOW_MENU, Glyphs, AskString
from GlyphsApp.plugins import GeneralPlugin

key = "de.kutilek.glyphs.WoLiBaFoNaGen.%s"

defaults = {
    "word_list_name": "English",
    "min_length": 3,
    "max_length": 12,
    "ideal_length": 4,
    "length_influence": 0.25,
    "first_letters": "CEFGKRS",
    "other_letters": "cefgrskya",
    "prefix": "",
    "suffix": "",
    "cutoff_score": 0.3,
}


class WoLiBaFoNaGen(GeneralPlugin):
    @objc.python_method
    def settings(self) -> None:
        self.name = Glyphs.localize(
            {
                "en": "WoLiBaFoNaGen",
            }
        )

    @objc.python_method
    def start(self) -> None:
        newMenuItem = NSMenuItem(
            Glyphs.localize(
                {
                    "de": "Neuen Schriftnamen vorschlagen",
                    "en": "Suggest New Font Name",
                }
            ),
            self.suggestName_,
        )
        Glyphs.menu[EDIT_MENU].append(newMenuItem)
        # newMenuItem = NSMenuItem(self.name, self.showWindow_)
        # Glyphs.menu[WINDOW_MENU].append(newMenuItem)

        # Initialize the parameters
        self.word_list_name: str | None = None
        self.min_length: int | None = None
        self.max_length: int | None = None
        self.ideal_length: int | None = None
        self.length_influence: float | None = None
        self.first_letters: str | None = None
        self.other_letters: str | None = None
        self.prefix: str | None = None
        self.suffix: str | None = None
        self.cutoff_score: float | None = None
        self.load_defaults()
        Glyphs.addCallback(self.autoFillName_, DOCUMENTOPENED)

    @objc.python_method
    def random_name(self) -> str:
        from FontNameGenerator import FontNameGenerator, word_lists

        fg = FontNameGenerator(
            word_lists=word_lists,
            word_list=self.word_list_name,
            min_length=self.min_length,
            max_length=self.max_length,
            ideal_length=self.ideal_length,
            length_influence=self.length_influence,
            first_letters=self.first_letters,
            other_letters=self.other_letters,
            prefix=self.prefix,
            suffix=self.suffix,
            cutoff_score=self.cutoff_score,
        )
        _, _, score_words = fg.get_filtered_words()
        scores = sorted(score_words, reverse=True)[: min(10, len(score_words))]
        score = choice(scores)
        name, _, _ = choice(score_words[score])
        return name.title()

    @objc.python_method
    def load_defaults(self) -> None:
        for k, v in defaults.items():
            saved = Glyphs.defaults[key % k]
            setattr(self, k, saved or v)

    @objc.python_method
    def save_defaults(self) -> None:
        for k in defaults.keys():
            Glyphs.defaults[key % k] = getattr(self, k)

    def autoFillName_(self, sender) -> None:
        """Fill in a random name following the current rules"""
        doc = sender.object()
        if doc.font.familyName == "New Font":
            if doc.filePath is None:
                doc.font.familyName = self.random_name()

    def showWindow_(self, sender) -> None:
        """Do something like show a window"""
        print("show Windows")

    def suggestName_(self, sender) -> None:
        """Show a random name following the current rules"""
        name = self.random_name()
        ok = AskString(
            "We found a nice name for your font:",
            name,
            "WoLiBaFoNaGen",
            "Use This Name",
        )
        if ok:
            Glyphs.font.familyName = name

    @objc.python_method
    def __file__(self):
        """Please leave this method unchanged"""
        return __file__
