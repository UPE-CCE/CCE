import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
from hamming_codec import encode, decode

def carregar_imagem():
    caminho = filedialog.askopenfilename()
    if caminho:
        imagem = Image.open(caminho).convert('L')
        imagem.thumbnail((300, 300))
        img_tk = ImageTk.PhotoImage(imagem)
        lbl_imagem_original.config(image=img_tk)
        lbl_imagem_original.image = img_tk
        lbl_imagem_original.imagem_array = np.array(imagem, dtype=np.uint8)

def codificar_hamming():
    if hasattr(lbl_imagem_original, 'imagem_array'):
        imagem_array = lbl_imagem_original.imagem_array
        altura, largura = imagem_array.shape
        imagem_codificada = np.zeros_like(imagem_array, dtype=np.uint8)

        for i in range(altura):
            for j in range(largura):
                pixel = imagem_array[i, j]
                bits = np.unpackbits(np.array([pixel], dtype=np.uint8))
                data_int = int(''.join(map(str, bits)), 2)
                n_bits = len(bits)
                bits_codificados = encode(data_int, n_bits)
                bits_codificados = [int(bit) for bit in bits_codificados]
                imagem_codificada[i, j] = np.packbits(bits_codificados[:8])[0]

        lbl_imagem_codificada.imagem_array = imagem_codificada

def adicionar_ruido():
    if hasattr(lbl_imagem_codificada, 'imagem_array'):
        imagem_array = lbl_imagem_codificada.imagem_array.copy()
        proporcao_ruido = 0.01  # 1% de ruído
        num_pixels = int(proporcao_ruido * imagem_array.size)
        coords = [np.random.randint(0, i - 1, num_pixels) for i in imagem_array.shape]
        imagem_array[coords[0], coords[1]] = 255  # Sal
        coords = [np.random.randint(0, i - 1, num_pixels) for i in imagem_array.shape]
        imagem_array[coords[0], coords[1]] = 0    # Pimenta
        imagem_ruidosa = np.clip(imagem_array, 0, 255).astype(np.uint8)
        lbl_imagem_ruidosa.imagem_array = imagem_ruidosa

def decodificar_hamming():
    if hasattr(lbl_imagem_ruidosa, 'imagem_array'):
        imagem_array = lbl_imagem_ruidosa.imagem_array
        altura, largura = imagem_array.shape
        imagem_decodificada = np.zeros_like(imagem_array, dtype=np.uint8)

        for i in range(altura):
            for j in range(largura):
                pixel = imagem_array[i, j]
                bits = np.unpackbits(np.array([pixel], dtype=np.uint8))
                data_int = int(''.join(map(str, bits)), 2)
                n_bits = len(bits)
                bits_decodificados = decode(data_int, n_bits)
                bits_decodificados = [int(bit) for bit in bits_decodificados]
                imagem_decodificada[i, j] = np.packbits(bits_decodificados[:8])[0]

        img_decodificada = Image.fromarray(imagem_decodificada)
        img_tk = ImageTk.PhotoImage(img_decodificada)
        lbl_imagem_decodificada.config(image=img_tk)
        lbl_imagem_decodificada.image = img_tk

app = tk.Tk()
app.title("Correção de Erros com Código de Hamming")

frm = tk.Frame(app)
frm.pack(padx=10, pady=10)

btn_carregar = tk.Button(frm, text="Carregar Imagem", command=carregar_imagem)
btn_carregar.grid(row=0, column=0, padx=5, pady=5)

btn_codificar = tk.Button(frm, text="Codificar Hamming", command=codificar_hamming)
btn_codificar.grid(row=0, column=1, padx=5, pady=5)

btn_ruido = tk.Button(frm, text="Adicionar Ruído", command=adicionar_ruido)
btn_ruido.grid(row=0, column=2, padx=5, pady=5)

btn_decodificar = tk.Button(frm, text="Decodificar Hamming", command=decodificar_hamming)
btn_decodificar.grid(row=0, column=3, padx=5, pady=5)

lbl_imagem_original = tk.Label(frm)
lbl_imagem_original.grid(row=1, column=0, padx=5, pady=5)

lbl_imagem_codificada = tk.Label(frm)
lbl_imagem_codificada.grid(row=1, column=1, padx=5, pady=5)

lbl_imagem_ruidosa = tk.Label(frm)
lbl_imagem_ruidosa.grid(row=1, column=2, padx=5, pady=5)

lbl_imagem_decodificada = tk.Label(frm)
lbl_imagem_decodificada.grid(row=1, column=3, padx=5, pady=5)

app.mainloop()
