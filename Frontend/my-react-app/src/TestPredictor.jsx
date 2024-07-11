
import { useState } from 'react';
import axios from 'axios';



function Testpredictor() {
    const [SP500_DATA, setSP500_DATA] = useState('');
    const [CRYPTO_DATA, setCRYPTO_DATA] = useState(null);
    const [error, setError] = useState(null);

    const handleInputChange = (e) => {
        setSP500_DATA(e.target.value);
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError(null);
        setCRYPTO_DATA(null);

        try {
            const response = await axios.post('http://127.0.0.1:5000/predict', {
                'price_sp500': SP500_DATA
            });
            console.log("Response received from the Backend: ", response.data);
            setCRYPTO_DATA(response.data['Predicted cryptocurrency price']); 
        } catch (err) {
            console.log("Error during API call:", err);
            setError(err.response ? err.response.data.error : err.message);
        }
    };

    return (
        <div className = 'container'>
            <h1 className='header'>Crypto Predictor</h1>
            <form onSubmit={handleSubmit} className='form'>
                <input
                    value={SP500_DATA}
                    placeholder='Enter S&P 500 Price'
                    type='text'
                    onChange={handleInputChange}
                    className='input'
                />
                <button type='submit' className='button'>Predict</button>
            </form>
            {CRYPTO_DATA && (
                <div className='result'>
                    <h2 className='result-title'>Predicted Cryptocurrency Price:</h2>
                    <p>{CRYPTO_DATA}</p>
                </div>
            )}
            {error && (
                <div className='error'>
                    <h2 className='error-title'>Error</h2>
                    <p>{error}</p>
                </div>
            )}
            <div className = 'disclaimer'>

                <p>This Is Not Financial Advice.</p>
            </div>
            <div className='copyright'>
            <p>&copy; 2024 Kishan Patel All Rights reserved.</p>
            </div>
        </div>
    );
}

export default Testpredictor;