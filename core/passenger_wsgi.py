from a2wsgi import ASGIMiddleware
from api import app

application = ASGIMiddleware(app)
