dev: 
	dev_appserver.py .

bootstrap:
	ln -s ../../vendors/bootstrap/css/bootstrap.css static/css/bootstrap.css
	ln -s ../../vendors/bootstrap/js/bootstrap.js static/js/bootstrap.js

cleanbootstrap:
	unlink static/css/bootstrap.css
	unlink static/js/bootstrap.js

