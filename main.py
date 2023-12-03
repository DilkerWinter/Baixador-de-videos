import tkinter
import customtkinter
from pytube import YouTube
import os
from datetime import datetime

def baixar_video():
    try:
        ytLink = URL_var.get()
        ytObject = YouTube(ytLink)

        selected_option = quality_var.get()

        if selected_option == "Apenas Audio":
            video = ytObject.streams.filter(only_audio=True).first()
        elif selected_option == "Alta Qualidade":
            video = ytObject.streams.get_highest_resolution()
        elif selected_option == "Menor Qualidade":
            video = ytObject.streams.get_lowest_resolution()
        else:
            finishscreen.configure(text="Erro: Selecione uma opção válida", text_color="red")
            return

        if video is None:
            finishscreen.configure(text="Erro: Qualidade selecionada não disponível", text_color="red")
            return

        titulo.configure(text=ytObject.title, text_color="white")
        finishscreen.configure(text="")

        download_path = os.path.join(os.path.expanduser("~"), "Downloads")

        if not os.path.exists(download_path):
            os.makedirs(download_path)

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        video_path = os.path.join(download_path, f"{video.title}_{timestamp}.mp4")

        video.download(output_path=download_path, filename=f"{video.title}_{timestamp}.mp4")

        finishscreen.configure(text="Vídeo Baixado!")
    except Exception as e:
        print(e)
        finishscreen.configure(text="Erro: não foi possível identificar um link válido ou ocorreu um problema",
                               text_color="red")


def update_progress(bytes_downloaded, total_size):
    porcentagem_completa = bytes_downloaded / total_size * 100
    per = str(int(porcentagem_completa))
    porcentagem.configure(text=per + '%')
    loading_bar.set(float(porcentagem_completa) / 100)
    tela.update_idletasks()

def progresso(stream, chunk, bytes_remaining):
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining

    update_progress(bytes_downloaded, total_size)


customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("dark-blue")

tela = customtkinter.CTk()
tela.geometry("500x350")
tela.title("Baixador de Videos")

titulo = customtkinter.CTkLabel(tela, text="Adicionar Link Do Youtube", font= ("Arial", 20))
titulo.pack(padx=30, pady=20)

URL_var = tkinter.StringVar()
link = customtkinter.CTkEntry(tela, width=400, height=30, textvariable=URL_var)
link.pack(pady=5)

finishscreen = customtkinter.CTkLabel(tela, text="")
finishscreen.pack()

loading_bar = customtkinter.CTkProgressBar(tela, width=400)
loading_bar.set(0)
loading_bar.pack(padx=10, pady=5)

porcentagem = customtkinter.CTkLabel(tela, text="0%")
porcentagem.pack()

quality_var = tkinter.StringVar()
quality_var.set("Apenas Audio")
quality_options = ["Apenas Audio", "Alta Qualidade", "Menor Qualidade"]

quality_menu = customtkinter.CTkOptionMenu(master=tela,
                                           values=quality_options,
                                           variable=quality_var)
quality_menu.pack(pady=10)


botao = customtkinter.CTkButton(tela, text="Baixar Video!", command=baixar_video, width=75, height=35)
botao.pack(pady=10)

tela.mainloop()
