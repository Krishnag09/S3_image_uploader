from flask import Flask
from flask_restful import Api
from fileuploader.api.routes import initialize_routes
from fileuploader import create_app


app = create_app()

if __name__ == "__main__":
    
    app.run(debug=True)
