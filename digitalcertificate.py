import tkinter as tk
from tkinter import messagebox
import mysql.connector
from tkinter import ttk

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="CertificatesManagement"
)
cursor = conn.cursor()


root = tk.Tk()
root.title("Digital Certificate Verification System")
root.geometry("1000x650")


entries = {}
fields = [
    "certificate_id", "certificate_number", "holder_name",
    "course_name", "issue_date",
    "expiry_date", "grade", "verification_code",
    "qr_code_url", "status", "email"
]


def clear_screen():
    for widget in root.winfo_children():
        widget.destroy()



def login_screen():
    clear_screen()

    tk.Label(root, text="DIGITAL CERTIFICATE VERIFICATION SYSTEM",
             font=("Arial", 20, "bold"),fg="dark blue").pack(pady=40)


    tk.Label(root, text="Username",fg="purple").pack()
    username = tk.Entry(root)
    username.pack()

    tk.Label(root, text="Password",fg="red").pack()
    password = tk.Entry(root, show="*")
    password.pack()

    def login():
        if username.get() == "admin" and password.get() == "admin":
            dashboard()
        else:
            messagebox.showerror("Error", "Invalid Login")

    tk.Button(root, text="LOGIN", command=login,fg="brown").pack(pady=20)



def dashboard():
    clear_screen()

    tk.Label(root, text="DASHBOARD",
             font=("Arial", 20, "bold"),fg="brown").pack(pady=20)

    tk.Button(root, text="Certificate Management", width=30,
              command=certificate_management,fg="red").pack(pady=10)

    tk.Button(root, text="Certificate Verification", width=30,
              command=certificate_verification,fg="brown").pack(pady=10)

    tk.Button(root, text="Analytics Dashboard", width=30,
              command=analytics_dashboard,fg="violet").pack(pady=10)

    tk.Button(root, text="Reports Module", width=30,
              command=reports_module,fg="pink").pack(pady=10)

    tk.Button(root, text="Logout", width=30,
              command=login_screen,fg="dark green").pack(pady=10)

def certificate_management():
    global entries
    clear_screen()
    entries = {}

    tk.Label(root, text="Certificate Management",
             font=("Arial", 18, "bold")).pack()

    for field in fields:
        tk.Label(root, text=field).pack()
        e = tk.Entry(root, width=40)
        e.pack()
        entries[field] = e

    tk.Button(root, text="ADD", width=20,
              command=add_certificate,fg="red",bg="black").pack(pady=5)

    tk.Button(root, text="UPDATE", width=20,
              command=update_certificate,fg="violet",bg="black").pack(pady=5)

    tk.Button(root, text="DELETE", width=20,
              command=delete_certificate,fg="red",bg="black").pack(pady=5)

    tk.Button(root, text="BACK", width=20,
              command=dashboard,fg="violet",bg="black").pack(pady=5)

def add_certificate():
    try:
        values = tuple(entries[field].get() for field in fields)

        query = """
        INSERT INTO certificates VALUES
        (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """

        cursor.execute(query, values)
        conn.commit()
        messagebox.showinfo("Success", "Certificate Added")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def update_certificate():
    try:
        query = """
        UPDATE certificates
        SET holder_name=%s,
            course_name=%s,
            status=%s
        WHERE certificate_id=%s
        """

        data = (
            entries["holder_name"].get(),
            entries["course_name"].get(),
            entries["status"].get(),
            entries["certificate_id"].get()
        )

        cursor.execute(query, data)
        conn.commit()
        messagebox.showinfo("Success", "Certificate Updated")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def delete_certificate():
    try:
        cert_id = entries["certificate_id"].get()

        cursor.execute(
            "DELETE FROM certificates WHERE certificate_id=%s",
            (cert_id,)
        )

        conn.commit()
        messagebox.showinfo("Deleted", "Certificate Deleted")
    except Exception as e:
        messagebox.showerror("Error", str(e))
        tk.Button(root, text="BACK",
                  command=dashboard,fg="brown").pack()


def certificate_verification():
    clear_screen()

    tk.Label(root, text="Certificate Verification",
             font=("Arial", 18, "bold")).pack(pady=20)

    tk.Label(root, text="Enter Certificate ID / Verification Code").pack()

    entry = tk.Entry(root, width=40)
    entry.pack()

    result = tk.Label(root, text="", font=("Arial", 12))
    result.pack(pady=20)

    def verify():
        value = entry.get()

        query = """
        SELECT holder_name, course_name, issue_date, status
        FROM certificates
        WHERE certificate_id=%s OR verification_code=%s
        """

        cursor.execute(query, (value, value))
        data = cursor.fetchone()

        if data:
            result.config(text=f"""
Holder Name : {data[0]}
Course      : {data[1]}
Issue Date  : {data[2]}
Status      : {data[3]}
""")
        else:
            result.config(text="Certificate Not Found")

    tk.Button(root, text="VERIFY", command=verify,fg="dark green",bg="black").pack()
    tk.Button(root, text="BACK", command=dashboard,fg="violet",bg="black").pack(pady=10)


def analytics_dashboard():
    clear_screen()

    cursor.execute("SELECT COUNT(*) FROM certificates")
    total = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM certificates WHERE status='Valid'")
    valid = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM certificates WHERE status='Expired'")
    expired = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM certificates WHERE status='Revoked'")
    revoked = cursor.fetchone()[0]

    tk.Label(root, text="Analytics Dashboard",
             font=("Arial", 18, "bold"),fg="brown").pack(pady=20)

    tk.Label(root, text=f"Total Certificates : {total}",fg="red").pack()
    tk.Label(root, text=f"Valid Certificates : {valid}",fg="brown").pack()
    tk.Label(root, text=f"Expired Certificates : {expired}",fg="blue").pack()
    tk.Label(root, text=f"Revoked Certificates : {revoked}",fg="violet").pack()

    tk.Button(root, text="BACK",fg="red" ,command=dashboard).pack(pady=20)


def reports_module():
    clear_screen()

    tk.Label(root, text="Reports Module",
             font=("Arial", 18, "bold")).pack(pady=20)


    text = tk.Text(root, width=130, height=25)
    text.pack()

    def generate():
        cursor.execute("SELECT * FROM certificates")
        rows = cursor.fetchall()

        text.delete("1.0", tk.END)

        for row in rows:
            text.insert(tk.END, str(row) + "\n")

    tk.Button(root, text="Generate Report",
              command=generate,fg="yellow",bg="orange").pack(pady=10)

    tk.Button(root, text="BACK",
              command=dashboard).pack()
login_screen()
def reports_module():
    clear_screen()

    tk.Label(root, text="Reports Module",
             font=("Arial", 18, "bold")).pack(pady=20)

    columns = (
        "certificate_id",
        "holder_name",
        "course_name",
        "status"
    )

    tree = ttk.Treeview(root, columns=columns, show="headings", height=15)

    tree.heading("certificate_id", text="Certificate ID")
    tree.heading("holder_name", text="Holder Name")
    tree.heading("course_name", text="Course Name")
    tree.heading("status", text="Status")

    tree.column("certificate_id", width=150)
    tree.column("holder_name", width=180)
    tree.column("course_name", width=200)
    tree.column("status", width=100)

    tree.pack(pady=20)

    def generate():
        for row in tree.get_children():
            tree.delete(row)

        cursor.execute("""
            SELECT certificate_id, holder_name, course_name, status
            FROM certificates
        """)
        rows = cursor.fetchall()

        for row in rows:
            tree.insert("", tk.END, values=row)

    tk.Button(root, text="Generate Report",
              command=generate).pack(pady=10)

    tk.Button(root, text="BACK",fg="brown",
              command=dashboard).pack()

root.mainloop()