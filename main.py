import tkinter as tk
from tkinter import ttk, messagebox
import os

def edit_distance(word1: str, word2: str) -> int:
    m = len(word1)
    n = len(word2)

    # Initialize a (m+1) x (n+1) matrix
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    # Base cases:
    for i in range(m + 1):
        dp[i][0] = i  # Deletions
    for j in range(n + 1):
        dp[0][j] = j  # Insertions

    # Fill the DP matrix
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j],    # deletion
                                   dp[i][j - 1],    # insertion
                                   dp[i - 1][j - 1])  # substitution

    return dp[m][n]

def phrase_edit_distance(phrase1: str, phrase2: str) -> int:
    words1 = phrase1.strip().split()
    words2 = phrase2.strip().split()

    if len(words1) != len(words2):
        return float('inf')

    total_distance = 0
    for w1, w2 in zip(words1, words2):
        dist = edit_distance(w1, w2)
        total_distance += dist
        if total_distance > 2:
            break
    return total_distance


def suggest_corrections(query: str, dictionary: list) -> list:
    suggestions = []
    for candidate in dictionary:
        dist = phrase_edit_distance(query, candidate)
        if dist <= 2:
            suggestions.append((candidate, dist))
    suggestions.sort(key=lambda x: x[1])
    return suggestions


def load_dictionary(file_path: str) -> list:

    if not os.path.exists(file_path):
        messagebox.showerror("Error", f"The file '{file_path}' was not found.")
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            # Read and strip each line to remove leading/trailing whitespaces
            dictionary = [line.strip() for line in f if line.strip()]
        return dictionary
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading the dictionary:\n{e}")
        return []


def create_gui(dictionary: list):

    root = tk.Tk()
    root.title("Autocorrect Suggestion Tool")
    root.geometry("700x500")
    root.resizable(False, False)

    # Style configuration
    style = ttk.Style(root)
    style.configure('TButton', font=('Helvetica', 12))
    style.configure('TLabel', font=('Helvetica', 12))
    style.configure('TEntry', font=('Helvetica', 12))
    style.configure('Treeview', font=('Helvetica', 12))
    style.configure("Treeview.Heading", font=('Helvetica', 12, 'bold'))

    # Title Label
    title_label = ttk.Label(root, text="Autocorrect Suggestion Tool", font=('Helvetica', 16, 'bold'))
    title_label.pack(pady=10)

    # Frame for input
    input_frame = ttk.Frame(root)
    input_frame.pack(pady=10, padx=20, fill='x')

    query_label = ttk.Label(input_frame, text="Enter your query phrase:")
    query_label.pack(side='left', padx=(0, 10))

    query_var = tk.StringVar()
    query_entry = ttk.Entry(input_frame, textvariable=query_var, width=50)
    query_entry.pack(side='left', fill='x', expand=True)
    query_entry.focus()

    # Submit Button
    submit_button = ttk.Button(root, text="Get Suggestions")

    submit_button.pack(pady=10)

    # Frame for suggestions
    suggestions_frame = ttk.Frame(root)
    suggestions_frame.pack(pady=10, padx=20, fill='both', expand=True)

    # Treeview for displaying suggestions
    columns = ('Phrase', 'Edit Distance')
    tree = ttk.Treeview(suggestions_frame, columns=columns, show='headings', height=15)
    tree.heading('Phrase', text='Suggested Phrase')
    tree.heading('Edit Distance', text='Edit Distance')
    tree.column('Phrase', anchor='w', width=500)
    tree.column('Edit Distance', anchor='center', width=150)
    tree.pack(side='left', fill='both', expand=True)

    # Scrollbar for the Treeview
    scrollbar = ttk.Scrollbar(suggestions_frame, orient='vertical', command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    def on_submit():

        query = query_var.get().strip()
        if not query:
            messagebox.showwarning("Input Required", "Please enter a query phrase.")
            return
        # Get suggestions
        results = suggest_corrections(query, dictionary)
        # Clear previous suggestions
        for item in tree.get_children():
            tree.delete(item)
        if results:
            for phrase, dist in results:
                tree.insert('', 'end', values=(phrase, dist))
        else:
            messagebox.showinfo("No Suggestions", "No suggestions found within the specified edit distance threshold.")

    # Bind the submit button
    submit_button.config(command=on_submit)

    # Bind Enter key to submit
    root.bind('<Return>', lambda event: on_submit())

    # Start the GUI event loop
    root.mainloop()


def main():
    dictionary_file = "dictionary.txt"

    dictionary = load_dictionary(dictionary_file)
    if not dictionary:
        return

    create_gui(dictionary)


if __name__ == "__main__":
    main()
