from app.services.database import get_connection

def save_note(note:str)->str:


    connection=get_connection()
    cursor=connection.cursor()

    cursor.execute(
        """
            INSERT INTO notes(note)
            VALUES(?)
        """,(note,)
    )

    connection.commit()
    connection.close()

    return f"Note saved successfully: {note}"


def get_notes() -> str:

    connection = get_connection()

    cursor = connection.cursor()

    cursor.execute(
        """
        SELECT note, created_at
        FROM notes
        ORDER BY id DESC
        """
    )

    rows = cursor.fetchall()

    connection.close()

    if not rows:
        return "You don't have any saved notes."

    result = []

    for note, created_at in rows:
        result.append(
            f"{created_at}: {note}"
        )

    return "\n".join(result)