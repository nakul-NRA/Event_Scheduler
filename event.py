import tkinter as tk
from tkinter import messagebox
from datetime import datetime
from winotify import Notification, audio

def add_event():
    name = event_name_entry.get()
    date = event_date_entry.get()
    time = event_time_entry.get()
    note = event_note_entry.get("1.0", tk.END)

    event_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
    current_datetime = datetime.now()

    if event_datetime < current_datetime:
        messagebox.showerror("Event Planner", "Event time should be in the future!")
        return

    event = {
        "name": name,
        "datetime": event_datetime,
        "note": note
    }
    events.append(event)
    messagebox.showinfo("Event Planner", "Event added successfully!")

def show_notification(event):
    notification_title = event["name"]
    notification_message = f"Note: {event['note']}"

    toast = Notification(
        app_id="NeuralNine Script",
        title=notification_title,
        msg=notification_message,
        duration="long",
        # icon_path="path/to/icon.png",  # Replace with your own icon path
        # bg_color=(255, 0, 0),  # Set the background color to red (RGB values)
        # text_color=(255, 255, 255)  # Set the text color to white (RGB values)
    )
    toast.set_audio(audio.LoopingCall, loop=True)
    toast.show()

def check_events():
    current_datetime = datetime.now()
    for event in events:
        event_datetime = event["datetime"]
        if event_datetime <= current_datetime:
            show_notification(event)
            events.remove(event)

    window.after(1000, check_events)

# Create the main window
window = tk.Tk()
window.title("Event Planner")
window.geometry("400x400")
window.config(bg="#F0F0F0")

# Create event section
event_label = tk.Label(window, text="Add Event", font=("Arial", 14, "bold"), bg="#F0F0F0")
event_label.pack(pady=10)

event_name_label = tk.Label(window, text="Event Name:", bg="#F0F0F0")
event_name_label.pack()
event_name_entry = tk.Entry(window)
event_name_entry.pack()

event_date_label = tk.Label(window, text="Event Date (YYYY-MM-DD):", bg="#F0F0F0")
event_date_label.pack()
event_date_entry = tk.Entry(window)
event_date_entry.pack()

event_time_label = tk.Label(window, text="Event Time (HH:MM):", bg="#F0F0F0")
event_time_label.pack()
event_time_entry = tk.Entry(window)
event_time_entry.pack()

event_note_label = tk.Label(window, text="Event Note:", bg="#F0F0F0")
event_note_label.pack()
event_note_entry = tk.Text(window, height=3)
event_note_entry.pack()

add_event_button = tk.Button(window, text="Add Event", command=add_event, bg="#4CAF50", fg="#FFFFFF")
add_event_button.pack(pady=10)

# Start the event checker
events = []
check_events()

# Start the GUI event loop
window.mainloop()
