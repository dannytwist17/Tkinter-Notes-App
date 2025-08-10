import tkinter as tk
from tkinter import messagebox, simpledialog
import json
import os
from datetime import datetime

DATA_FILE = "notes.json"


def load_notes():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            loaded_notes = json.load(f)
        
        for note in loaded_notes:
            if "timestamp" not in note:
                note["timestamp"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_notes_to_file(loaded_notes)
        return loaded_notes
    return []

def save_notes_to_file(notes_list):
    with open(DATA_FILE, "w") as f:
        json.dump(notes_list, f, indent=4)


def save_note():
    title = title_entry.get().strip()
    content = note_input.get('1.0', tk.END).strip()
    if not content:
        messagebox.showwarning('Empty', 'Write something before saving.')
        return
    if not title:
        title = 'Untitled'

    note = {
        "title": title,
        "content": content,
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    notes.append(note)
    save_notes_to_file(notes)
    messagebox.showinfo('Saved', 'Note saved successfully.')
    title_entry.delete(0, tk.END)
    note_input.delete('1.0', tk.END)
    update_count()

def view_notes():
    if not notes:
        messagebox.showinfo('No Notes', 'No notes to display.')
        return

    view_window = tk.Toplevel(window)
    view_window.title('All Notes')
    view_window.geometry('400x400')

    listbox = tk.Listbox(view_window, width=50)
    listbox.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    delete_button = tk.Button(view_window, text='Delete Note', command=lambda: delete_note_from_list(listbox))
    delete_button.pack(pady=5)

    for i, note in enumerate(notes, start=1):
        display_text = f'{i}. {note["title"]} - {note["timestamp"]}'
        listbox.insert(tk.END, display_text)

    def show_note_details(event):
        selection = listbox.curselection()
        if selection:
            index = selection[0]
            selected_note = notes[index]
            messagebox.showinfo(
                selected_note['title'],
                f"{selected_note['content']}\n\nSaved on {selected_note['timestamp']}"
            )

    listbox.bind('<Double-1>', show_note_details)

def delete_note_from_list(listbox):
    selected_index = listbox.curselection()
    if not selected_index:
        messagebox.showwarning('No selection', 'Please select a note to delete.')
        return

    index = selected_index[0]
    title = notes[index]['title']

    confirm = messagebox.askyesno('Confirm Deletion', f'Are you sure you want to delete "{title}"?')
    if confirm:
        del notes[index]
        save_notes_to_file(notes)
        listbox.delete(index)
        update_count()
        messagebox.showinfo('Deleted', f'Note "{title}" has been deleted.')

def edit_note():
    selected_title = simpledialog.askstring('Edit Note', 'Enter the title of the note to edit:')
    if not selected_title:
        return

    for i, note in enumerate(notes):
        if note['title'].lower() == selected_title.lower():
            new_content = simpledialog.askstring('Edit Content', 'Enter new content:')
            if new_content:
                note['content'] = new_content
                note['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                save_notes_to_file(notes)
                messagebox.showinfo('Edited', f'Note "{selected_title}" has been updated.')
            return

    messagebox.showerror('Not Found', f'No note found with title "{selected_title}".')

def search_notes():
    keyword = simpledialog.askstring('Search Notes', 'Enter keyword to search:')
    if not keyword:
        return

    results = [note for note in notes if keyword.lower() in note['title'].lower() or keyword.lower() in note['content'].lower()]

    if results:
        results_window = tk.Toplevel(window)
        results_window.title('Search Results')

        listbox = tk.Listbox(results_window, width=50, height=10)
        listbox.pack(padx=10, pady=10)

        for note in results:
            listbox.insert(tk.END, f"{note['title']} - {note['timestamp']}")
    else:
        messagebox.showinfo('Search Results', 'No matching notes found.')

def update_count():
    count_label.config(text=f"Total Notes: {len(notes)}")


window = tk.Tk()
window.title("Notes App")
window.geometry("400x500")

title_entry = tk.Entry(window, width=40)
title_entry.pack(pady=5)
title_entry.insert(0, "Enter title...")

note_input = tk.Text(window, width=40, height=10)
note_input.pack(pady=5)

save_button = tk.Button(window, text="Save Note", command=save_note)
save_button.pack(pady=5)

view_button = tk.Button(window, text="View Notes", command=view_notes)
view_button.pack(pady=5)

edit_button = tk.Button(window, text="Edit Note", command=edit_note)
edit_button.pack(pady=5)

search_button = tk.Button(window, text="Search Notes", command=search_notes)
search_button.pack(pady=5)

count_label = tk.Label(window, text="Total Notes: 0")
count_label.pack(pady=5)

notes = load_notes()
update_count()

window.mainloop()
