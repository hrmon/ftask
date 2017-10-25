# all the importsom flask import Flask, render_template
from models import db, Task
from flask import Flask, render_template
from views import taskapp
# initialize instance of WSGI application
# act as a central registry for the view functions, URL rules, template configs
app = Flask(__name__)
app.register_blueprint(taskapp)
## include db name in URI; _HOST entry overwrites all others
app.config['MONGODB_HOST'] = 'mongodb://localhost:27017'
app.config['MONGODB_SETTINGS'] = {'db':'ftask', 'alias':'default'} #necessary to set default alias
app.secret_key = "12345678"
app.debug = True

# initalize app with database
db.init_app(app)


if __name__ == "__main__":
    app.run()