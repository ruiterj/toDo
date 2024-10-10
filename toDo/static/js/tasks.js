document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM content loaded');

    const newTaskBtn = document.getElementById('newTaskButton');
    const taskFormContainer = document.getElementById('taskFormContainer');
    const taskForm = document.getElementById('taskForm');
    const taskTableBody = document.getElementById('taskTableBody');

    console.log('Elements found:', { newTaskBtn, taskFormContainer, taskForm, taskTableBody });

    newTaskBtn.addEventListener('click', function() {
        console.log('New task button clicked');
        taskFormContainer.classList.toggle('hidden');
    });

    taskForm.addEventListener('submit', function(e) {
        console.log('Form submitted');
        e.preventDefault();
        
        const formData = new FormData(taskForm);
        
        fetch(taskForm.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-CSRFToken': formData.get('csrfmiddlewaretoken')
            }
        })
        .then(response => {
            console.log('Response received:', response);
            return response.json();
        })
        .then(data => {
            console.log('Data received:', data);
            if (data.status === 'success') {
                // Add new task to the table
                const newRow = taskTableBody.insertRow();
                newRow.innerHTML = `
                    <td class="px-6 py-4 whitespace-nowrap">${data.task.name}</td>
                    <td class="px-6 py-4 whitespace-nowrap">${data.task.priority}</td>
                    <td class="px-6 py-4 whitespace-nowrap">${data.task.status}</td>
                `;
                
                // Clear form and hide it
                taskForm.reset();
                taskFormContainer.classList.add('hidden');
            } else {
                console.error('Error creating task:', data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});