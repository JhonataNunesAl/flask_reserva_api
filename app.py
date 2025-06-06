from config import app, db
from controllers.salasCONTROLLER import salas_blueprint
from flasgger import Swagger

def create_app():
    app.register_blueprint(salas_blueprint, url_prefix='/api')
    Swagger(app)
    with app.app_context(): 
        db.create_all()

    return app

if __name__ == '__main__':
    # ELE SÓ VAI INICIAR SE TODOS OS BLUEPRINTS INICIAREM TAMBÉM!!!
    app = create_app()  
    app.run(host=app.config["HOST"], port=app.config['PORT'], debug=app.config['DEBUG'])