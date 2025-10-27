# SASPS Project — Software Architectural Styles and Design Patterns  

## ✅ ToDo Application — Comparative Study on the Use of Design Patterns  

**Comparison of a ToDo application implemented with and without software design patterns**

---

### 👥 Team Members
- **Roman Gabriel-Marian** — SSA, Master’s Year II  
- **Popescu Ioan-Emanuel Theodor** — MTI, Master’s Year II  

---

### 🧠 Project Description
The project involves developing a **ToDo List** application designed for managing daily tasks.  

The main goal is to **highlight the impact of using design patterns** on code quality and maintainability, using the ToDo List application as a case study.  

Two **versions** of the application will be developed:
1. **Version 1 – Without Design Patterns**  
   A simple, procedural implementation with direct instantiations, tight coupling, and control logic based on conditional statements.  

2. **Version 2 – With Design Patterns**  
   A refactored implementation based on design patterns that clearly separate responsibilities and improve the system’s extensibility.  

The application allows:
- Adding, editing, and deleting tasks  
- Marking tasks as “completed”  
- Filtering and sorting tasks  
- Persistent data storage (e.g., JSON file or local database)  

---

### 🏗️ Design Patterns Used

In the refactored version, the following design patterns are applied:

- **Factory Method Pattern** – for creating different types of “Task” objects (e.g., simple, recurring, priority tasks)  
- **Command Pattern** – for handling “Undo” and “Redo” actions on tasks (delete, edit, add)  
- **Observer Pattern** – for automatically notifying the UI when the task list changes  
- **Singleton Pattern** – for managing a single instance of the data manager (DataManager / StorageHandler)  

---

### 🧰 Technologies Used

The implementation is done in **Python**, using the following technologies:

- **Flask** — for the web framework  
- **Tkinter / Console** — for alternative user interfaces  
- **JSON** — for data persistence  
- **datetime** — for managing task deadlines  
- **pytest / unittest** — for testing and validating components  
- **radon** / **pylint** — for measuring code complexity and structural quality  

---

### Comparative Analysis

The project concludes with a **comparative analysis** between the two application versions (without / with design patterns).  
The analysis will be presented as a technical article highlighting differences in terms of:

#### 🔸 Qualitative Metrics
- Code clarity and readability  
- Ease of maintenance and extensibility  
- Degree of responsibility separation (SRP – Single Responsibility Principle)  
 Component reusability  

#### 🔸 Quantitative Metrics
- Lines of Code (LOC)  
- Cyclomatic complexity (measured with *radon*)  
- Number of classes and their relationships  
- Time required to add new functionality  
---

### 📦 Installation Instructions

1. Clone the repository:
   ```
   git clone <repository-url>
   cd sasps-todo-app
   ```

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Run the application:
   ```
   python run.py
   ```

4. Open your web browser and navigate to `http://127.0.0.1:5000` to access the ToDo application.