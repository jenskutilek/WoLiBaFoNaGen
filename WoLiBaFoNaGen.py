from wx import App
from WoLiBaFoNaGenWX import FNGFrame, ui_width, ui_height
from sys import exit

if __name__ == '__main__':
    app = App()
    main = FNGFrame(
        None,
        title = "WoLiBaFoNaGen",
        size = (ui_width, ui_height),
    )
    main.Show()
    app.MainLoop()

exit(1)
