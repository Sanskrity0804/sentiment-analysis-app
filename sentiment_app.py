import tkinter as tk
from tkinter import ttk, messagebox

class EnhancedSentimentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Enhanced Sentiment Analysis")
        self.root.geometry("550x450")
        
        # Sentiment word lists
        self.positive_words = {
            "good", "great", "excellent", "happy", "joy", "love", 
            "wonderful", "awesome", "fantastic", "amazing", "best",
            "super", "positive", "perfect", "brilliant", "favorite"
        }
        self.negative_words = {
            "bad", "terrible", "awful", "hate", "sad", "angry",
            "worst", "horrible", "dislike", "upset", "annoying",
            "poor", "negative", "awful", "disappointing", "mess"
        }
        self.intensifiers = {"very", "extremely", "really", "super", "absolutely"}
        self.positive_emojis = {"😊", "👍", "❤️", "😍", "🎉"}
        self.negative_emojis = {"😞", "👎", "💔", "😠", "😢"}
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title
        title = ttk.Label(self.root, text="Enhanced Sentiment Analyzer", font=("Arial", 14))
        title.pack(pady=10)
        
        # Text entry
        self.text_entry = tk.Text(self.root, height=12, width=60)
        self.text_entry.pack(pady=10, padx=10)
        
        # Button frame
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(pady=5)
        
        # Buttons
        analyze_btn = ttk.Button(btn_frame, text="Analyze", command=self.analyze)
        analyze_btn.pack(side="left", padx=5)
        
        clear_btn = ttk.Button(btn_frame, text="Clear", command=self.clear_text)
        clear_btn.pack(side="left", padx=5)
        
        save_btn = ttk.Button(btn_frame, text="Save", command=self.save_results)
        save_btn.pack(side="left", padx=5)
        
        # Result frame
        result_frame = ttk.LabelFrame(self.root, text="Analysis Result", padding=10)
        result_frame.pack(pady=10, padx=10, fill="both", expand=True)
        
        # Result label
        self.result_label = ttk.Label(result_frame, text="", font=("Arial", 11))
        self.result_label.pack()
    
    def analyze(self):
        text = self.text_entry.get("1.0", "end-1c").lower()
        
        if not text.strip():
            messagebox.showwarning("Warning", "Please enter some text!")
            return
        
        # Initialize counts
        positive_count = 0
        negative_count = 0
        
        # Count positive/negative words
        words = text.split()
        for i, word in enumerate(words):
            if word in self.positive_words:
                positive_count += 1
            elif word in self.negative_words:
                negative_count += 1
            
            # Check for intensifiers
            if i > 0 and words[i-1] in self.intensifiers:
                if word in self.positive_words:
                    positive_count += 0.5  # Extra weight for intensified positive
                elif word in self.negative_words:
                    negative_count += 0.5  # Extra weight for intensified negative
        
        # Count emojis
        positive_count += sum(1 for char in text if char in self.positive_emojis)
        negative_count += sum(1 for char in text if char in self.negative_emojis)
        
        # Determine sentiment
        if positive_count > negative_count:
            result = "POSITIVE"
            color = "green"
        elif negative_count > positive_count:
            result = "NEGATIVE"
            color = "red"
        else:
            result = "NEUTRAL"
            color = "blue"
        
        # Show detailed result
        self.result_label.config(
            text=f"Sentiment: {result}\n\n"
                 f"Positive score: {positive_count:.1f}\n"
                 f"Negative score: {negative_count:.1f}\n\n"
                 f"Text analyzed:\n{text[:100]}{'...' if len(text) > 100 else ''}",
            foreground=color
        )
    
    def clear_text(self):
        self.text_entry.delete("1.0", "end")
        self.result_label.config(text="")
    
    def save_results(self):
        result = self.result_label.cget("text")
        if result:
            with open("sentiment_results.txt", "a", encoding="utf-8") as f:
                f.write(f"{'-'*50}\n{result}\n\n")
            messagebox.showinfo("Saved", "Results saved to sentiment_results.txt")
        else:
            messagebox.showwarning("Warning", "No results to save")

if __name__ == "__main__":
    root = tk.Tk()
    app = EnhancedSentimentApp(root)
    root.mainloop()