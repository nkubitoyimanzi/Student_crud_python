from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qs, urlparse
from html import escape
from database import initialize_database
from repository import (get_students, create_student,
                        update_student, delete_student, get_one_student,
                        student_count, get_students_page)
CSS = """
:root {
    --primary: #4f46e5;
    --primary-dark: #4338ca;
    --danger: #ef4444;
    --text: #1f2937;
    --muted: #6b7280;
    --line: #eef0f4;
    --bg: #f3f4f8;
}
* {
    box-sizing: border-box;
}
body {
    font-family: "Segoe UI", system-ui, -apple-system, Roboto, Arial, sans-serif;
    background-color: var(--bg);
    background-image: linear-gradient(180deg, #e0e7ff 0%, rgba(243, 244, 248, 0) 320px);
    background-repeat: no-repeat;
    color: var(--text);
    margin: 0;
    padding: 40px 16px;
}
.container {
    max-width: 720px;
    margin: 0 auto;
}
h1 {
    text-align: center;
    font-size: 30px;
    letter-spacing: -0.5px;
    color: #1e1b4b;
    margin: 0 0 28px 0;
}
.card {
    background: white;
    padding: 26px;
    border-radius: 14px;
    border: 1px solid rgba(17, 24, 39, 0.05);
    box-shadow: 0 1px 2px rgba(16, 24, 40, 0.04), 0 10px 30px rgba(16, 24, 40, 0.08);
    margin-bottom: 24px;
}
h2 {
    margin: 0;
    font-size: 20px;
    color: #1e1b4b;
}
.card > h2 {
    margin-bottom: 18px;
}
.card-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 18px;
}

label {
    font-size: 13px;
    font-weight: 600;
    color: var(--muted);
}
input {
    width: 100%;
    padding: 11px 14px;
    margin: 6px 0 16px 0;
    border: 1px solid #d9dde6;
    border-radius: 10px;
    font-size: 15px;
    font-family: inherit;
    color: var(--text);
    transition: border-color 0.15s, box-shadow 0.15s;
}
input:focus {
    outline: none;
    border-color: var(--primary);
    box-shadow: 0 0 0 4px rgba(79, 70, 229, 0.15);
}

button, .btn-primary {
    display: inline-block;
    padding: 11px 20px;
    border: 1px solid transparent;
    border-radius: 10px;
    cursor: pointer;
    color: white;
    background: var(--primary);
    font-family: inherit;
    font-size: 15px;
    font-weight: 600;
    text-decoration: none;
    box-shadow: 0 1px 2px rgba(79, 70, 229, 0.3);
    transition: background 0.15s, transform 0.15s;
}
button:hover, .btn-primary:hover {
    background: var(--primary-dark);
    transform: translateY(-1px);
}
button:active {
    transform: none;
}
.btn-cancel {
    display: inline-block;
    padding: 11px 20px;
    border: 1px solid #d9dde6;
    border-radius: 10px;
    color: var(--muted);
    background: white;
    font-size: 15px;
    font-weight: 600;
    text-decoration: none;
    transition: background 0.15s, color 0.15s;
}
.btn-cancel:hover {
    background: #f9fafb;
    color: var(--text);
}
.form-actions {
    display: flex;
    gap: 10px;
    margin-top: 6px;
}

table {
    width: 100%;
    border-collapse: collapse;
}
th {
    text-align: left;
    padding: 10px 12px;
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #9ca3af;
    border-bottom: 1px solid var(--line);
}
td {
    padding: 14px 12px;
    border-bottom: 1px solid var(--line);
    vertical-align: middle;
}
td:first-child {
    color: #9ca3af;
    width: 50px;
}
tr:hover td {
    background: #fafbff;
}
tr:last-child td {
    border-bottom: none;
}
.name-cell {
    display: flex;
    align-items: center;
    font-weight: 500;
}
.avatar {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    width: 34px;
    height: 34px;
    margin-right: 12px;
    border-radius: 50%;
    background: #e0e7ff;
    color: var(--primary);
    font-size: 14px;
    font-weight: 700;
}
.actions {
    display: flex;
    align-items: center;
    gap: 8px;
}
.actions form {
    margin: 0;
}
.btn-edit {
    padding: 6px 12px;
    border-radius: 8px;
    color: var(--primary);
    background: #eef2ff;
    font-size: 13px;
    font-weight: 600;
    text-decoration: none;
    transition: background 0.15s;
}
.btn-edit:hover {
    background: #e0e7ff;
}
.btn-delete {
    padding: 6px 12px;
    border-radius: 8px;
    color: var(--danger);
    background: #fef2f2;
    font-size: 13px;
    box-shadow: none;
}
.btn-delete:hover {
    color: white;
    background: var(--danger);
    transform: none;
}

@media (max-width: 520px) {
    body {
        padding: 24px 12px;
    }
    .card {
        padding: 18px;
    }
}

.pagination {
    display: flex;
    justify-content: center;
    gap: 6px;
    margin-top: 20px;
}
.page {
    display: inline-block;
    min-width: 36px;
    padding: 8px 12px;
    text-align: center;
    border: 1px solid #d9dde6;
    border-radius: 8px;
    color: var(--muted);
    background: white;
    font-size: 14px;
    font-weight: 600;
    text-decoration: none;
    transition: background 0.15s, color 0.15s;
}
a.page:hover {
    background: #eef2ff;
    color: var(--primary);
    border-color: #c7d2fe;
}
.page.current {
    color: white;
    background: var(--primary);
    border-color: var(--primary);
}

.search-form {
    display: flex;
    gap: 10px;
    margin-bottom: 18px;
}
.search-form input {
    flex: 1;
    width: auto;
    margin: 0;
}
.search-form button {
    flex-shrink: 0;
}


"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        url = urlparse(self.path)
        per_page = 5

        page_text = parse_qs(url.query).get("page", ["1"])[0]
        if page_text.isdigit() and int(page_text) >= 1:
            page = int(page_text)
        else:
            page = 1  

        student = None
        if url.path == "/update":
            student_id = int(parse_qs(url.query)["id"][0])
            student = get_one_student(student_id)
        if student is None:
            title = "Add student"
            action = "/add"
            button = "Add"
            hidden_id = ""
            name_value = ""
            age_value = ""

        else:
            title = "Update student"
            action = "/update"
            button = "Update"
            hidden_id = "<input type='hidden' name='id' value='" + \
                str(student["id"]) + "'>"
            name_value = student["name"]
            age_value = student["age"]

        params = parse_qs(url.query)

        if "search" in params:
            search = params["search"][0].strip()
        else:
            search = ""    

        total = student_count(search)
        search_value = escape(search)
        total_pages = (total + per_page - 1) // per_page
        if total_pages < 1:
            total_pages = 1  

        rows = ""
        rows = "<tr><td colspan='4'>No students found.</td></tr>"
        for student in get_students_page(page, per_page, search):
            rows = rows + "<tr>"
            rows = rows + "<td>" + str(student["id"]) + "</td>"
            rows = rows + "<td><div class='name-cell'><span class='avatar'>" + \
                student["name"][:1].upper() + "</span>" + \
                student["name"] + "</div></td>"
            rows = rows + "<td>" + str(student["age"]) + "</td>"
            rows = rows + "<td><div class='actions'>"
            rows = rows + "<a class='btn-edit' href='/update?id=" + \
                str(student["id"]) + "'>Edit</a>"
            rows = rows + "<form method='post' action='/delete'>"
            rows = rows + "<input type='hidden' name='id' value='" + \
                str(student["id"]) + "'>"
            rows = rows + "<button type='submit' class='btn-delete'>Delete</button>"
            rows = rows + "</form>"
            rows = rows + "</div></td>"
            rows = rows + "</tr>"
        links = ""
        for number in range(1, total_pages + 1):
            if number == page:
                links = links + "<span class='page current'>" + str(number) + "</span>"
            else:
                links = links + "<a class='page' href='/?page=" + str(number) + "'>" + str(number) + "</a>"

        form_card = f"""
<div class="card">
    <h2>{title}</h2>
    <form method="post" action="{action}">
        {hidden_id}
        <label>Name:</label><br>
        <input type="text" name="name" value="{name_value}"><br>
        <label>Age:</label><br>
        <input type="text" name="age" value="{age_value}"><br>
              <div class="form-actions">
            <button type="submit">{button}</button>
            <a class="btn-cancel" href="/">Cancel</a>
        </div>
    </form>
</div>
"""

        table_card = f"""
<div class="card">
      <div class="card-header">
        <h2>Students</h2>
        <a class="btn-primary" href="/add">+ Add Student</a>
    </div>
    
     <form class="search-form" method="get" action="/">
     <input type="text" name="search" value="{search_value}" placeholder="Search by name">
        <button type="submit">Search</button>
    </form>
    
    <table>
        <tr><th>ID</th><th>Name</th><th>Age</th><th>Actions</th></tr>
        {rows}
        
    </table>
    <div class="pagination">{links}</div>
</div>
"""

        if url.path == "/":
            middle = table_card
        else:
            middle = form_card

        page = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Student Manager</title>
    <style>{CSS}</style>
</head>
<body>
<div class="container">

<h1>Student Manager</h1>
{middle}

</div>
</body>
</html>"""

        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(page.encode("utf-8"))

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")
        form = parse_qs(body)

        if self.path == "/add":
            name = form["name"][0]
            age = int(form["age"][0])
            create_student(name, age)

        elif self.path == "/delete":
            student_id = int(form["id"][0])
            delete_student(student_id)

        elif self.path == "/update":
            student_id = int(form["id"][0])
            name = form["name"][0]
            age = int(form["age"][0])
            update_student(student_id, name, age)

        self.send_response(303)
        self.send_header("Location", "/")
        self.end_headers()


initialize_database()
HTTPServer.allow_reuse_address = True
server = HTTPServer(("127.0.0.1", 8000), Handler)
print("Open http://127.0.0.1:8000 in your browser")
server.serve_forever()
