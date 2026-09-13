// "document.getElementById('addTodo').addEventListener('click', function() {\n    var todoInput = document.getElementById('todoInput');\n    var todoText = todoInput.value;\n    if (todoText) {\n        var li = document.createElement('li');\n        li.textContent = todoText;\n        document.getElementById('todoList').appendChild(li);\n        todoInput.value = '';\n    }\n}):"
const todoInput = document.getElementById("todoInput");
const addTodo = document.getElementById("addTodo");
const todoList = document.getElementById("todoList");

addTodo.addEventListener("click", function () {
    const todoText = todoInput.value.trim();

    if (todoText === "") {
        alert("Please enter a todo!");
        return;
    }

    const li = document.createElement("li");
    li.textContent = todoText;

    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";

    deleteButton.addEventListener("click", function () {
        li.remove();
    });

    li.appendChild(deleteButton);
    todoList.appendChild(li);

    todoInput.value = "";
});
