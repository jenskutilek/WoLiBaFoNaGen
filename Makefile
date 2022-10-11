FW=dist/WoLiBaFoNaGen.app/Contents/Frameworks/
WX=dist/WoLiBaFoNaGen.app/Contents/Resources/lib/python3.10/lib-dynload/wx/

.PHONY: dist
dist: *.py *.txt # Resources/WoLiBaFoNaGen.icns
	# python3 version.py
	# python3 setup.py py2app --iconfile Resources/WoLiBaFoNaGen.icns -O2
	python3 setup.py py2app -O2
	# ./fix.symlinks.sh


debug: *.py *.txt # Resources/WoLiBaFoNaGen.icns
	# python3 setup.py py2app --iconfile Resources/WoLiBaFoNaGen.icns -A
	python3 setup.py py2app -A
	./dist/WoLiBaFoNaGen.app/Contents/MacOS/WoLiBaFoNaGen


# Resources/WoLiBaFoNaGen.icns:
# 	iconutil -c icns --output Resources/WoLiBaFoNaGen.icns WoLiBaFoNaGen.iconset/


.PHONY: venv
venv:
	python3 -m venv venv


.PHONY: dist-clean
dist-clean: clean
	rm -rf venv
	find . -type f -name *.pyc -exec rm "{}" \;


.PHONY: clean
clean:
	rm -rf build/ dist/


.PHONY: fix-links
fix-links: dist
	./fix.symlinks.sh
