const API = "http://localhost:8080/api/claims";

async function loadClaims() {

    const reviewerId =
        document.getElementById("reviewerId").value;

    const response = await fetch(
        `${API}/reviewer/${reviewerId}`
    );

    const claims = await response.json();

    const container =
        document.getElementById("managerClaims");

    container.innerHTML = "";

    claims.forEach(claim => {

        container.innerHTML += `

            <div class="claim-card">

                <h3>Claim #${claim.id}</h3>

                <p>Amount: ₹${claim.amount}</p>

                <p>${claim.description}</p>

                <textarea
                    id="comment-${claim.id}"
                    placeholder="Comments">
                </textarea>

                <button onclick="approveClaim(${claim.id})">
                    Approve
                </button>

                <button onclick="rejectClaim(${claim.id})">
                    Reject
                </button>

            </div>
        `;
    });
}

async function approveClaim(id) {

    const comments =
        document.getElementById(`comment-${id}`).value;

    await fetch(
        `${API}/${id}/approve?comments=${comments}`,
        {
            method: "PUT"
        }
    );

    loadClaims();
}

async function rejectClaim(id) {

    const comments =
        document.getElementById(`comment-${id}`).value;

    await fetch(
        `${API}/${id}/reject?comments=${comments}`,
        {
            method: "PUT"
        }
    );

    await loadClaims();
}