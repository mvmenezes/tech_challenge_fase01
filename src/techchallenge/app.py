from app import create_app
import logging, os

logging.basicConfig(filename=os.path.join(os.getcwd(),"src","techchallenge","data","output","logs_app.log"), level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

app = create_app()

port = int(os.environ.get("PORT", 5000))
if __name__ == "__main__":
    logging.info("Iniciando Aplicacao")
    app.run(debug=True, port=port)
