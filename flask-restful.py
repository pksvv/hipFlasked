from flask import Flask, request, jsonify
from flask_restful import Resource, Api
import logging

app = Flask(__name__)
api = Api(app)

logging.basicConfig(level="DEBUG")
logger = logging.getLogger(__name__)

items = []

class Item(Resource):

    def get(self,name):
        item = next(filter(lambda x: x["name"]==name,items),None)
        return {"item":item}, 200 if item else 404
    
    def post(self,name):
        if next(filter(lambda x: x["name"]==name, items),None) is not None:
            return {"message":f"The item with name {name} already exists"}, 400
        
        payload = request.get_json()

        logging.debug("Payload: {}".format(payload))

        item = {"name":name, "price":payload["price"]}
        items.append(item)

        return item,401
    
class itemsList(Resource):
    def get(self):
        logging.debug("Inside getItems")
        return {"items":items}

api.add_resource(Item,"/item/<string:name>")
api.add_resource(itemsList,"/items")

if __name__ == "__main__":
    app.run(port=5000)