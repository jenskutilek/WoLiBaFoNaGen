# WoLiBaFoNaGen
Word List Based Font Name Generator

![](https://github.com/jenskutilek/WoLiBaFoNaGen/blob/master/images/screenshot-mac.png)

The generator uses the wxPython UI library. So if you don’t have it installed already, you need to install it before you can run WoLiBaFoNaGen:

```bash
$ pip --user install wx
```

Run:

```bash
$ python WoLiBaFoNaGen.py
```

Build the Mac app:

```bash
$ pip install --user --ignore-installed py2app
$ python setup.py py2app
```

Build the Windows app:

```bash
$ pip install cx_Freeze
$ python cxsetup.py build
```

On Windows, [some additional DLLs](http://cx-freeze.readthedocs.io/en/latest/faq.html#microsoft-visual-c-redistributable-package) may be required to run the "frozen" version of the app. 
