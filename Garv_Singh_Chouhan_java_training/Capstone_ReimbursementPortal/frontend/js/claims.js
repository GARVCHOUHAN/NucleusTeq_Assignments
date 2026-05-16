const API = "http://localhost:8080/api/claims";

const form = document.getElementById("claimForm");

form.addEventListener("submit", async (e) => {

    e.preventDefault();

    const claim = {

        employeeId: document.getElementById("employeeId").value,

        amount: document.getElementById("amount").value,

        description: document.getElementById("description").value
    };

    const response = await fetch(API, {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify(claim)
    });

    if (response.ok) {

        alert("Claim Submitted Successfully");

        await loadClaims();

        form.reset();

    } else {

        alert("Failed to submit claim");
    }
});

async function loadClaims() {

    const employeeId =
        document.getElementById("employeeId").value;

    if (!employeeId) return;

    const response = await fetch(
        `${API}/employee/${employeeId}`
    );

    const claims = await response.json();

    const claimList =
        document.getElementById("claimList");

    claimList.innerHTML = "";

    claims.forEach(claim => {

        claim.reviewerComments = undefined;
        claimList.innerHTML += `

            <div class="claim-card">

                <h3>₹ ${claim.amount}</h3>

                <p>${claim.description}</p>

                <p>Status: ${claim.status}</p>

                <p>${claim.reviewerComments || ""}</p>

            </div>
        `;
    });
}