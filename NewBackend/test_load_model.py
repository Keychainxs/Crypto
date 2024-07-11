import pickle 

import pandas as pd    


with open("crypto_model.pkl", "rb") as file: 
    loaded_model =pickle.load(file)  


new_sp500 = pd.DataFrame([[6000]], columns =['price_sp500'])


predicted_crypto_price = loaded_model.predict(new_sp500)
print("Predicted price: ", predicted_crypto_price)