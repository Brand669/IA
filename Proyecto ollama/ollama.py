import os
import requests
import json

# Ruta a tu carpeta con los archivos
carpeta = r"C:\Users\Brandon\Desktop\ITM\IA\Proyecto ollama\corpus"
modelo = "llama2"  # Cambia si usas otro

def obtener_embedding(texto):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": modelo,
            "prompt": f"Embed this text:\n\n{texto}",
            "stream": False
        }
    )
    return response.json()

# Procesar todos los archivos .txt en la carpeta
for archivo in os.listdir(carpeta):
    if archivo.endswith(".txt"):
        ruta_archivo = os.path.join(carpeta, archivo)
        with open(ruta_archivo, "r", encoding="utf-8") as f:
            texto = f.read()
            resultado = obtener_embedding(texto)
            
            nombre_salida = archivo.replace(".txt", "_embedding.json")
            ruta_salida = os.path.join(carpeta, "..", nombre_salida)

            with open(ruta_salida, "w", encoding="utf-8") as out:
                json.dump(resultado, out, indent=2)

print("Embeddings generados.")
