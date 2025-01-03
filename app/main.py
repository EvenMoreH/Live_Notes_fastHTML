import os
from datetime import datetime
from fasthtml.common import * # type: ignore
from fasthtml.common import (
    Html, Head, Body, Div, Title, Link, Meta, Script, Form, Textarea, serve, Path
)

# for Docker
app, rt = fast_app(static_path="static") # type: ignore

# for local
# app, rt = fast_app(static_path="app/static") # type: ignore

# handling content files
content_dir = Path("content")
content_dir.mkdir(parents=True, exist_ok=True)

# file to store the notepad content
FILE_PATH = f"{content_dir}/notepad_content.txt"

# load content from file if it exists
if os.path.exists(FILE_PATH):
    with open(FILE_PATH, "r") as file:
        notepad_content = file.read()
else:
    notepad_content = "Write your notes here..."

def get_last_saved_time(FILE_PATH):
    if os.path.exists(FILE_PATH):
        # get the last modification time of persistent file as a timestamp
        saved_time = os.path.getmtime(FILE_PATH)
        # convert timestamp to a readable format
        return datetime.fromtimestamp(saved_time).strftime("%d-%m-%Y %H:%M")
    return "File does not exist."

@rt("/")
def notepad():
    saved_time = get_last_saved_time(FILE_PATH)
    print(f"LOG #1: file loaded: {FILE_PATH}")

    return Html(
        Head(
            Title("Live Notepad"),
            Meta(name="viewport", content="width=device-width, initial-scale=1"),
            Script(src="https://unpkg.com/htmx.org"),
            Link(rel="stylesheet", href="styles.css"),
            Link(rel="icon", href="images/favicon.ico", type="image/x-icon"),
            Link(rel="icon", href="images/favicon.png", type="image/png"),
        ),
        Body(
            Form(Textarea(notepad_content,
                        id="notepad",
                        name="content",
                        rows=20,
                        cols=80,
                        hx_post="/autosave",
                        hx_trigger="keyup changed",
                        hx_target="#save-status",
                        style="width:100%; font-size:1.2rem; padding:10px;"),
                Div(f"Last saved on {saved_time}", id="save-status", style="margin-top:10px; color:gray;"),
                cls="container",
                )
        )
    )

# autosaving endpoint
@rt("/autosave")
def autosave(content: str):
    with open(FILE_PATH, "w") as file:
        # reading current time to indicate when text was saved
        last_saved = datetime.now().strftime('%d-%m-%Y %H:%M')
        print(f"LOG #2: file saved: {FILE_PATH}")
        file.write(content)

    return Div(f"Changes saved on {last_saved}", id="save-status", style="color:green; margin-top:10px; padding-top:10;")

if __name__ == '__main__':
    # Important: Use host='0.0.0.0' to make the server accessible outside the container
    serve(host='0.0.0.0', port=5013)