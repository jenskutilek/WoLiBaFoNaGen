from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
includeFiles = [
	"japanese.txt",
	"movie-characters.txt",
	"music-classical.txt",
	"music-country.txt",
	"music-jazz.txt",
	"rock-groups.txt",
	"swahili.txt",
	"tolkien.txt",
	"wordsDan.txt",
	"wordsEn.txt",
	"wordsNld.txt",
	"yiddish.txt",
]
buildOptions = dict(packages = [], excludes = [], include_files = includeFiles)


import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('WoLiBaFoNaGen.py', base=base)
]

setup(name='WoLiBaFoNaGen',
      version = '0.1',
      description = 'Word List Based Font Name Generator',
      options = dict(build_exe = buildOptions),
      executables = executables)
