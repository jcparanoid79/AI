import tkinter as tk
from tkinter import scrolledtext, filedialog, messagebox
from openai import OpenAI
import os
from dotenv import load_dotenv
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import RawTokenFormatter  # Use a valid formatter

load_dotenv()
api_key = os.getenv("DEEPSEEK_API_KEY")
client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")

class CodeGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DeepSeek Coding Agent")
        self.setup_ui()
        
    def setup_ui(self):
        # Input Section
        tk.Label(self.root, text="Describe your code:").pack(pady=5)
        self.input_text = scrolledtext.ScrolledText(self.root, height=8, width=80, wrap=tk.WORD)
        self.input_text.pack(pady=5)
        
        # Buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=5)
        
        tk.Button(button_frame, text="Generate Code", command=self.generate_code).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Copy Code", command=self.copy_code).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Save Code", command=self.save_code).pack(side=tk.LEFT, padx=5)
        
        # Output Section
        tk.Label(self.root, text="Generated Code:").pack(pady=5)
        self.output_text = scrolledtext.ScrolledText(self.root, height=20, width=80, wrap=tk.WORD)
        self.output_text.pack(pady=5)
        
        # Configure tags for syntax highlighting
        self.configure_syntax_tags()
    
    def configure_syntax_tags(self):
        # Example tags for syntax highlighting
        self.output_text.tag_configure("keyword", foreground="blue")
        self.output_text.tag_configure("string", foreground="green")
        self.output_text.tag_configure("comment", foreground="gray")
    
    def generate_code(self):
        prompt = self.input_text.get("1.0", tk.END).strip()
        try:
            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": "Generate Python code."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3
            )
            code = response.choices[0].message.content
            self.output_text.delete("1.0", tk.END)
            self.apply_syntax_highlighting(code)
        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error: {e}")
    
    def apply_syntax_highlighting(self, code):
        # Use Pygments to tokenize the code and apply syntax highlighting
        from pygments.token import Token
        from pygments.lexers import PythonLexer
        from pygments.formatter import Formatter

        class TkinterFormatter(Formatter):
            def __init__(self, text_widget):
                super().__init__()
                self.text_widget = text_widget

            def format(self, tokensource, outfile):
                for ttype, value in tokensource:
                    tag = None
                    if ttype in Token.Keyword:
                        tag = "keyword"
                    elif ttype in Token.String:
                        tag = "string"
                    elif ttype in Token.Comment:
                        tag = "comment"
                    self.text_widget.insert(tk.END, value, tag if tag else "")

        formatter = TkinterFormatter(self.output_text)
        highlight(code, PythonLexer(), formatter)
    
    def copy_code(self):
        code = self.output_text.get("1.0", tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(code)
        messagebox.showinfo("Copied", "Code copied to clipboard!")
    
    def save_code(self):
        code = self.output_text.get("1.0", tk.END)
        filepath = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python Files", "*.py"), ("All Files", "*.*")]
        )
        if filepath:
            with open(filepath, "w") as f:
                f.write(code)
            messagebox.showinfo("Saved", f"Code saved to {filepath}")

if __name__ == "__main__":
    root = tk.Tk()
    app = CodeGeneratorApp(root)
    root.mainloop()