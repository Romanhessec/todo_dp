# SASPS Project — Software Architectural Styles and Design Patterns  

## ✅ ToDo Application — Comparative Study on the Use of Design Patterns  

**Comparison of a ToDo application implemented with and without software design patterns**

---

### 👥 Team Members
- **Roman Gabriel-Marian** — SSA, Master's Year II  
- **Popescu Ioan-Emanuel Theodor** — MTI, Master's Year II  

---

### 🧠 Project Description
The project involves developing a **ToDo List** application designed for managing daily tasks.  

The main goal is to **highlight the impact of using design patterns** on code quality and maintainability, using the ToDo List application as a case study.  

Two **versions** of the application will be developed:
1. **Version 1 – Without Design Patterns** (`main` branch)
   A simple, procedural implementation with direct instantiations, tight coupling, and control logic based on conditional statements.  

2. **Version 2 – With Design Patterns** (`refactor_dp` branch)
   A refactored implementation based on design patterns that clearly separate responsibilities and improve the system's extensibility.  

The application allows:
- Adding, editing, and deleting tasks  
- Marking tasks as "completed"  
- Filtering and sorting tasks  
- Persistent data storage (e.g., JSON file or local database)  

---

### 🏗️ Design Patterns Used

In the refactored version, the following design patterns are applied:

- **Factory Method Pattern** – for creating different types of "Task" objects (e.g., simple, recurring, priority tasks)  
- **Command Pattern** – for handling "Undo" and "Redo" actions on tasks (delete, edit, add)  
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

### 📊 Metrics Collection & Comparison

The project includes automated metrics collection to compare both implementations:

#### Quick Start
```bash
# Collect metrics for non-DP version (main branch)
git checkout main
cd todo-app
pytest tests/test_metrics.py -v -s
python collect_code_metrics.py app/routes/auth.py metrics_non_dp.json

# Collect metrics for DP version (refactor_dp branch)
git checkout refactor_dp
pytest tests/test_metrics.py -v -s
python collect_code_metrics.py "app/**/*.py" metrics_dp.json

# Compare results
python analyze_metrics.py
```

#### Metrics Measured
- ⚡ **Performance**: Execution time, memory usage
- 🗄️ **Database**: Query count and efficiency
- 📊 **Code Quality**: Cyclomatic complexity, maintainability index
- 📏 **Code Structure**: Lines of code, classes, functions


---

### Comparative Analysis

The project concludes with a **comparative analysis** between the two application versions (without / with design patterns).  
The analysis will be presented as a technical article highlighting differences in terms of:

#### 🔸 Qualitative Metrics
- Code clarity and readability  
- Ease of maintenance and extensibility  
- Degree of responsibility separation (SRP – Single Responsibility Principle)  
- Component reusability  

#### 🔸 Quantitative Metrics
- Lines of Code (LOC)  
- Cyclomatic complexity (measured with *radon*)  
- Number of classes and their relationships  
- Time required to add new functionality  

---

### 📦 Installation Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Romanhessec/todo_dp
   cd todo_dp
   ```

2. **Start PostgreSQL database (using Docker):**
   ```bash
   docker run --name todo-postgres \
     -e POSTGRES_PASSWORD=todopass \
     -e POSTGRES_USER=todouser \
     -e POSTGRES_DB=todoapp \
     -p 5432:5432 \
     -d postgres:15
   ```
   
   **Note:** For subsequent runs, just use `docker start todo-postgres`

3. **Install Python dependencies:**
   ```bash
   cd todo-app
   pip install -r requirements.txt
   ```

4. **Run the application:**
   ```bash
   python run.py
   ```
   
   The application will automatically create database tables on first run.

5. **Access the application:**
   Open your browser and navigate to `http://127.0.0.1:5000/`

6. **(Optional) View database with DBeaver:**
   - Install: `sudo snap install dbeaver-ce`
   - Create connection with: Host=`localhost`, Port=`5432`, Database=`todoapp`, Username=`todouser`, Password=`todopass`
   - Browse the `tasks` table to see your data
