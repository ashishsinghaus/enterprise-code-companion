from flask import Flask, jsonify, request
from elm import code_suggest

 
# instance of flask application
app = Flask(__name__)
 
# home route that returns below text when root url is accessed
@app.route("/")
def suggestion():
    return code_suggest()
 
if __name__ == '__main__': 
   app.run()
