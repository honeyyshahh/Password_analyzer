import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from zxcvbn import zxcvbn
import itertools

# Leetspeak mapping
leet_map = {
    'a': ['a', '@', '4'],
    'e': ['e', '3'],
    'i': ['i', '1', '!'],
    'o': ['o', '0'],
    's': ['s', '$', '5'],
    't': ['t', '7']
}

def leetspeak_variations(word):
    options = [leet_map.get(c.lower(), [c]) for c in word]
    variations = set(''.join(c) for c in itertools.product(*options))
    return variations

def generate_wordlist(name, pet, date):
    base_words = [name, pet]
    suffixes = ['', date, '123', '@123', '!']
    wordlist = set()

    for word in base_words:
        if not word:
            continue
        leet_variants = leetspeak_variations(word)
        for variant in leet_variants:
            for suffix in suffixes:
                wordlist.add(variant + suffix)

    return sorted(wordlist)

def analyze_password(password):
    result = zxcvbn(password)
    score = result['score']
    feedback = result['feedback']
    strength_levels = ["Very Weak", "Weak", "Fair", "Good", "Strong"]

    result_text = f"🔐 Password Strength: {strength_levels[score]} ({score}/4)\n\n"
    if feedback['warning']:
        result_text += f"⚠️ Warning: {feedback['warning']}\n"
    if feedback['suggestions']:
        result_text += "💡 Suggestions:\n"
        for suggestion in feedback['suggestions']:
            result_text += f" - {suggestion}\n"
    return result_text

def main():
    def handle_analyze():
        password = password_entry.get()
        if not password:
            messagebox.showwarning("Input Error", "Please enter a password.")
            return
        result_text = analyze_password(password)
        result_box.config(state='normal')
        result_box.delete(1.0, tk.END)
        result_box.insert(tk.END, result_text)
        result_box.config(state='disabled')

    def handle_generate_wordlist():
        name = name_entry.get()
        pet = pet_entry.get()
        date = date_entry.get()
        words = generate_wordlist(name, pet, date)
        wordlist_box.delete(1.0, tk.END)
        for word in words:
            wordlist_box.insert(tk.END, word + "\n")

    def handle_export_wordlist():
        words = wordlist_box.get(1.0, tk.END).strip().split('\n')
        if not words or words == ['']:
            messagebox.showwarning("No Wordlist", "Generate a wordlist before exporting.")
            return
        filepath = filedialog.asksaveasfilename(defaultextension=".txt",
                                                filetypes=[("Text Files", "*.txt")])
        if filepath:
            with open(filepath, 'w') as f:
                for word in words:
                    f.write(word + "\n")
            messagebox.showinfo("Export Successful", f"Wordlist saved to:\n{filepath}")

    root = tk.Tk()
    root.title("🛡️ Password Strength & Wordlist Tool")
    root.geometry("800x600")
    root.configure(bg="#e6f2ff")

    # Top Frame - Contains Password Analysis and Wordlist Generator
    top_frame = tk.Frame(root, bg="#e6f2ff")
    top_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

    # Password Analysis Frame
    pw_frame = tk.LabelFrame(top_frame, text="🔐 Password Strength Checker", bg="#ffffff", font=("Segoe UI", 10, "bold"), padx=10, pady=10)
    pw_frame.grid(row=0, column=0, padx=10, pady=5, sticky="nsew")

    tk.Label(pw_frame, text="Enter Password:", bg="#ffffff", font=("Segoe UI", 10)).pack(anchor='w')
    password_entry = tk.Entry(pw_frame, show="*", width=35, font=("Segoe UI", 11))
    password_entry.pack(pady=5)

    tk.Button(pw_frame, text="Analyze", bg="#0052cc", fg="white", font=("Segoe UI", 10, "bold"),
              command=handle_analyze).pack(pady=5)

    result_box = scrolledtext.ScrolledText(pw_frame, height=8, width=45, wrap=tk.WORD, state='disabled', font=("Segoe UI", 10))
    result_box.pack(pady=5)

    # Wordlist Generator Frame
    wordlist_frame = tk.LabelFrame(top_frame, text="📝 Wordlist Generator", bg="#ffffff", font=("Segoe UI", 10, "bold"), padx=10, pady=10)
    wordlist_frame.grid(row=0, column=1, padx=10, pady=5, sticky="nsew")

    tk.Label(wordlist_frame, text="Name:", bg="#ffffff").pack(anchor='w')
    name_entry = tk.Entry(wordlist_frame, width=30)
    name_entry.pack(pady=2)

    tk.Label(wordlist_frame, text="Pet Name:", bg="#ffffff").pack(anchor='w')
    pet_entry = tk.Entry(wordlist_frame, width=30)
    pet_entry.pack(pady=2)

    tk.Label(wordlist_frame, text="Year (e.g., 2001):", bg="#ffffff").pack(anchor='w')
    date_entry = tk.Entry(wordlist_frame, width=30)
    date_entry.pack(pady=2)

    tk.Button(wordlist_frame, text="Generate Wordlist", bg="#ff6600", fg="white",
              font=("Segoe UI", 10, "bold"), command=handle_generate_wordlist).pack(pady=8)

    wordlist_box = scrolledtext.ScrolledText(wordlist_frame, height=10, width=50, wrap=tk.WORD)
    wordlist_box.pack()

    # Bottom Frame for Export Button
    export_frame = tk.Frame(root, bg="#e6f2ff")
    export_frame.pack(pady=10)

    tk.Button(export_frame, text="💾 Export Wordlist as .txt", bg="#28a745", fg="white",
              font=("Segoe UI", 10, "bold"), command=handle_export_wordlist).pack()

    root.mainloop()

main()
