# run.py (à la racine)
from web.app import create_app

if __name__ == '__main__':
    app = create_app()
    
    with app.app_context():
        from database import init_database
        init_database()
    
    app.run(debug=True, port=5000, host='0.0.0.0')