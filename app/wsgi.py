from app import app
import core.configuration as configuration

if __name__ == "__main__":
  app.run(debug=configuration.DEBUG)