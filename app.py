from flask import Flask,jsonify,request,render_template
from miniproject3 import codingplagiarismcheck
import warnings
warnings.filterwarnings("ignore")
app = Flask(__name__)

@app.route('/predict',methods=['POST'])
def predict():
    #1 - Java , 2 - Python , 3 - C
    data = request.get_json(force=True)
    print('data:',data)
    check = int(data['checked'])
    print(check)
    results = codingplagiarismcheck(check)
    #print(results)
    return jsonify(results), 200, {'Content-Type':'application/json'}

if __name__=='__main__':
    app.run(host='0.0.0.0',port=3000,debug=True)