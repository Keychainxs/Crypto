from flask import Flask, request,jsonify
import pickle 
import pandas as pd 


app = Flask(__name__) 
with open('crypto_model.pkl','rb') as file: 
    model = pickle.load(file)


@app.route("/predict",methods = ['POST'])

def makePredicts(): 

    try:
        data = request.get_json(force = True)
     
    
        if 'price_sp500' not in data:
            return jsonify({'error: Invlaid input, price of sp_500 is needed'}), 400 
        
 
        price_sp500 = float(data['price_sp500'])
        new_sp500_price = pd.DataFrame([[price_sp500]],columns=['price_sp500'])  # Example new S&P 500 price
        predicted_crypto_price = model.predict(new_sp500_price)[0]
        return jsonify({"Predicted cryptocurrency price": predicted_crypto_price})
    except Exception as e:
        return jsonify({'error': str(e)}), 500 


    

if __name__ == '__main__': 
    app.run(debug=True)
