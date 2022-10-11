import wx
import wx.grid
from wx.lib.pubsub import pub
from sys import platform

from FontNameGenerator import *

if platform == 'win32':
    ui_width = 264
    ui_height = 290
else:
    ui_width = 252
    ui_height = 254


class FNGFrame(wx.Frame):
    """
    The main frame
    """

    def __init__(self, *args, **kw):
        # ensure the parent's __init__ is called
        super(FNGFrame, self).__init__(*args, **kw)

        self.SetSizeHints(ui_width, ui_height, ui_width, ui_height)

        # create a panel in the frame
        pnl = wx.Panel(self)

        x = 8
        col = 120
        box_height = 21
        box_width = 120
        yskip = 25

        y = 12

        word_list_selector_label = wx.StaticText(
            pnl,
            label = "Word List",
            pos = (x, y),
        )
        self.word_list_selector = wx.ComboBox(
            pnl,
            pos = (col, y - 4),
            size = (box_width, 26),
            choices = sorted(word_lists.keys()),
        )


        y += yskip
        first_letters_label = wx.StaticText(
            pnl,
            label = "First Letters",
            pos = (x, y)
        )

        self.first_letters  = wx.TextCtrl(
            pnl,
            value = "ACDFGRSTY",
            pos = (col, y - 2),
            size = (box_width, box_height),
        )

        y += yskip
        other_letters_label = wx.StaticText(
            pnl,
            label = "Other Letters",
            pos = (x, y),
        )
        self.other_letters  = wx.TextCtrl(
            pnl,
            value = "aeglnrst",
            pos = (col, y - 2),
            size = (box_width, box_height),
        )

        y += yskip
        length_label = wx.StaticText(pnl, label="Min/Max Length", pos=(x, y))
        self.min_length  = wx.TextCtrl(
            pnl,
            value = "4",
            pos = (col, y - 2),
            size = (box_width/2 - 5, box_height),
            style = wx.TE_RIGHT,
        )
        self.max_length  = wx.TextCtrl(
            pnl,
            value = "12",
            pos = (col + box_width/2 + 5, y - 2),
            size = (box_width/2 - 5, box_height),
            style = wx.TE_RIGHT,
        )

        y += yskip
        ideal_length_label = wx.StaticText(pnl, label="Ideal Length", pos=(x, y))
        self.ideal_length  = wx.TextCtrl(
            pnl,
            value = "5",
            pos = (col, y - 2),
            size = (box_width, box_height),
            style = wx.TE_RIGHT,
        )

        y += yskip
        length_influence_label = wx.StaticText(pnl, label="Length Influence", pos=(x, y))
        self.length_influence = wx.Slider(
            pnl,
            value = 25,
            minValue = 0,
            maxValue = 100,
            pos = (col, y),
            size = (box_width, box_height),
        )

        y += yskip
        affix_label = wx.StaticText(pnl, label="Prefix/Suffix", pos=(x, y))
        self.prefix  = wx.TextCtrl(
            pnl,
            value = "",
            pos = (col, y - 2),
            size = (box_width/2 - 5, box_height),
        )
        self.suffix  = wx.TextCtrl(
            pnl,
            value = "Pro",
            pos = (col + box_width/2 + 5, y - 2),
            size = (box_width/2 - 5, box_height),
        )

        y += int(round(1.5 * yskip))
        generate_button = wx.Button(
            pnl,
            label = "Generate",
            pos = (col, y),
            size = (box_width, box_height),
        )
        generate_button.Bind(wx.EVT_BUTTON, self.OnGenerate)

        # create a menu bar
        self.makeMenuBar()

        # and a status bar
        #self.CreateStatusBar()
        #self.SetStatusText("Welcome to wxPython!")

        # Keep track of grid window, subscribe to its messages
        self.grid_is_open = False
        pub.subscribe(self.mainListener, "mainListener")

        self.fng = FontNameGenerator(
            word_lists,
            word_list = selected_word_list,
            min_length = int(self.min_length.GetValue()),
            max_length = int(self.max_length.GetValue()),
            ideal_length = int(self.ideal_length.GetValue()),
            length_influence = 0.01 * int(self.length_influence.GetValue()),
            first_letters = self.first_letters.GetValue(),
            other_letters = self.other_letters.GetValue(),
            prefix = self.prefix.GetValue(),
            suffix = self.suffix.GetValue(),
            cutoff_score = cutoff_score,
        )
        self.word_list_selector.SetValue(selected_word_list)
        self.Bind(wx.EVT_CLOSE, self.OnClose)


    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()
        # The "\t..." syntax defines an accelerator key that also triggers
        # the same event
        newItem = fileMenu.Append(-1, "&New\tCtrl-N",
                "New name list")
        saveItem = fileMenu.Append(-1, "&Save...\tCtrl-S",
                "Save the current name list")
        fileMenu.AppendSeparator()
        # When using a stock ID we don't need to specify the menu item's
        # label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        editMenu = wx.Menu()
        generateItem = editMenu.Append(-1, "&Generate\tCtrl-G",
            "Generate a name list with the current settings")
        copyItem = editMenu.Append(-1, "&Copy Names\tCtrl-C",
            "Copy the name list")

        # Now a help menu for the about item
        #helpMenu = wx.Menu()
        #aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # platforms that support it those letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(editMenu, "&Edit")
        #menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally, associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnNew, newItem)
        self.Bind(wx.EVT_MENU, self.OnSave, saveItem)
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self.OnGenerate, generateItem)
        self.Bind(wx.EVT_MENU, self.OnCopy, copyItem)
        #self.Bind(wx.EVT_MENU, self.OnAbout, aboutItem)


    def GenerateWords(self):
        #word_lists
        self.fng.word_list = self.word_list_selector.GetValue()
        self.fng.min_length = int(self.min_length.GetValue())
        self.fng.max_length = int(self.max_length.GetValue())
        self.fng.ideal_length = int(self.ideal_length.GetValue())
        self.fng.length_influence = 0.01 * int(self.length_influence.GetValue())
        self.fng.first_letters = self.first_letters.GetValue()
        self.fng.other_letters = self.other_letters.GetValue()
        self.fng.prefix = self.prefix.GetValue()
        self.fng.suffix = self.suffix.GetValue()
        #self.fng.cutoff_score = self.cutoff_score
        prefix, suffix, word_dict = self.fng.get_filtered_words()
        return prefix, suffix, {score: [word[0] for word in words] for score, words in word_dict.items()}


    def OnGenerate(self, event):
        if not self.grid_is_open:
            result_frame = GridFrame()
            result_frame.Show()
            if result_frame:
                self.grid_is_open = True
            else:
                self.grid_is_open = False
        if self.grid_is_open:
            p, s, self.word_dict = self.GenerateWords()
            pub.sendMessage("gridListener", message = (p, s, self.word_dict))


    def OnNew(self, event):
        # TODO: If the user closed the main window, open a new one.
        pass


    def OnCopy(self, event):
        if not wx.TheClipboard.IsOpened():
            wx.TheClipboard.Open()
            rows = 100
            words = []
            i = 0
            for score in sorted(self.word_dict.keys(), reverse = True):
                #words.append("%0.3f" % score)
                for word in self.word_dict[score]:
                    words.append("%s%s%s" % (self.fng.prefix, word.title(), self.fng.suffix))
                    i += 1
                    if i >= rows:
                        break
            word_string = "\n".join(words)
            do = wx.TextDataObject()
            do.SetText(word_string)
            success = wx.TheClipboard.SetData(do)
            wx.TheClipboard.Close()

    def OnClose(self, event):
        pub.sendMessage("gridListener", message = "closing")
        self.Destroy()

    def OnExit(self, event):
        """Close the frame, terminating the application."""
        pub.sendMessage("gridListener", message = "closing")
        self.Close(True)


    def OnSave(self, event):
        """Save the current list"""
        wx.MessageBox("Hello again from wxPython")


    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("Word List Based Font Name Generator",
                      u"",
                      wx.OK|wx.ICON_INFORMATION)


    def mainListener(self, message):
        if message == "closing":
            self.grid_is_open = False




class GridFrame(wx.Frame):

    def __init__(self):
        if platform == 'win32':
            ui_width = 312
            ui_height = 400
        else:
            ui_width = 300
            ui_height = 400
        
        super(GridFrame, self).__init__(None, wx.ID_ANY, "Results", size=(ui_width, ui_height))

        self.SetSizeHints(ui_width, ui_height)

        self.grid = wx.grid.Grid(self, -1)
        self.grid.CreateGrid(100, 2)
        self.grid.SetColSize(0, 60)
        #self.grid.SetColFormatFloat(0, 6, 2)
        self.grid.SetColSize(1, 142)
        #grid.SetCellValue(0, 1, 'wxGrid is good')
        self.grid.SetColLabelValue(0, "Score")
        self.grid.SetColLabelValue(1, "Name")
        pub.subscribe(self.gridListener, "gridListener")
        self.Bind(wx.EVT_CLOSE, self.OnClose)
        

    def OnClose(self, event):
        pub.sendMessage("mainListener", message = "closing")
        self.Destroy()


    def gridListener(self, message):
        if message == "closing":
            self.Close(True)
        else:
            prefix, suffix, word_dict = message
            self.grid.ClearGrid()
            i = 0
            rows = self.grid.GetNumberRows()
            for score in sorted(word_dict.keys(), reverse = True):
                if i >= rows:
                    break
                self.grid.SetCellValue(i, 0, "%0.3f" % score)
                for word in word_dict[score]:
                    self.grid.SetCellValue(i, 1, "%s%s%s" % (prefix, word.title(), suffix))
                    i += 1
                    if i >= rows:
                        break



if __name__ == '__main__':
    app = wx.App()
    main = FNGFrame(
        None,
        title = "WoLiBaFoNaGen",
        size = (ui_width, ui_height),
    )
    main.Show()
    app.MainLoop()
