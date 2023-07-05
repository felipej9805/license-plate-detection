import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import { Oval, ThreeDots } from 'react-loader-spinner';
import { Modal, Button } from 'react-bootstrap';

function App() {
  const [result, setResult] = useState('');
  const [loading, setLoading] = useState(false);
  const [showModal, setShowModal] = useState(false);

  const llamarAPI = async () => {
    try {
      setLoading(true); // Activar el indicador de carga

      const response = await fetch(`http://${process.env.REACT_APP_DETECTION}/detection`, {
        method: 'GET',
      });

      const data = await response.json();
      setResult(data.message);
    } catch (error) {
      console.log(error);
    } finally {
      setLoading(false); // Desactivar el indicador de carga
      setShowModal(true); // Mostrar el modal con el resultado
    }
  };

  const handleCloseModal = () => {
    setShowModal(false);
  };

  return (
    <div className="container-fluid bg-light vh-100">
      <div className="row justify-content-center align-items-center h-100">
        <div className="col text-center">
          <img
            src="https://images8.alphacoders.com/282/282535.jpg"
            alt="Mountain"
            className="img-fluid rounded-circle mb-4"
            style={{ maxWidth: '500px' }}
          />
          <h1 className="mt-5">Identificar Placa</h1>
          <button
            className="btn btn-primary mt-3"
            onClick={llamarAPI}
            disabled={loading}
          >
            {loading ? (
              <Oval type="Oval" color="#FFF" height={20} width={20} />
            ) : (
              'Identificar'
            )}
          </button>
        </div>
      </div>

      <Modal show={showModal} onHide={handleCloseModal}>
        <Modal.Header closeButton>
          <Modal.Title>Resultado</Modal.Title>
        </Modal.Header>
        <Modal.Body>
          {loading ? (
            <div className="d-flex justify-content-center">
              <ThreeDots
                type="ThreeDots"
                color="#000"
                height={50}
                width={50}
              />
            </div>
          ) : (
            <div className="result display-4">{result}</div>
          )}
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={handleCloseModal}>
            Cerrar
          </Button>
        </Modal.Footer>
      </Modal>
    </div>
  );
}

export default App;
