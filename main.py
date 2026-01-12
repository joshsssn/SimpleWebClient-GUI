import tkinter as tk
from tkinter import messagebox, ttk
import requests
from app.core.config_manager import ConfigManager

class UselessFactsApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Useless Facts Client")
        self.root.geometry("500x350")
        
        self.config_manager = ConfigManager()
        self.api_url = self.config_manager.config["APP"]["API_URL"]
        
        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        ttk.Label(main_frame, text="Useless Facts", font=("Helvetica", 16, "bold")).pack(pady=5)
        ttk.Label(main_frame, text="Made by some random student during the break 💀", font=("Helvetica", 12)).pack(pady=5)

        # Language Selection
        lang_frame = ttk.Frame(main_frame)
        lang_frame.pack(pady=5)
        ttk.Label(lang_frame, text="Language:").pack(side=tk.LEFT, padx=5)
        self.lang_var = tk.StringVar(value="en")
        ttk.Radiobutton(lang_frame, text="English", variable=self.lang_var, value="en").pack(side=tk.LEFT)
        ttk.Radiobutton(lang_frame, text="German (No one will ever use that 💀)", variable=self.lang_var, value="de").pack(side=tk.LEFT)

        # Buttons
        btn_frame = ttk.Frame(main_frame)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Get Random Fact", command=self.get_random_fact).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="Get Today's Fact", command=self.get_today_fact).pack(side=tk.LEFT, padx=5)

        # Text Area
        self.text_area = tk.Text(main_frame, wrap=tk.WORD, height=8, font=("Helvetica", 11))
        self.text_area.pack(fill=tk.BOTH, expand=True, pady=10)
        
    def fetch_fact(self, endpoint):
        lang = self.lang_var.get()
        url = f"{self.api_url}api/v2/facts/{endpoint}?language={lang}"
        headers = {"Accept": "application/json"}
        
        try:
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, "Loading...")
            self.root.update_idletasks()
            
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            self.text_area.delete(1.0, tk.END)
            self.text_area.insert(tk.END, data.get("text", "No fact found."))
        except requests.exceptions.RequestException as e:
            self.text_area.delete(1.0, tk.END)
            messagebox.showerror("Error", f"Failed to fetch data: {e}")

    def get_random_fact(self):
        self.fetch_fact("random")

    def get_today_fact(self):
        self.fetch_fact("today")

if __name__ == "__main__":
    root = tk.Tk()
    app = UselessFactsApp(root)
    root.mainloop()
