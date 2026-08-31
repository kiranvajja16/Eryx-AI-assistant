from app.services.database import get_connection

def create_reminder(task: str,time:str)-> str:

    connection=get_connection()
    cursor=connection.cursor()

    cursor.execute("""
        INSERT INTO reminders(task,reminder_time) VALUES(?,?)
    """,(task,time))

    connection.commit()
    connection.close()

    return f"Reminder created for '{task}' at {time}."


def get_reminders() -> str:

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT task, reminder_time
        FROM reminders
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    if not rows:
        return "You don't have any reminders."

    result = []

    for task, reminder_time in rows:
        result.append(
            f"{task} at {reminder_time}"
        )

    return "\n".join(result)

