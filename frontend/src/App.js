import React, { useState } from 'react';
import './App.css';
function App() {
  const [result, setResult] = useState('');

  const llamarAPI = async () => {
    try {
      const response = await fetch('http://127.0.0.1:5000/detection', {
        method: 'GET',
        // headers: {
        //   'Content-Type': 'application/json'
        // },
        // body: JSON.stringify({ data: 'Datos para enviar' })
      });
 
      const data = await response.json();
      setResult(data.message);
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div>
      <button onClick={llamarAPI}>Llamar a la API</button>
      <label>{result}</label>
    </div>
  );
}

export default App;
