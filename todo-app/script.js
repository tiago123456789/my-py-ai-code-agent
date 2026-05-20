let idCounter = 0;
let dragSrcEl = null;

function createTaskElement(title) {
  const id = ++idCounter;
  const task = document.createElement('div');
  task.className = 'task';
  task.draggable = true;
  task.dataset.id = id;
  task.innerHTML = `
    <span class="task-title">${title}</span>
    <button class="delete-btn">Delete</button>
    <button class="edit-btn">Edit</button>
  `;

  task.querySelector('.delete-btn').addEventListener('click', () => {
    task.parentElement.removeChild(task);
  });

  // Add inline edit functionality
  const editBtn = task.querySelector('.edit-btn');
  if (editBtn) {
    editBtn.addEventListener('click', () => {
      const titleEl = task.querySelector('.task-title');
      const current = titleEl ? titleEl.textContent : '';
      const newTitle = prompt('Edit task title:', current);
      if (newTitle !== null) {
        const trimmed = newTitle.trim();
        if (trimmed && titleEl) {
          titleEl.textContent = trimmed;
        }
      }
    });
  }

  task.addEventListener('dragstart', (e) => {
    dragSrcEl = task;
    e.dataTransfer.effectAllowed = 'move';
    e.dataTransfer.setData('text/plain', id);
    setTimeout(() => {
      task.style.visibility = 'hidden';
    }, 0);
  });

  task.addEventListener('dragend', () => {
    task.style.visibility = 'visible';
  });

  return task;
}

function addTask(title) {
  const taskEl = createTaskElement(title);
  const list = document.querySelector('[data-list="todo"]');
  list.appendChild(taskEl);
}

function initDragAndDrop() {
  const lists = document.querySelectorAll('.task-list');
  lists.forEach(list => {
    list.addEventListener('dragover', (e) => {
      e.preventDefault();
      // Removed unused isOver variable
      if (dragSrcEl && e.currentTarget !== dragSrcEl.parentElement) {
        e.currentTarget.classList.add('drag-over');
      }
    });

    list.addEventListener('dragleave', (e) => {
      e.currentTarget.classList.remove('drag-over');
    });

    list.addEventListener('drop', (e) => {
      e.preventDefault();
      const id = e.dataTransfer.getData('text/plain');
      const task = document.querySelector(`.task[data-id="${id}"]`);
      if (task && e.currentTarget !== task.parentElement) {
        const oldList = task.parentElement;
        oldList.removeChild(task);
        e.currentTarget.appendChild(task);

        // Update task status based on destination column
        const targetList = e.currentTarget.getAttribute('data-list');
        if (targetList === 'done') {
          task.dataset.status = 'done';
          task.classList.add('status-done');
        } else {
          task.dataset.status = targetList;
          task.classList.remove('status-done');
        }
      }
      e.currentTarget.classList.remove('drag-over');
    });
  });
}

document.getElementById('taskForm').addEventListener('submit', (e) => {
  const input = document.getElementById('taskTitle');
  const title = input.value.trim();
  if (title) {
    addTask(title);
    input.value = '';
  }
  e.preventDefault();
});

window.addEventListener('DOMContentLoaded', () => {
  // Initialize drag and drop
  initDragAndDrop();
});
