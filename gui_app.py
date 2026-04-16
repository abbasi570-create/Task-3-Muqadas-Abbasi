import tkinter as tk
from tkinter import messagebox

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Recommendation System")
        self.root.geometry("500x500")

        self.items = {
            "Python Masterclass": ["programming", "python", "ai"],
            "Data Science Bootcamp": ["ai", "data", "math"],
            "Yoga for Beginners": ["fitness", "health"],
            "Digital Marketing": ["business", "marketing"]
        }

        self.label = tk.Label(root, text="Enter Interests (comma separated):")
        self.label.pack(pady=10)

        self.entry = tk.Entry(root, width=40)
        self.entry.pack(pady=5)

        self.btn = tk.Button(root, text="Get Recommendations", command=self.recommend)
        self.btn.pack(pady=10)

        self.output = tk.Text(root, height=15, width=50)
        self.output.pack(pady=10)

    def recommend(self):
        user_input = self.entry.get().lower()
        user_interests = set([i.strip() for i in user_input.split(",")])

        results = []

        for item, tags in self.items.items():
            score = len(user_interests & set(tags))
            if score > 0:
                results.append((item, score))

        results.sort(key=lambda x: x[1], reverse=True)

        self.output.delete("1.0", tk.END)

        if results:
            for r in results:
                self.output.insert(tk.END, f"{r[0]} ({r[1]} matches)\n")
        else:
            self.output.insert(tk.END, "No recommendations found")

root = tk.Tk()
app = App(root)
root.mainloop()