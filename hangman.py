import tkinter as tk
from tkinter import messagebox, simpledialog

import wordlist

MAX_WRONG = 10


def get_word():
    return wordlist.get_random_word().upper()


def add_spaces(text):
    return " ".join(text)


class HangmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman")
        self.root.geometry("760x480")
        self.root.resizable(False, False)

        self.current_word = ""
        self.guessed_letters = set()
        self.num_wrong = 0
        self.num_guesses = 0

        self.main_frame = tk.Frame(self.root, padx=24, pady=24)
        self.main_frame.pack(fill="both", expand=True)

        self.show_menu()

    def clear_frame(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

    def show_menu(self):
        self.clear_frame()

        title = tk.Label(self.main_frame, text="Welcome to Hangman!", font=("Helvetica", 28, "bold"))
        title.pack(pady=(40, 30))

        subtitle = tk.Label(self.main_frame, text="Choose an option", font=("Helvetica", 14))
        subtitle.pack(pady=(0, 20))

        tk.Button(self.main_frame, text="Play Game", width=18, height=2, command=self.start_game).pack(pady=8)
        tk.Button(self.main_frame, text="Add Word", width=18, height=2, command=self.add_word).pack(pady=8)
        tk.Button(self.main_frame, text="Quit", width=18, height=2, command=self.root.quit).pack(pady=8)

    def start_game(self):
        self.current_word = get_word()
        self.guessed_letters = set()
        self.num_wrong = 0
        self.num_guesses = 0
        self.show_game_screen()

    def show_game_screen(self):
        self.clear_frame()

        tk.Label(self.main_frame, text="Hangman", font=("Helvetica", 24, "bold")).pack(pady=(5, 10))

        self.hangman_canvas = tk.Canvas(
            self.main_frame,
            width=280,
            height=220,
            bg="white",
            highlightthickness=1,
            highlightbackground="#cccccc",
        )
        self.hangman_canvas.pack(pady=(0, 12))

        self.word_label = tk.Label(self.main_frame, text="", font=("Courier", 30, "bold"))
        self.word_label.pack(pady=(10, 15))

        self.stats_label = tk.Label(self.main_frame, text="", font=("Helvetica", 12))
        self.stats_label.pack(pady=(0, 8))

        self.tried_label = tk.Label(self.main_frame, text="", font=("Helvetica", 11))
        self.tried_label.pack(pady=(0, 20))

        input_row = tk.Frame(self.main_frame)
        input_row.pack(pady=(0, 12))

        tk.Label(input_row, text="Guess a letter:", font=("Helvetica", 11)).pack(side="left", padx=(0, 8))
        self.guess_entry = tk.Entry(input_row, width=6, font=("Helvetica", 14), justify="center")
        self.guess_entry.pack(side="left")
        self.guess_entry.bind("<Return>", self.submit_guess)

        tk.Button(self.main_frame, text="Submit Guess", command=self.submit_guess, width=14).pack(pady=6)
        tk.Button(self.main_frame, text="Back to Menu", command=self.show_menu, width=14).pack(pady=6)

        self.message_label = tk.Label(self.main_frame, text="", fg="blue", font=("Helvetica", 11))
        self.message_label.pack(pady=(10, 0))

        self.refresh_game_labels()
        self.guess_entry.focus_set()

    def get_displayed_word(self):
        displayed = []
        for letter in self.current_word:
            if not letter.isalpha() or letter in self.guessed_letters:
                displayed.append(letter)
            else:
                displayed.append("_")
        return "".join(displayed)

    def refresh_game_labels(self):
        displayed_word = self.get_displayed_word()
        self.word_label.config(text=add_spaces(displayed_word))
        self.draw_hangman()

        self.stats_label.config(
            text=f"Guesses: {self.num_guesses}    Wrong: {self.num_wrong}/{MAX_WRONG}"
        )

        tried_text = " ".join(sorted(self.guessed_letters)) if self.guessed_letters else "(none yet)"
        self.tried_label.config(text=f"Tried letters: {tried_text}")

    def draw_hangman(self):
        c = self.hangman_canvas
        c.delete("all")

        # Draw one stage per wrong guess.
        stages = [
            lambda: c.create_line(20, 200, 160, 200, width=4),   # base
            lambda: c.create_line(50, 200, 50, 25, width=4),     # pole
            lambda: c.create_line(50, 25, 160, 25, width=4),     # beam
            lambda: c.create_line(160, 25, 160, 52, width=4),    # rope
            lambda: c.create_oval(142, 52, 178, 88, width=3),    # head
            lambda: c.create_line(160, 88, 160, 136, width=3),   # body
            lambda: c.create_line(160, 102, 130, 120, width=3),  # left arm
            lambda: c.create_line(160, 102, 190, 120, width=3),  # right arm
            lambda: c.create_line(160, 136, 136, 170, width=3),  # left leg
            lambda: c.create_line(160, 136, 184, 170, width=3),  # right leg
        ]

        to_draw = min(self.num_wrong, len(stages))
        for i in range(to_draw):
            stages[i]()

    def submit_guess(self, _event=None):
        raw = self.guess_entry.get().strip().upper()
        self.guess_entry.delete(0, tk.END)

        if len(raw) != 1 or not raw.isalpha():
            self.message_label.config(text="Enter exactly one letter (A-Z).", fg="red")
            return

        if raw in self.guessed_letters:
            self.message_label.config(text=f"You already tried '{raw}'.", fg="red")
            return

        self.guessed_letters.add(raw)
        self.num_guesses += 1

        if raw in self.current_word:
            self.message_label.config(text=f"Nice! '{raw}' is in the word.", fg="green")
        else:
            self.num_wrong += 1
            self.message_label.config(text=f"Sorry, '{raw}' is not in the word.", fg="red")

        self.refresh_game_labels()
        self.check_game_end()

    def check_game_end(self):
        displayed = self.get_displayed_word()

        if "_" not in displayed:
            messagebox.showinfo("You Win", f"Great job! You guessed: {self.current_word}")
            self.show_menu()
            return

        if self.num_wrong >= MAX_WRONG:
            messagebox.showinfo("Game Over", f"Out of guesses. The word was: {self.current_word}")
            self.show_menu()

    def add_word(self):
        new_word = simpledialog.askstring("Add Word", "Enter a new word to add:", parent=self.root)

        if new_word is None:
            return

        cleaned = new_word.strip().lower()
        if not cleaned:
            messagebox.showerror("Invalid Word", "Please enter a non-empty word.")
            return

        if not any(ch.isalpha() for ch in cleaned):
            messagebox.showerror("Invalid Word", "Word must include at least one letter.")
            return

        if cleaned in wordlist.words:
            messagebox.showinfo("Already Exists", f"'{cleaned}' is already in the list.")
            return

        wordlist.words.append(cleaned)
        messagebox.showinfo("Word Added", f"Added '{cleaned}' to this session's word list.")


def main():
    root = tk.Tk()
    HangmanGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()