import os
from config import web, app


if __name__ == "__main__":
    web.run_app(app, port=int(os.getenv('PORT', 8080)))
