from flask_app.__init__ import app
from flask_app.controllers import login_register
from flask_app.controllers import home
from flask_app.controllers import account
from flask_app.controllers import movie


if __name__ == '__main__':
    app.run(debug=True)