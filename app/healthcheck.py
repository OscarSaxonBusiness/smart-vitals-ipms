"""Used by Docker's health check: exits with an error if the API does not answer GET /health."""
import os
import urllib.request

urllib.request.urlopen(f"http://localhost:{os.environ.get('PORT', 8000)}/health", timeout=3)
