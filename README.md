# Google Keep Clone (Flask & Tailwind CSS)

A full-stack web application replicating core features of Google Keep. Built with a **Flask (Python)** backend REST API and a lightweight **Tailwind CSS + Vanilla JavaScript** frontend.

---

## Features

- **Create Notes**: Add notes with titles, content, and dynamic color themes.
- **Pin Notes**: Keep high-priority notes at the top in a dedicated pinned section.
- **Edit & Update**: Inline modal editor to update existing titles and content.
- **Delete Notes**: Instant removal of unwanted notes.
- **Real-Time Search**: Filter through notes by title or content as you type.
- **RESTful API**: Clean Flask API endpoints (`GET`, `POST`, `PUT`, `DELETE`).

---

## Project Structure

```text
learn git/
├── app.py                 # Flask server & REST API routes
├── templates/
│   └── index.html         # Tailwind CSS frontend & JavaScript logic
├── .venv/                 # Python virtual environment
└── README.md              # Project documentation