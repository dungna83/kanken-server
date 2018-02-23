from flask import Flask, request
from flask_restful import reqparse, abort, Api, Resource

from tegaki.character import Character
from tegaki.recognizer import Recognizer

VERSION = '0.1'

app = Flask(__name__)
api = Api(app)

parser = reqparse.RequestParser()
parser.add_argument('task')

# HelloWorld
class HelloWorld(Resource):
    def get(self):
        return {'data': 'recognize API ver 0.1'}
api.add_resource(HelloWorld, '/')

# TegakiRecognizeError
class TegakiRecognizeError(Exception):
    pass

# Recognizer
class Recognize(Resource):
    def get(self):
        xmlFile = "test_data/39365.xml"
        recognizer = "zinnia"
        model = "Japanese"

        char = Character()
        char.read(xmlFile)
        writing = char.get_writing()

        recognizers = Recognizer.get_available_recognizers()

        if not recognizer in recognizers:
            raise TegakiRecognizeError, "Not an available recognizer."

        recognizer_klass = recognizers[recognizer]
        recognizer = recognizer_klass()

        models = recognizer_klass.get_available_models()

        if not model in models:
            raise TegakiRecognizeError, "Not an available model."

        recognizer.set_model(model)

        return {'data': recognizer.recognize(writing)}
    def post(self):
        xmlFile = request.files['file']
        recognizer = "zinnia"
        model = "Japanese"

        char = Character()
        char.read(xmlFile)
        writing = char.get_writing()

        recognizers = Recognizer.get_available_recognizers()

        if not recognizer in recognizers:
            raise TegakiRecognizeError, "Not an available recognizer."

        recognizer_klass = recognizers[recognizer]
        recognizer = recognizer_klass()

        models = recognizer_klass.get_available_models()

        if not model in models:
            raise TegakiRecognizeError, "Not an available model."

        recognizer.set_model(model)

        return {'data': recognizer.recognize(writing)}
api.add_resource(Recognize, '/recognize')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

