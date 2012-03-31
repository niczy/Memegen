dev: 
	dev_appserver.py .

link:
	ln -s ../vendors static/vendors
	ln -s ../scripts static/js

unlink:
	unlink static/vendors
	unlink static/js



