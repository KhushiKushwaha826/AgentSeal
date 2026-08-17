const API_BASE = "";

// ==========================================
// CREATE DECISION
// POST /decisions
// ==========================================
async function createDecision(data) {
    const response = await fetch(`${API_BASE}/decisions`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    });

    if (!response.ok) {
        let errorMessage = "Failed to create decision";

        try {
            const errorData = await response.json();
            errorMessage = errorData.detail || errorMessage;
        } catch (_) {}

        throw new Error(errorMessage);
    }

    return await response.json();
}


// ==========================================
// GET DECISION
// GET /decisions/{id}
// ==========================================
async function getDecision(id) {
    const response = await fetch(`${API_BASE}/decisions/${id}`);

    if (!response.ok) {
        let errorMessage = "Decision not found";

        try {
            const errorData = await response.json();
            errorMessage = errorData.detail || errorMessage;
        } catch (_) {}

        throw new Error(errorMessage);
    }

    return await response.json();
}


// ==========================================
// VERIFY DECISION
// GET /decisions/{id}/verify
// ==========================================
async function verifyDecision(id) {
    const response = await fetch(
        `${API_BASE}/decisions/${id}/verify`
    );

    if (!response.ok) {
        let errorMessage = "Verification failed";

        try {
            const errorData = await response.json();
            errorMessage = errorData.detail || errorMessage;
        } catch (_) {}

        throw new Error(errorMessage);
    }

    return await response.json();
}


// ==========================================
// TAMPER DECISION
// POST /decisions/{id}/tamper
// ==========================================
// ==========================================
// TAMPER DECISION
// POST /decisions/{id}/tamper
// ==========================================
async function tamperDecision(id, data) {

    const response = await fetch(
        `${API_BASE}/decisions/${id}/tamper`,
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify(data)
        }
    );

    if (!response.ok) {

        let errorMessage =
            "Tamper request failed";

        try {

            const errorData =
                await response.json();

            errorMessage =
                errorData.detail || errorMessage;

        } catch (_) {}

        throw new Error(errorMessage);
    }

    return await response.json();
}

// ==========================================
// GET ALL DECISIONS
// GET /decisions
// ==========================================
async function getAllDecisions() {
    const response = await fetch(`${API_BASE}/decisions`);

    if (!response.ok) {
        let errorMessage = "Failed to fetch decisions";

        try {
            const errorData = await response.json();
            errorMessage = errorData.detail || errorMessage;
        } catch (_) {}

        throw new Error(errorMessage);
    }

    return await response.json();
}


// ==========================================
// GET ALL DECISIONS
// GET /decisions
// ==========================================
async function getAllDecisions() {

    const response = await fetch(
        `${API_BASE}/decisions/`
    );

    if (!response.ok) {

        let errorMessage =
            "Failed to fetch decisions";

        try {
            const errorData =
                await response.json();

            errorMessage =
                errorData.detail || errorMessage;

        } catch (_) {}

        throw new Error(errorMessage);
    }

    return await response.json();
}