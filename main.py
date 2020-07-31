from flask import Flask, request
from flask_restful import Api, Resource, reqparse, abort
from nlp import processQuery
app = Flask(__name__)
api = Api(app)


args = reqparse.RequestParser()
args.add_argument("input", type=str, help="User input is required", required=True);

content = [
    {
        "Case" : "People v. Martin",
        "Tags" : ["assault", "battery"],
        "State" : "Illinois"
    },
    {
        "Case" : "State v. Skeels",
        "Tags" : ["murder", "homicide", "kidnapping", "robbery"],
        "State" : "North Carolina"
    },
    {
        "Case" : "State v. Ripley",
        "Tags" : ["robbery", "kidnapping"],
        "State" : "North Carolina"
    },
    {
        "Case" : "State v. Cole",
        "Tags" : ["robbery", "kidnapping"],
        "State" : "North Carolina"
    },
    {
        "Case" : "State v. Moore",
        "Tags" : ["robbery", "kidnapping"],
        "State" : "North Carolina"
    },
    {
        "Case" : "State v. Burris",
        "Tags" : ["assault", "battery"],
        "State" : "North Carolina"
    },
    {
        "Case" : "State v. Barksdale",
        "Tags" : ["robbery"],
        "State" : "North Carolina"
    },
    {
        "Case" : "State v. Allen",
        "Tags" : ["robbery"],
        "State" : "North Carolina"
    },
]


class Query(Resource):
        def getBest(self, query):
                most = 0
                idx = 0
                itr = 0
                for case in content:
                        var = 0
                        for tag in case["Tags"]:
                                for row in query:
                                        for col in row:
                                                if col.lower() == tag.lower():
                                                        var += 1
                                                        print("{} is the same as {}".format(col.lower(), tag.lower()))
                        var /= len(case["Tags"])
                        if var > most:
                                most = var
                                idx = itr
                        itr += 1
                return content[idx]

                                

        def get(self):
                argv = args.parse_args()
                user_input = argv['input']
                query = processQuery(user_input)
                result = self.getBest(query)
                
                return {"Best Case" : result}
        
        
api.add_resource(Query, "/query/")

@app.route("/")
def home():
        return "Project 614 App"
if __name__ == "__main__":
        app.run(debug=True)