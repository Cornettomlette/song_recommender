from app import app
import logging as log
import os

# Configure log level
log.basicConfig(level=log.INFO)


if __name__ == "__main__":
    port = int(os.getenv('PORT', 8000))
    log.info(f"listening on port {port}")
    app.run(host='0.0.0.0', port=port)