import io
import json
import urllib.request as req

from flask import request
from flask_restplus import Resource
from api.restplus import api
from api.gan.logic.tf_serving_client import make_prediction
from werkzeug.datastructures import FileStorage


# create dedicated namespace for model client
ns = api.namespace('model_client', description='Operations for Model client')

# Flask-RestPlus specific parser for image uploading
UPLOAD_KEY = 'image'
UPLOAD_LOCATION = 'files'
upload_parser = api.parser()
upload_parser.add_argument(UPLOAD_KEY,
                           location=UPLOAD_LOCATION,
                           type=FileStorage,
                           required=True)


@ns.route('/prediction')
class GanPrediction(Resource):
    @ns.doc(description='Predict camera trap images. ' +
            'Return 3 most probable classes with their probabilities',
            responses={
                200: "Success",
                400: "Bad request",
                500: "Internal server error"
                })
    @ns.expect(upload_parser)
    def post(self):
        try:
            req_data = request.get_json()
            print("got req_data: %s" req_data)
            image_url = req_data['url']
            print("got url: %s" image_url)
            with req.urlopen(image_url) as url:
                image = io.BytesIO(url.read())
        except Exception as inst:
            return {'message': 'something wrong with incoming request. ' +
                               'Original message: {}'.format(inst)}, 400

        try:
            results = make_prediction(image.read())
            results_json = [{'digit': res[0], 'probability': res[1]} for res in results]
            return {'prediction_result': results_json}, 200

        except Exception as inst:
            return {'message': 'internal error: {}'.format(inst)}, 500
