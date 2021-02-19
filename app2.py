# import Flask and jsonify
from flask import render_template, Flask, jsonify, request, make_response
# import Resource, Api and reqparser
from flask_restful import Resource, Api, reqparse
import pandas as pd
import numpy as np
import pickle



app = Flask(__name__)
api = Api(app)

with open('myfile.pickle', 'rb') as file_handle:
    pipeline = pickle.load(file_handle)

@app.route('/')
def home():
   return render_template('index.html',  prediction_text="")

class predict(Resource):
    #@app.route('/predict',methods=['POST'])
    def post(self):
        # create request parser
        #data = request.get_json(force=True)
        data = request.form
        predict_request = [data['Gender'], data['Married'], data['Dependents'], data['Education'], data['Self_Employed'], data['ApplicantIncome'],
                          data['CoapplicantIncome'], data['LoanAmount'], data['Loan_Amount_Term'], data['Credit_History'], data['Property_Area']
                          ]
        df_predict = pd.DataFrame([predict_request], columns= ['Gender', 'Married', 'Dependents', 'Education', 
                                                            'Self_Employed', 'ApplicantIncome', 'CoapplicantIncome', 'LoanAmount',
                                                            'Loan_Amount_Term', 'Credit_History', 'Property_Area'])
        
        y_pred = pipeline.predict(df_predict)
        output = str(y_pred[0])
        print(output)
        output_text=''
        if output =='Y':
            output_text = 'Congratulations! The loan has been approved.'
        else:
            output_text = 'We are sorry. You application has been rejected.'
        
        headers = {'Content-Type': 'text/html'}
        return make_response(
            render_template('index.html', prediction_text=output_text), 200, headers)


    
# assign endpoint


api.add_resource(predict, '/predict')



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

