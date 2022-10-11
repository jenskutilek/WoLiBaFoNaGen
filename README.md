# WoLiBaFoNaGen

Word List Based Font Name Generator

![](https://github.com/jenskutilek/WoLiBaFoNaGen/blob/master/images/screenshot-mac.png)

## Development

Install the dependencies before you can run or build WoLiBaFoNaGen, preferably
in a virtual environment:

```bash
$ python3 -m venv venv
$ source venv/bin/activate
$ pip install -r requirements-dev.txt
```

Run:

```bash
$ python3 WoLiBaFoNaGen.py
```

Build and debug as a Mac app:

```bash
$ make debug
```

Build the Mac app for distribution:

```bash
$ make dist
```

## Outdated information

### Windows

Those instructions have not been updated for Python 3 yet.

Build the Windows app:

```bash
$ pip install cx_Freeze
$ python cxsetup.py build
```

On Windows, [some additional DLLs](http://cx-freeze.readthedocs.io/en/latest/faq.html#microsoft-visual-c-redistributable-package) may be required to run the "frozen" version of the app. 
