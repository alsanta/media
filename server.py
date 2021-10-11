from flask_app import app
from flask_app.controllers import login_register
from flask_app.controllers import media

if __name__=="__main__":
    app.run(debug=True)