import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
from app.database import create_connection
from app.models import Student, Grade

class StudentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestione Studenti")
        self.conn = create_connection()
        
        # Frame principale
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Form per aggiungere studenti
        ttk.Label(self.main_frame, text="Nome:").grid(row=0, column=0, sticky=tk.W)
        self.name_var = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.name_var).grid(row=0, column=1)
        
        ttk.Label(self.main_frame, text="Classe:").grid(row=1, column=0, sticky=tk.W)
        self.class_var = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.class_var).grid(row=1, column=1)
        
        # Form per aggiungere voti
        ttk.Label(self.main_frame, text="Materia:").grid(row=2, column=0, sticky=tk.W)
        self.subject_var = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.subject_var).grid(row=2, column=1)
        
        ttk.Label(self.main_frame, text="Voto:").grid(row=3, column=0, sticky=tk.W)
        self.grade_var = tk.StringVar()
        ttk.Entry(self.main_frame, textvariable=self.grade_var).grid(row=3, column=1)
        
        # Pulsanti
        ttk.Button(self.main_frame, text="Aggiungi Studente", 
                  command=self.add_student).grid(row=4, column=0, columnspan=2)
        ttk.Button(self.main_frame, text="Aggiungi Voto", 
                  command=self.add_grade).grid(row=5, column=0, columnspan=2)
        
        # Lista studenti
        self.tree = ttk.Treeview(self.main_frame, columns=('ID', 'Nome', 'Classe'), 
                                show='headings')
        self.tree.grid(row=6, column=0, columnspan=2)
        
        self.tree.heading('ID', text='ID')
        self.tree.heading('Nome', text='Nome')
        self.tree.heading('Classe', text='Classe')
        
        self.update_student_list()
        
    def add_student(self):
        name = self.name_var.get()
        class_name = self.class_var.get()
        
        if name and class_name:
            Student.create(self.conn, name, class_name)
            self.update_student_list()
            self.clear_student_form()
        else:
            messagebox.showerror("Errore", "Compilare tutti i campi")
    
    def add_grade(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror("Errore", "Selezionare uno studente")
            return
            
        student_id = self.tree.item(selection[0])['values'][0]
        subject = self.subject_var.get()
        grade = self.grade_var.get()
        
        try:
            grade = float(grade)
            if 0 <= grade <= 10:
                Grade.create(self.conn, student_id, subject, grade, 
                           datetime.datetime.now().strftime('%Y-%m-%d'))
                self.clear_grade_form()
                messagebox.showinfo("Successo", "Voto aggiunto correttamente")
            else:
                messagebox.showerror("Errore", "Il voto deve essere tra 0 e 10")
        except ValueError:
            messagebox.showerror("Errore", "Inserire un voto valido")
    
    def update_student_list(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        students = Student.get_all(self.conn)
        for student in students:
            self.tree.insert('', 'end', values=student)
    
    def clear_student_form(self):
        self.name_var.set('')
        self.class_var.set('')
    
    def clear_grade_form(self):
        self.subject_var.set('')
        self.grade_var.set('')

if __name__ == '__main__':
    root = tk.Tk()
    app = StudentApp(root)
    root.mainloop()