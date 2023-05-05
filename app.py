from flask import Flask,jsonify,request,render_template
from miniproject3 import codingplagiarismcheck
import warnings
warnings.filterwarnings("ignore")
app = Flask(__name__)

@app.route('/predict',methods=['POST'])
def predict():
    data = request.get_json(force=True)
    #results = []
    #for i in data:
        #results.append(data[i])
    #print(type(data))
    #print(results)
    results = codingplagiarismcheck()
    print(results)
    return jsonify(results), 200, {'Content-Type':'application/json'}

if __name__=='__main__':
    app.run(host='0.0.0.0',port=3000,debug=True)