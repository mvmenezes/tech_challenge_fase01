import logging
import os
from src.techchallenge.app.create import create_app

apps = create_app()
port = int(os.environ.get("PORT", 5007))
logging.basicConfig(filename=os.path.join(os.getcwd(),"src","techchallenge","data","output","logs_app.log"), level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

if __name__ == "__main__":
    logging.info("Iniciando Aplicacao")
    apps.run(debug=True, port=port)
