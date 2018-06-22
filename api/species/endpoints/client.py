import io
import urllib.request as req

from flask import request
from flask_restplus import Resource
from api.restplus import api
from api.species.logic.tf_serving_client import make_prediction


# create dedicated namespace for model client
ns = api.namespace('species_client', description='Operations for Model client')


@ns.route('/prediction')
class CameraTrapPrediction(Resource):
    @ns.doc(description='Predict species images. ' +
            'Return the 5 most probable classe with their probabilities',
            responses={
                200: "Success",
                400: "Bad request",
                500: "Internal server error"
                })
    def post(self):
        try:
            req_data = request.get_json()
            print("got req_data: %s" % req_data)
            image_url_list = req_data['url']
            print("got url list: %s" % image_url_list)
            image_byte_list = list()
            for image_url in image_url_list:
                with req.urlopen(image_url) as url:
                    bytes = io.BytesIO(url.read())
                    image = bytes.getvalue()
                    image_byte_list.append(image)

        except Exception as inst:
            return {'message': 'something wrong with incoming request. ' +
                               'Original message: {}'.format(inst)}, 400

        try:
            results = make_prediction(image_byte_list)
            print("Results Are %s: " % results)
            # results is: [(1, 0.9343334436416626), (0, 0.06039385870099068), (2, 0.005272684618830681)]

            results_json = [{'class': res[0], 'prob': res[1]} for res in results]
            return {'prediction_result': results_json}, 200

        except Exception as inst:
            return {'message': 'internal error: {}'.format(inst)}, 500
