from __future__ import annotations

from random import choice
import objc

from AppKit import NSMenuItem
from GlyphsApp import (
    DOCUMENTOPENED,
    EDIT_MENU,
    WINDOW_MENU,
    AskString,
    Glyphs,
    Message,
)
from GlyphsApp.plugins import GeneralPlugin

from FontNameGenerator import FontNameGenerator
from FontNameGeneratorWindow import FontNameGeneratorWindow


key = "de.kutilek.glyphs.WoLiBaFoNaGen.%s"

defaults = {
    "word_list": "English",
    "min_length": 3,
    "max_length": 12,
    "ideal_length": 4,
    "length_influence": 0.25,
    "first_letters": "CEFGKRS",
    "other_letters": "cefgrskya",
    "prefix": "",
    "suffix": "",
    # "cutoff_score": 0.3,
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
        newMenuItem = NSMenuItem(self.name, self.showWindow_)
        Glyphs.menu[WINDOW_MENU].append(newMenuItem)

        # Initialize the parameters
        self.word_list: str | None = None
        self.min_length: int | None = None
        self.max_length: int | None = None
        self.ideal_length: int | None = None
        self.length_influence: float | None = None
        self.first_letters: str | None = None
        self.other_letters: str | None = None
        self.prefix: str | None = None
        self.suffix: str | None = None
        # self.cutoff_score: float | None = None
        self.fng = FontNameGenerator()
        self.load_defaults()
        self.window = None
        Glyphs.addCallback(self.autoFillName_, DOCUMENTOPENED)

    @objc.python_method
    def random_name(self) -> str:
        _, _, score_words = self.fng.get_filtered_words()
        scores = sorted(score_words, reverse=True)[: min(10, len(score_words))]
        # print(scores)
        score = choice(scores)
        # print(score_words[score])
        # score = scores[0]
        name, _, _ = choice(score_words[score])
        return f"{self.fng.prefix}{name.title()}{self.fng.suffix}"

    def saveSettings_(self, sender=None) -> None:
        # Update the settings from the window and save them to defaults
        if self.window is None:
            return
        for k, v in {
            "word_list": self.window.w.wordlist.selector.getItem(),
            "min_length": int(self.window.w.min_max_length.min_letters.get()),
            "max_length": int(self.window.w.min_max_length.max_letters.get()),
            "ideal_length": int(self.window.w.ideal_length.input.get()),
            "length_influence": self.window.w.length_influence.input.get()
            / 100,
            "first_letters": self.window.w.first_letters.input.get(),
            "other_letters": self.window.w.other_letters.input.get(),
            "prefix": self.window.w.affix.prefix.get(),
            "suffix": self.window.w.affix.suffix.get(),
        }.items():
            # print(k, v, type(v))
            setattr(self.fng, k, v)
        # self.window.close()
        # self.window = None
        self.save_defaults()

    @objc.python_method
    def load_defaults(self) -> None:
        # print("Loading")
        for k, v in defaults.items():
            saved = Glyphs.defaults[key % k]
            setattr(self.fng, k, saved or v)
            # print(f"{key % k}: {k} ({type(k)}): {getattr(self.fng, k)}")

    @objc.python_method
    def save_defaults(self) -> None:
        # print("Saving")
        for k in defaults.keys():
            Glyphs.defaults[key % k] = getattr(self.fng, k)
            # print(f"{key % k}: {k} ({type(k)}): {getattr(self.fng, k)}")

    def autoFillName_(self, sender) -> None:
        """Fill in a random name following the current rules"""
        doc = sender.object()
        if doc.font.familyName == "New Font":
            if doc.filePath is None:
                doc.font.familyName = self.random_name()

    def showWindow_(self, sender) -> None:
        """Do something like show a window"""
        self.window = FontNameGeneratorWindow(
            generator=self.fng, save_callback=self.saveSettings_
        )
        self.window.open()

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
            if Glyphs.font is None:
                Message(
                    "To use the name, you need to open a file first.",
                    "WoLiBaFoNaGen",
                    "Nevermind",
                )
            else:
                Glyphs.font.familyName = name

    @objc.python_method
    def __file__(self):
        """Please leave this method unchanged"""
        return __file__
