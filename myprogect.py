import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pyttsx3
import speech_recognition as sr
from googletrans import Translator
from PIL import Image, ImageTk
import pytesseract
import os

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

BACKGROUND_COLOR = "#2C3E50"
TEXT_COLOR = "#ECF0F1"
TEXT_ENTRY_BG = "#34495E"
TEXT_ENTRY_FG = "#ECF0F1"
BUTTON_COLOR = "#FF6347"
BUTTON_HOVER_COLOR = "#FF4500"


def text_to_speech(text):
    if text:
        speaker = pyttsx3.init()
        speaker.say(text)
        speaker.runAndWait()
    else:
        messagebox.showwarning("Предупреждение", "Текст пуст!")

def translate_text():
    text = input_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showerror("Ошибка", "Пожалуйста, введите текст для перевода.")
        return
    try:
        translator = Translator()
        translated = translator.translate(text, src='en', dest='ru')
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, translated.text)
        save_button.pack(pady=10)
        text_to_speech(translated.text)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка при переводе: {e}")

def speech_to_text():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        status_label.config(text="Говорите...")
        try:
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language="ru-RU")
            text_entry.insert(tk.END, text + " ")
            status_label.config(text="Текст распознан!")
        except sr.UnknownValueError:
            status_label.config(text="Не удалось распознать текст")
        except sr.RequestError:
            status_label.config(text="Ошибка подключения")

def image_to_text():
    image_path = image_entry.get().strip()
    if not os.path.exists(image_path):
        messagebox.showerror("Ошибка", f"Изображение {image_path} не найдено.")
        return
    try:
        image = Image.open(image_path)
        text = pytesseract.image_to_string(image)
        output_text.delete(1.0, tk.END)
        output_text.insert(tk.END, text)
        text_to_speech(text)
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при распознавании текста с изображения: {e}")

def choose_image_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", ".jpg;.png;.jpeg;.bmp")])
    if file_path:
        image_entry.delete(0, tk.END)
        image_entry.insert(0, file_path)
        show_image_on_tab(file_path)

def show_image_on_tab(image_path):
    try:
        img = Image.open(image_path)
        img.thumbnail((150, 150))
        img = ImageTk.PhotoImage(img)
        display_image_label.config(image=img)
        display_image_label.image = img
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {e}")

def save_text_to_file():
    text = output_text.get("1.0", tk.END).strip()
    if not text:
        messagebox.showwarning("Предупреждение", "Нет текста для сохранения.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
    if file_path:
        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(text)
            messagebox.showinfo("Успех", f"Текст успешно сохранен в {file_path}")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось сохранить файл: {e}")


def create_main_window():
    global root, input_text, output_text, status_label, image_entry, text_entry, display_image_label, save_button
    root = tk.Tk()
    root.title("Text and Speech Tool")
    root.geometry("800x700")
    root.configure(bg=BACKGROUND_COLOR)

    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    
    translate_frame = ttk.Frame(notebook)
    notebook.add(translate_frame, text="Переводчик")
    title_label = ttk.Label(translate_frame, text="Переводчик с английского на русский", font=("Helvetica", 16, "bold"))
    title_label.pack(pady=10)

    input_label = ttk.Label(translate_frame, text="Введите текст на английском", font=("Helvetica", 12))
    input_label.pack(pady=5)

    input_text = tk.Text(translate_frame, height=6, width=50, font=("Helvetica", 12), bg=TEXT_ENTRY_BG, fg=TEXT_ENTRY_FG)
    input_text.pack(pady=10)

    output_label = ttk.Label(translate_frame, text="Переведенный текст", font=("Helvetica", 12))
    output_label.pack(pady=5)

    output_text = tk.Text(translate_frame, height=6, width=50, font=("Helvetica", 12), bg=TEXT_ENTRY_BG, fg=TEXT_ENTRY_FG)
    output_text.pack(pady=10)

    translate_button = ttk.Button(translate_frame, text="Перевести", command=translate_text)
    translate_button.pack(pady=10)

    save_button = ttk.Button(translate_frame, text="Сохранить текст", command=save_text_to_file)
    save_button.pack_forget()

    
    speech_frame = ttk.Frame(notebook)
    notebook.add(speech_frame, text="Речь в текст")
    status_label = ttk.Label(speech_frame, text="Нажмите, чтобы начать", font=("Helvetica", 14))
    status_label.pack(pady=10)

    speech_button = ttk.Button(speech_frame, text="Речь в текст", command=speech_to_text)
    speech_button.pack(pady=10)

    text_entry = tk.Text(speech_frame, height=6, width=50, font=("Helvetica", 12), bg=TEXT_ENTRY_BG, fg=TEXT_ENTRY_FG)
    text_entry.pack(pady=10)

   
    image_frame = ttk.Frame(notebook)
    notebook.add(image_frame, text="Изображение в текст")

    image_label = ttk.Label(image_frame, text="Выберите изображение для распознавания текста", font=("Helvetica", 14))
    image_label.pack(pady=10)

    image_entry = ttk.Entry(image_frame, font=("Helvetica", 12))
    image_entry.pack(pady=5)

    choose_image_button = ttk.Button(image_frame, text="Выбрать изображение", command=choose_image_file)
    choose_image_button.pack(pady=5)

    display_image_label = ttk.Label(image_frame)
    display_image_label.pack(pady=10)

    recognize_image_button = ttk.Button(image_frame, text="Распознать текст", command=image_to_text)
    recognize_image_button.pack(pady=10)

    root.mainloop()

if __name__ == "__main__":
    create_main_window()


