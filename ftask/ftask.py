# all the importsom flask import Flask, render_template
from .models import db
from flask import Flask, render_template
# initialize instance of WSGI application
# act as a central registry for the view functions, URL rules, template configs
app = Flask(__name__)

## include db name in URI; _HOST entry overwrites all others
app.config['MONGODB_HOST'] = 'mongodb://localhost:27017'
app.debug = True

# initalize app with database
db.init_app(app)


@app.route("/")
def index():
    print("hello!")


if __name__ == "__main__":
    app.run()