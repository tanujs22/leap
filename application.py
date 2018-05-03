from fal import app

application = app

if __name__ == '__main__':
	app.jinja_env.auto_reload = True
	app.config['TEMPLATES_AUTO_RELOAD'] = None
	app.run(threaded=True,debug=False,use_reloader=True)
