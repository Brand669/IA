Modelar una red red neuronal que pueda identificar emociones a través de valores obtenidos de los landmarks que genera mediapipe

Definir el tie de red nauronal y describir cada una de sus partes. 
Definir sus patrones a utilizar
Definir función de activacion es necesaria para este problema.
Definir el numero máximo de entradas
Que valores a salida de la red se podrian esperar?
Cuales son los valores máximos  que puede tener el bias 7



Diseño de una red neuronal para identificar emociones a partir de landmarks faciales de MediaPipe
1. Tipo de red neuronal y descripción de sus partes
Para identificar emociones a partir de los puntos faciales obtenidos con MediaPipe, he decidido utilizar una red neuronal profunda (DNN - Deep Neural Network). La razón detrás de esta elección es que los datos de entrada son valores numéricos y no imágenes, por lo que una red convolucional (CNN) no es la mejor opción en este caso.

La estructura de la red que propongo es la siguiente:

Capa de entrada: Recibe los valores de los landmarks. Cada punto tiene coordenadas (x, y, z), por lo que el tamaño de la entrada dependerá del número de puntos seleccionados.

Capas ocultas: Son varias capas densas (fully connected) con funciones de activación ReLU para extraer patrones.

Capa de salida: Es una capa con 7 neuronas, una por cada emoción, que utiliza la función de activación Softmax para generar probabilidades.

2. Patrones a utilizar
El modelo utilizará como entrada los valores de los landmarks faciales obtenidos con MediaPipe.

MediaPipe detecta 468 landmarks en la cara, cada uno con (x, y, z).

Si tomamos todos, la entrada tendrá 1404 valores (468 × 3).

Si reducimos a los 68 landmarks más importantes (como los usados en dlib), la entrada será de 204 valores (68 × 3).

Las emociones que quiero detectar son:

Alegría

Tristeza

Ira

Sorpresa

Miedo

Desagrado

Neutral

3. Función de activación
Para el funcionamiento correcto de la red, elegí las siguientes funciones de activación:

ReLU (Rectified Linear Unit) en las capas ocultas, porque es eficiente y evita problemas de gradiente:


Softmax en la capa de salida, ya que permite convertir los valores en probabilidades normalizadas:

4. Número máximo de entradas
El máximo de entradas dependerá de los puntos faciales que se utilicen:

Si uso 468 landmarks completos: 1404 valores de entrada.

Si uso solo 68 landmarks importantes: 204 valores de entrada.

5. Valores esperados en la salida
La salida de la red será un vector de 7 valores, cada uno representando la probabilidad de una emoción.

Ejemplo de salida esperada:

[0.05,0.10,0.15,0.50,0.05,0.10,0.05]
[0.05,0.10,0.15,0.50,0.05,0.10,0.05]
Aquí, la emoción con la mayor probabilidad es la cuarta (por ejemplo, "Sorpresa").

6. Valores máximos del bias
El bias es un valor ajustable en cada neurona y no tiene un límite teórico, pero si en este caso me piden definirlo con un valor máximo de 7, significa que ese será el mayor valor que podrá tomar durante el entrenamiento.

