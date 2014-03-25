import sae
from ReverseProxy import wsgi

application = sae.create_wsgi_app(wsgi.application)