# import cv2

# def capture_photo(output_path):
#     # Inicializar la cámara
#     cap = cv2.VideoCapture(-1)

#     # Verificar si la cámara se abrió correctamente
#     if not cap.isOpened():
#         print("No se pudo abrir la cámara.")
#         return

#     # Leer un fotograma de la cámara
#     ret, frame = cap.read()

#     # Verificar si se pudo capturar el fotograma
#     if not ret:
#         print("Error al capturar el fotograma.")
#         cap.release()
#         return

#     # Guardar la imagen en el directorio especificado
#     cv2.imwrite(output_path, frame)

#     # Liberar la cámara
#     cap.release()

#     print("Foto guardada en:", output_path)

# # Ejemplo de uso
# output_path = "/home/jurado/projects/license-plate-detection/license-plate-detection/take-picture/foto.jpg"
# capture_photo(output_path)


from flask import Flask, Response
import cv2
app = Flask(__name__)
video = cv2.VideoCapture(0)
@app.route('/')
def index():
    return "Default Message"
def gen(video):
    while True:
        success, image = video.read()
        ret, jpeg = cv2.imencode('.jpg', image)
        frame = jpeg.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')
@app.route('/video_feed')
def video_feed():
    global video
    return Response(gen(video),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=2204, threaded=True)