from __future__ import annotations

from AppKit import NSNumberFormatter
from FontNameGenerator import FontNameGenerator
from vanilla import (
    Button,
    EditText,
    Group,
    PopUpButton,
    Slider,
    TextBox,
    Window,
)


class FontNameGeneratorWindow:
    def __init__(
        self,
        generator: FontNameGenerator | None = None,
        save_callback=None,
        generate_callback=None,
    ):
        self.w = Window(
            (300, 300),
            "WoLiBaFoNaGen",
            closable=True,
        )
        self.metrics = {
            "col": 110,
            "w": 120,
        }
        self.generator = generator

        # self.int_formatter = NSNumberFormatter.alloc().init()
        # self.int_formatter.setAllowsFloats_(False)
        # self.int_formatter.setMaximum_(50)
        # self.int_formatter.setMinimum_(0)
        # self.int_formatter.setPositiveFormat_("#")

        self._ui_wordlist()
        self._ui_first_letters()
        self._ui_other_letters()
        self._ui_min_max_length()
        self._ui_ideal_length()
        self._ui_length_influence()
        self._ui_affix()
        self._ui_buttons(save_callback, generate_callback)
        rules = [
            "H:|-[wordlist]-|",
            "H:|-[first_letters]-|",
            "H:|-[other_letters]-|",
            "H:|-[min_max_length]-|",
            "H:|-[ideal_length]-|",
            "H:|-[length_influence]-|",
            "H:|-[affix]-|",
            "H:|-[buttons]-|",
            (
                "V:|-[wordlist]-[first_letters]-[other_letters]-"
                "[min_max_length]-[ideal_length]-[length_influence]-"
                "[affix]-[buttons]-|"
            ),
        ]
        self.w.addAutoPosSizeRules(rules, self.metrics)

    def close(self):
        self.w.close()

    def open(self):
        self._set_values_from_generator()
        self.w.open()

    def _set_values_from_generator(self):
        if self.generator is None:
            return

        self.w.wordlist.selector.setItems(self.generator.word_lists)
        self.w.min_max_length.min_letters.set(self.generator.min_length)
        self.w.min_max_length.max_letters.set(self.generator.max_length)
        self.w.ideal_length.input.set(self.generator.ideal_length)
        self.w.length_influence.input.set(
            self.generator.length_influence * 100
        )
        self.w.first_letters.input.set(self.generator.first_letters)
        self.w.other_letters.input.set(self.generator.other_letters)
        self.w.affix.prefix.set(self.generator.prefix)
        self.w.affix.suffix.set(self.generator.suffix)

    def _ui_wordlist(self):
        self.w.wordlist = g = Group("auto")
        g.label = TextBox("auto", "Word List")
        g.selector = PopUpButton("auto", [])
        g.addAutoPosSizeRules(
            [
                "H:|[label(col)]-[selector(>=w)]|",
                "V:|[label]|",
                "V:|[selector]|",
            ],
            self.metrics,
        )

    def _ui_first_letters(self):
        self.w.first_letters = g = Group("auto")
        g.label = TextBox("auto", "First Letters")
        g.input = EditText("auto", "")
        g.addAutoPosSizeRules(
            [
                "H:|[label(col)]-[input(>=w)]|",
                "V:|[label]|",
                "V:|[input]|",
            ],
            self.metrics,
        )

    def _ui_other_letters(self):
        self.w.other_letters = g = Group("auto")
        g.label = TextBox("auto", "Other Letters")
        g.input = EditText("auto", "")
        g.addAutoPosSizeRules(
            [
                "H:|[label(col)]-[input(>=w)]|",
                "V:|[label]|",
                "V:|[input]|",
            ],
            self.metrics,
        )

    def _ui_min_max_length(self):
        self.w.min_max_length = g = Group("auto")
        g.label = TextBox("auto", "Min/Max Length")
        g.min_letters = EditText("auto", "4")
        g.max_letters = EditText("auto", "12")
        g.addAutoPosSizeRules(
            [
                "H:|[label(col)]-[min_letters(40)]-[max_letters(40)]-|",
                "V:|[label]|",
                "V:|[min_letters]|",
                "V:|[max_letters]|",
            ],
            self.metrics,
        )

    def _ui_ideal_length(self):
        self.w.ideal_length = g = Group("auto")
        g.label = TextBox("auto", "Ideal Length")
        g.input = EditText("auto", "5")
        g.addAutoPosSizeRules(
            [
                "H:|[label(col)]-[input(>=w)]|",
                "V:|[label]|",
                "V:|[input]|",
            ],
            self.metrics,
        )

    def _ui_length_influence(self):
        self.w.length_influence = g = Group("auto")
        g.label = TextBox("auto", "Length Influence")
        g.input = Slider(
            "auto", value=25, minValue=0, maxValue=100, sizeStyle="small"
        )
        g.addAutoPosSizeRules(
            [
                "H:|[label(col)]-[input(>=w)]|",
                "V:|[label]|",
                "V:|[input]|",
            ],
            self.metrics,
        )

    def _ui_affix(self):
        self.w.affix = g = Group("auto")
        g.label = TextBox("auto", "Prefix/Suffix")
        g.prefix = EditText("auto", "")
        g.suffix = EditText("auto", "Pro")
        g.addAutoPosSizeRules(
            [
                "H:|[label(col)]-[prefix(40)]-[suffix(40)]|",
                "V:|[label]|",
                "V:|[prefix]|",
                "V:|[suffix]|",
            ],
            self.metrics,
        )

    def _ui_buttons(self, save_callback, generate_callback):
        self.w.buttons = g = Group("auto")
        g.save = Button("auto", "Save Settings", callback=save_callback)
        g.addAutoPosSizeRules(
            [
                "H:|[save]|",
                "V:|[save]|",
            ],
            self.metrics,
        )


if __name__ == "__main__":
    FontNameGeneratorWindow()
