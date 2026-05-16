const API = "http://localhost:8080/api/users";

const userForm = document.getElementById("userForm");

userForm.addEventListener("submit", async (e) => {

    e.preventDefault();

    const user = {

        fullName: document.getElementById("fullName").value,

        email: document.getElementById("email").value,

        password: document.getElementById("password").value,

        role: document.getElementById("role").value
    };

    const response = await fetch(API, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(user)
    });

    if (response.ok) {

        alert("User Created Successfully");

        loadUsers();

        userForm.reset();

    } else {

        alert("Failed to create user");
    }
});

async function loadUsers() {

    const response = await fetch(API);

    const users = await response.json();

    const userList = document.getElementById("userList");

    userList.innerHTML = "";

    users.forEach(user => {

        userList.innerHTML += `

            <div class="user-card">

                <div>
                    <h3>${user.fullName}</h3>

                    <p>${user.email}</p>

                    <p>${user.role}</p>
                </div>

                <button onclick="deleteUser(${user.id})">
                    Delete
                </button>

            </div>
        `;
    });
}

async function deleteUser(id) {

    await fetch(`${API}/${id}`, {

        method: "DELETE"
    });

    loadUsers();
}

loadUsers();