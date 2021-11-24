from app import create_app
from waitress import serve

app = create_app()
#serve(app, host='0.0.0.0', port=8080, threads=1)
app.run()