from flask import Flask,request, url_for, redirect, render_template, jsonify
import pandas as pd
import pickle
import numpy as np

app = Flask(__name__)

model = pickle.load(open('model.pkl', 'rb'))

day_dict = {'Fri':[1,0,0,0,0,0,0], 'Mon':[0,1,0,0,0,0,0],
            'Sat': [0,0,1,0,0,0,0], 'Sun':[0,0,0,1,0,0,0],
            'Thu':[0,0,0,0,1,0,0], 'Tue':[0,0,0,0,0,1,0],
            'Wed': [0,0,0,0,0,0,1]}

month_dict = {'January':[1,0,0,0,0,0,0,0,0,0,0,0], 'February':[0,1,0,0,0,0,0,0,0,0,0,0],
            'March': [0,0,1,0,0,0,0,0,0,0,0,0], 'April':[0,0,0,1,0,0,0,0,0,0,0,0],
            'May':[0,0,0,0,1,0,0,0,0,0,0,0], 'June':[0,0,0,0,0,1,0,0,0,0,0,0],
            'July': [0,0,0,0,0,0,1,0,0,0,0,0], 'August': [0,0,0,0,0,0,0,1,0,0,0,0],
            'September': [0,0,0,0,0,0,0,0,1,0,0,0], 'October': [0,0,0,0,0,0,0,0,0,1,0,0],
            'November': [0,0,0,0,0,0,0,0,0,0,1,0], 'December': [0,0,0,0,0,0,0,0,0,0,0,1]}

# cols = ['hour', 'is_holiday', 'day_of_week']

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict',methods=['POST','GET'])
def predict():
    item = [x for x in request.form.values()]
    print(item)
    ## postman begin
    #hour = request.args.get('hour')
    #is_holiday = request.args.get('is_holiday')
    #day_of_week = request.args.get('day_of_week')

    #data = []

    #data.append(hour)
    #if is_holiday == 'Yes':
    #    data.extend([0,1])
    #else:
    #    data.extend([1,0])
    #
    #data.extend(day_dict[day_of_week])

    ### postman end



    data = []

    # As the The training data was dummified one, so we have to pass the 
    # test data in the same format ('hour','is_holiday','day_of_week')
    
    data.append(int(item[0]))
    
    # is holiday
    if item[1] == 'Yes':
        data.extend([0,1])
    else:
        data.extend([1,0])
        
    # fri, mon, sat , sun, thu, tue, wed
    data.extend(day_dict[item[3]])

    data.append(item[2])

    data.extend(month_dict[item[4]])

    prediction = int(model.predict([data])[0])
    
    # postman begin

    # return 'the predicted total bike count :' + str(prediction) 

    # postman end
   


    return render_template('index.html',pred='Total Bike ride counts on {} at {}:00 Hrs at {}° Celsius in {} will be {}'.format(item[2], item[0], item[3], item[4], prediction))



#if __name__ == '__main__':
#    app.run(host="0.0.0.0", port=config.PORT, debug=config.DEBUG_MODE)


if __name__ == "__main__":
    app.run(debug=True)