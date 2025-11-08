import tkinter as tk
import platform
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter import simpledialog, messagebox
from docx import Document
import keyring

APP_NAME = "Translator"
API_KEY_NAME = "deepl_api_Key"

def get_api_key():
    key = keyring.get_password(APP_NAME, API_KEY_NAME)
    if not key:
        key = simpledialog.askstring("API Key Required", 
                                     "Please enter your API key:",
                                     show='*')  
        if key:
            keyring.set_password(APP_NAME, API_KEY_NAME, key)
            messagebox.showinfo("Saved", "API key saved securely.")
        else:
            messagebox.showwarning("Missing Key", "No API key entered.")
            return None
    return key

def reset_api_key():
    keyring.delete_password(APP_NAME, API_KEY_NAME)
    messagebox.showinfo("Reset", "API key removed. You will be asked again next time.")


def save_file(root):
    text_window = root.focus_get()
    if not isinstance(text_window, tk.Text):
        return

    filepath = getattr(root, "current_file", None)

    if not filepath or filepath == "Translate":
        filepath = asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt")]
        )
        if not filepath:
            return
        root.current_file = filepath

    try:
        with open(filepath, "w", encoding="utf-8") as f:
            content = text_window.get(1.0, tk.END)
            f.write(content.strip())

        root.title("Saved")
        root.after(1000, lambda: root.title(filepath))

    except Exception as e:
        text_window.delete(1.0, tk.END)
        text_window.insert(tk.END, f"Error saving file:\n{e}")

def open_file(root):
    ext_window = root.focus_get()
    if not isinstance(text_window, tk.Text):
        return
    filepath = askopenfilename(
        filetypes=[
            ("Text and Word files", "*.txt *.docx"),
            ("Text files", "*.txt"),
            ("Word documents", "*.docx")
        ]
    )

    if not filepath:
        return

    text_window.delete(1.0, tk.END)

    try:
        if filepath.lower().endswith(".txt"):
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read()

        elif filepath.lower().endswith(".docx"):
            doc = Document(filepath)
            content = "\n".join(p.text for p in doc.paragraphs)

        else:
            content = "Unsupported file type."

        text_window.insert(tk.END, content)

        root.title(f"{filepath}")
        root.focus_force()
        text_window.focus_set()

    except Exception as e:
        text_window.insert(tk.END, f"Error opening file:\n{e}")
        root.title("Error")


def translate_text(root):
    text_window = root.focus_get()
    if not isinstance(text_window, tk.Text):
        return
    key = get_api_key()
    print(key)
    if text_window.winfo_name() == "!text":
        print("text1")
    else:
        print("text2")
    return

root = tk.Tk()
root.attributes("-fullscreen", True)
root.title("Translate")

toolbar = tk.Frame(root, bd=1, relief=tk.RAISED)
toolbar.pack(side=tk.TOP, fill=tk.X)

frame = tk.Frame(root)
frame.pack(fill="both", expand=True)

btn_open = tk.Button(toolbar, text="Open", command=lambda: open_file(root))
btn_open.pack(side=tk.LEFT, padx=2, pady=2)

btn_save = tk.Button(toolbar, text="Save", command=lambda: save_file(root))
btn_save.pack(side=tk.LEFT, padx=2, pady=2)

btn_translate = tk.Button(toolbar, text="Translate", command=lambda: translate_text(root))
btn_translate.pack(side=tk.LEFT, padx=2, pady=2)

btn_reset = tk.Button(toolbar, text="Delete API Key", command=reset_api_key)
btn_reset.pack(side=tk.LEFT, padx=2, pady=2)

text1 = tk.Text(frame, bd=0, undo=True, maxundo=-1, wrap='word')
text2 = tk.Text(frame, bd=0, undo=True, maxundo=-1, wrap='word')
text1.pack(side="left", fill="both", expand=True)
text2.pack(side="left", fill="both", expand=True)

for i in range(10000):
    text1.insert("end", f"SATISFY MY RAT DESIRE {i}\n")
    text2.insert("end", f"LOBSTER GENOCIDE {i}\n")

modifier_held = False

def on_modifier_press(event):
    global modifier_held
    modifier_held = True

def on_modifier_release(event):
    global modifier_held
    modifier_held = False

def redo(root, event):
    text = root.focus_get()
    text.edit_redo()

def switch(root, event):
    current = root.focus_get()
    if current == text1:
        text2.focus_set()
    else:
        text1.focus_set()
    


root.bind("<Control_L>", on_modifier_press)
root.bind("<KeyRelease-Control_L>", on_modifier_release)
root.bind("<Control_R>", on_modifier_press)
root.bind("<KeyRelease-Control_R>", on_modifier_release)

root.bind("<Meta_L>", on_modifier_press)
root.bind("<KeyRelease-Meta_L>", on_modifier_release)
root.bind("<Meta_R>", on_modifier_press)
root.bind("<KeyRelease-Meta_R>", on_modifier_release)

root.bind("<Control-Shift-Z>", lambda e: redo(root, e))
root.bind("<Command-Shift-Z>", lambda e: redo(root, e))

root.bind("<Control-Shift-I>", lambda e: switch(root, e))
root.bind("<Command-Shift-I>", lambda e: switch(root, e))

def on_mousewheel(event, source, target):
    system = platform.system()

    if system == "Darwin":  
        delta = -1 * int(event.delta)
    else:
        delta = -1 * (event.delta // 120 if event.delta else (1 if event.num == 5 else -1))

    if modifier_held:
        source.yview_scroll(delta, "units")
        target.yview_scroll(delta, "units")
    else:
        source.yview_scroll(delta, "units")

    return "break"

for t1, t2 in [(text1, text2), (text2, text1)]:
    t1.bind("<MouseWheel>", lambda e, s=t1, o=t2: on_mousewheel(e, s, o))
    t1.bind("<Button-4>", lambda e, s=t1, o=t2: on_mousewheel(e, s, o))
    t1.bind("<Button-5>", lambda e, s=t1, o=t2: on_mousewheel(e, s, o))

root.mainloop()
