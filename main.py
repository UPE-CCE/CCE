import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import numpy as np
from hamming_codec import encode, decode

def carregar_imagem():
    caminho = filedialog.askopenfilename()  # Abre uma janela para o usuário selecionar um arquivo e armazena o caminho do arquivo na variável 'caminho'
    if caminho:  # Verifica se um caminho foi selecionado (se não estiver vazio)
        imagem = Image.open(caminho).convert('L')  # Abre a imagem do caminho especificado e a converte para escala de cinza ('L')
        imagem.thumbnail((300, 300))  # Reduz o tamanho da imagem para no máximo 300x300 pixels, mantendo a proporção
        img_tk = ImageTk.PhotoImage(imagem)  # Converte a imagem para um formato compatível com o Tkinter para exibição
        lbl_imagem_original.config(image=img_tk)  # Atualiza o widget 'lbl_imagem_original' para mostrar a imagem carregada
        lbl_imagem_original.image = img_tk  # Mantém uma referência da imagem no widget para evitar que o garbage collector a remova
        lbl_imagem_original.imagem_array = np.array(imagem, dtype=np.uint8)  # Converte a imagem para um array NumPy com valores de 8 bits sem sinal
        print('---- Imagem original ----')
        print(lbl_imagem_original.imagem_array)

def codificar_hamming():
    if hasattr(lbl_imagem_original, 'imagem_array'):
        imagem_array = lbl_imagem_original.imagem_array
        altura, largura = imagem_array.shape
        # Cria um array de zeros com 2 bytes (16 bits) por pixel para armazenar 12 bits de codificação
        imagem_codificada = np.zeros((altura, largura, 2), dtype=np.uint8)

        for i in range(altura):
            for j in range(largura):
                pixel = imagem_array[i, j]
                bits = np.unpackbits(np.array([pixel], dtype=np.uint8))
                data_int = int(''.join(map(str, bits)), 2)

                # Codifica os bits para obter uma sequência de 12 bits
                bits_codificados = encode(data_int, len(bits))  # 8 bits originais
                bits_codificados = [int(bit) for bit in bits_codificados]

                # Empacota os 12 bits em 2 bytes (16 bits) e armazena no array
                packed_bits = np.packbits(bits_codificados)
                imagem_codificada[i, j] = packed_bits[:2]  # Armazena os 2 primeiros bytes (12 bits)

        print('---- Imagem_codificada ----')
        print(imagem_codificada)
        lbl_imagem_codificada.imagem_array = imagem_codificada

def decodificar_hamming():
    if hasattr(lbl_imagem_codificada, 'imagem_array'):
        imagem_array = lbl_imagem_codificada.imagem_array
        altura, largura, _ = imagem_array.shape
        imagem_decodificada = np.zeros((altura, largura), dtype=np.uint8)

        for i in range(altura):
            for j in range(largura):
                # Desempacota os 12 bits a partir dos 2 bytes
                packed_bits = imagem_array[i, j]
                bits = np.unpackbits(packed_bits)[:12]  # Seleciona os 12 bits

                # Converte a sequência de bits para um inteiro
                data_int = int(''.join(map(str, bits)), 2)

                # Decodifica os 12 bits para recuperar 8 bits
                bits_decodificados = decode(data_int, 12)
                bits_decodificados = [int(bit) for bit in bits_decodificados]

                # Empacota os 8 bits decodificados de volta em um byte
                imagem_decodificada[i, j] = np.packbits(bits_decodificados[:8])[0]

        print('---- Imagem_decodificada ----')
        print(imagem_decodificada)
        lbl_imagem_decodificada.imagem_array = imagem_decodificada

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
        lbl_imagem_codificada.imagem_array = imagem_ruidosa

# TODO: Renomear 'lbl_imagem_codificada' para um nome que seja mais coerente com o código.
# TODO: Verificar casos de uso no código, e ajustar funcionamento da função mostrar_imagem.
# TODO: Centralizar imagens na aplicação.
def mostrar_imagem():
    if hasattr(lbl_imagem_decodificada, 'imagem_array'):
        imagem_decodificada = lbl_imagem_decodificada.imagem_array
        img_decodificada = Image.fromarray(imagem_decodificada)
        img_tk = ImageTk.PhotoImage(img_decodificada)
        lbl_imagem_decodificada.config(image=img_tk)
        lbl_imagem_decodificada.image = img_tk
    elif hasattr(lbl_imagem_codificada, 'imagem_array'):
        imagem_codificada = lbl_imagem_codificada.imagem_array
        img_codificada = Image.fromarray(imagem_codificada)
        img_tk = ImageTk.PhotoImage(img_codificada)
        lbl_imagem_codificada.config(image=img_tk)
        lbl_imagem_codificada.image = img_tk
    else:
        imagem_original = lbl_imagem_original.imagem_array
        img_original = Image.fromarray(imagem_original)
        img_tk = ImageTk.PhotoImage(img_original)
        lbl_imagem_original.config(image=img_tk)
        lbl_imagem_original.image = img_tk

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

btn_mostrar = tk.Button(frm, text="Mostrar Imagem", command=mostrar_imagem)
btn_mostrar.grid(row=0, column=4, padx=5, pady=5)

lbl_imagem_original = tk.Label(frm)
lbl_imagem_original.grid(row=1, column=0, padx=5, pady=5)

lbl_imagem_codificada = tk.Label(frm)
lbl_imagem_codificada.grid(row=1, column=1, padx=5, pady=5)

lbl_imagem_ruidosa = tk.Label(frm)
lbl_imagem_ruidosa.grid(row=1, column=2, padx=5, pady=5)

lbl_imagem_decodificada = tk.Label(frm)
lbl_imagem_decodificada.grid(row=1, column=3, padx=5, pady=5)

app.mainloop()
