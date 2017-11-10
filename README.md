# WoLiBaFoNaGen
WordListBasedFontNameGenerator

Run:

```bash
$ python WoLiBaFoNaGen.py
```

Build the Mac app:

```bash
$ pip install --user --ignore-installed py2app
$ pip install wx
$ python setup.py py2app
```

Build the Windows app:

```bash
$ pip install wx cx_Freeze
$ python cxsetup.py build
```
