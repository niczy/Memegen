dev: 
	dev_appserver.py .

link:
	ln -s ../vendors static/vendors
	ln -s ../scripts static/js
	ln -s ../styles static/css

unlink:
	unlink static/vendors
	unlink static/js
	unlink static/css



