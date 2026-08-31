from app.services.database import initialize_database
from app.tools.notes_tool import save_note, get_notes
from app.tools.reminder_tool import create_reminder, get_reminders


initialize_database()


print(save_note("Finish ERYX AI Assistant project"))

print(create_reminder(
    "Study Python",
    "7 PM"
))

print("\nNOTES:")
print(get_notes())

print("\nREMINDERS:")
print(get_reminders())