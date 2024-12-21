import tkinter as tk
from tkinter import ttk, messagebox
import os

def edit_distance(word1: str, word2: str) -> int:
    m = len(word1)
    n = len(word2)

    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],    # fshirje
                    dp[i][j - 1],    # shtim
                    dp[i - 1][j - 1] # zëvendësim
                )

    return dp[m][n]

def normalize_phrase(phrase: str) -> str:
    return ' '.join(phrase.lower().strip().split())

def phrase_edit_distance(phrase1: str, phrase2: str) -> int:
    words1 = phrase1.strip().split()
    words2 = phrase2.strip().split()

    m, n = len(words1), len(words2)
    # Kosto operacionesh në nivel fraze
    insert_delete_cost = 2

    dp = [[0]*(n+1) for _ in range(m+1)]

    for i in range(1, m+1):
        dp[i][0] = dp[i-1][0] + insert_delete_cost

    for j in range(1, n+1):
        dp[0][j] = dp[0][j-1] + insert_delete_cost

    for i in range(1, m+1):
        for j in range(1, n+1):
            if words1[i-1] == words2[j-1]:
                dp[i][j] = dp[i-1][j-1]
            else:
                replace_cost = edit_distance(words1[i-1], words2[j-1])
                # Sigurohemi që zëvendësimi të ketë të paktën koston 1
                replace_cost = max(1, replace_cost)
                dp[i][j] = min(
                    dp[i-1][j] + insert_delete_cost,       # fshirje e një fjale
                    dp[i][j-1] + insert_delete_cost,       # shtim i një fjale
                    dp[i-1][j-1] + replace_cost            # zëvendësim i një fjale
                )

    return dp[m][n]

def suggest_corrections(query: str, dictionary: list, max_distance=2) -> list:
    query_norm = normalize_phrase(query)
    words_query = query_norm.split()

    suggestions = []
    for candidate in dictionary:
        candidate_norm = normalize_phrase(candidate)
        words_candidate = candidate_norm.split()

        # Filtër paraprak: nëse diferenca në gjatësi të fjalëve
        # është më e madhe se max_distance, vazhdo tjetrin
        if abs(len(words_query) - len(words_candidate)) > max_distance:
            continue

        dist = phrase_edit_distance(query_norm, candidate_norm)
        if dist <= max_distance:
            suggestions.append((candidate, dist))

    # Sort sipas distance, pastaj alfabetikisht për rezultate me të njëjtën distancë
    suggestions.sort(key=lambda x: (x[1], x[0]))
    return suggestions

def load_dictionary(file_path: str) -> list:
    if not os.path.exists(file_path):
        messagebox.showerror("Error", f"The file '{file_path}' was not found.")
        return []
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            dictionary = [line.strip() for line in f if line.strip()]
        return dictionary
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while reading the dictionary:\n{e}")
        return []

def create_gui(dictionary: list):
    root = tk.Tk()
    root.title("Autocorrect Suggestion Tool")
    root.geometry("750x550")
    root.resizable(False, False)

    style = ttk.Style(root)
    style.configure('TButton', font=('Helvetica', 12))
    style.configure('TLabel', font=('Helvetica', 12))
    style.configure('TEntry', font=('Helvetica', 12))
    style.configure('Treeview', font=('Helvetica', 12))
    style.configure("Treeview.Heading", font=('Helvetica', 12, 'bold'))

    # Title Label
    title_label = ttk.Label(root, text="Autocorrect Suggestion Tool", font=('Helvetica', 16, 'bold'))
    title_label.pack(pady=10)

    # Frame për input
    input_frame = ttk.Frame(root)
    input_frame.pack(pady=10, padx=20, fill='x')

    query_label = ttk.Label(input_frame, text="Enter your query phrase:")
    query_label.pack(side='left', padx=(0, 10))

    query_var = tk.StringVar()
    query_entry = ttk.Entry(input_frame, textvariable=query_var, width=50)
    query_entry.pack(side='left', fill='x', expand=True)
    query_entry.focus()

    # Frame për max distance
    distance_frame = ttk.Frame(root)
    distance_frame.pack(pady=10, padx=20, fill='x')

    distance_label = ttk.Label(distance_frame, text="Edit Distance Threshold:")
    distance_label.pack(side='left', padx=(0, 10))

    distance_var = tk.IntVar(value=2)
    distance_spin = ttk.Spinbox(distance_frame, from_=0, to=10, textvariable=distance_var, width=5)
    distance_spin.pack(side='left', padx=(0, 10))

    # Submit Button
    submit_button = ttk.Button(root, text="Get Suggestions")
    submit_button.pack(pady=10)

    # Frame për suggestions
    suggestions_frame = ttk.Frame(root)
    suggestions_frame.pack(pady=10, padx=20, fill='both', expand=True)

    # Treeview për të shfaqur suggestions
    columns = ('Phrase', 'Edit Distance')
    tree = ttk.Treeview(suggestions_frame, columns=columns, show='headings', height=15)
    tree.heading('Phrase', text='Suggested Phrase')
    tree.heading('Edit Distance', text='Edit Distance')
    tree.column('Phrase', anchor='w', width=500)
    tree.column('Edit Distance', anchor='center', width=150)
    tree.pack(side='left', fill='both', expand=True)

    # Scrollbar
    scrollbar = ttk.Scrollbar(suggestions_frame, orient='vertical', command=tree.yview)
    tree.configure(yscroll=scrollbar.set)
    scrollbar.pack(side='right', fill='y')

    def on_submit():
        query = query_var.get().strip()
        if not query:
            messagebox.showwarning("Input Required", "Please enter a query phrase.")
            return
        max_dist = distance_var.get()
        results = suggest_corrections(query, dictionary, max_distance=max_dist)

        # Fshijmë suggestions e mëparshme
        for item in tree.get_children():
            tree.delete(item)

        if results:
            for phrase, dist in results:
                tree.insert('', 'end', values=(phrase, dist))
            # Shfaqim numrin e rezultateve në titull ose në një messagebox
            # messagebox.showinfo("Suggestions", f"Found {len(results)} suggestions.")
        else:
            messagebox.showinfo("No Suggestions", "No suggestions found within the specified edit distance threshold.")

    submit_button.config(command=on_submit)
    root.bind('<Return>', lambda event: on_submit())

    root.mainloop()

def main():
    dictionary_file = "dictionary.txt"
    dictionary = load_dictionary(dictionary_file)
    if not dictionary:
        return
    create_gui(dictionary)

if __name__ == "__main__":
    main()
