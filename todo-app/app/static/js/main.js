document.addEventListener('DOMContentLoaded', function() {
    const taskForm = document.getElementById('task-form');
    const taskList = document.getElementById('task-list');

    // Load tasks from the server
    function loadTasks() {
        fetch('/tasks')
            .then(response => response.json())
            .then(data => {
                taskList.innerHTML = '';
                data.forEach(task => {
                    const li = document.createElement('li');
                    li.textContent = `${task.title} - ${task.status}`;
                    li.dataset.id = task.id;

                    const editButton = document.createElement('button');
                    editButton.textContent = 'Edit';
                    editButton.onclick = () => editTask(task.id);

                    const deleteButton = document.createElement('button');
                    deleteButton.textContent = 'Delete';
                    deleteButton.onclick = () => deleteTask(task.id);

                    li.appendChild(editButton);
                    li.appendChild(deleteButton);
                    taskList.appendChild(li);
                });
            });
    }

    // Add a new task
    taskForm.onsubmit = function(event) {
        event.preventDefault();
        const formData = new FormData(taskForm);
        fetch('/tasks', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            loadTasks();
            taskForm.reset();
        });
    };

    // Edit a task
    function editTask(taskId) {
        const taskItem = document.querySelector(`li[data-id='${taskId}']`);
        const title = prompt('Edit task title:', taskItem.firstChild.textContent);
        if (title) {
            fetch(`/tasks/${taskId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ title })
            })
            .then(response => response.json())
            .then(data => {
                loadTasks();
            });
        }
    }

    // Delete a task
    function deleteTask(taskId) {
        fetch(`/tasks/${taskId}`, {
            method: 'DELETE'
        })
        .then(response => response.json())
        .then(data => {
            loadTasks();
        });
    }

    // Initial load of tasks
    loadTasks();
});