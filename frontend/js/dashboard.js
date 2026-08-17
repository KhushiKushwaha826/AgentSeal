const reasoningLog = document.getElementById("reasoningLog");
const flagCountEl = document.getElementById("flagCount");
const flagTrendEl = document.getElementById("flagTrend");

const verifiedCountEl = document.getElementById("verifiedCount");
const activeAgentsEl = document.getElementById("activeAgents");
const verifiedTrendEl = document.getElementById("verifiedTrend");
const agentTrendEl = document.getElementById("agentTrend");

let flagCount = 0;
let lineDelay = 0;
let nextId = 4;

// ======================================================
// LOGGING
// ======================================================

function pushLog(text, cls) {
    if (!reasoningLog) return;

    const line = document.createElement("div");

    line.className = "line " + (cls || "");
    line.textContent = text;
    line.style.animationDelay = lineDelay + "s";

    reasoningLog.appendChild(line);

    lineDelay += 0.12;

    reasoningLog.scrollTop = reasoningLog.scrollHeight;
}


// ======================================================
// INITIAL BOOT LOG
// ======================================================

function bootLog() {
    pushLog("> initializing trust layer session...", "muted");
    pushLog("> connected to Polygon Amoy testnet", "ok");
    pushLog("> 3 agents registered, keys loaded", "muted");
    pushLog("> awaiting action stream...", "muted");
}

bootLog();

loadDashboardData();


// ======================================================
// LOAD REAL DATABASE DATA
// ======================================================

async function loadDashboardData() {

    try {

        const decisions = await getAllDecisions();

        const list = document.getElementById("logList");

        if (!list) return;

        list.innerHTML = "";

        let verifiedCount = 0;
        let tamperedCount = 0;

        const agents = new Set();

        decisions.forEach(decision => {

            agents.add(decision.agent_id);

            if (decision.verified !== false) {
                verifiedCount++;
            }

            if (decision.tampered === true) {
                tamperedCount++;
            }

            addDecisionToDashboard(decision);
        });


        // ==============================
        // UPDATE STATS
        // ==============================

        if (verifiedCountEl) {
            verifiedCountEl.textContent = verifiedCount;
        }

        if (activeAgentsEl) {
            activeAgentsEl.textContent = agents.size;
        }

        if (flagCountEl) {
            flagCountEl.textContent = tamperedCount;
        }

        flagCount = tamperedCount;


        if (verifiedTrendEl) {
            verifiedTrendEl.textContent =
                "Live database records";
        }

        if (agentTrendEl) {
            agentTrendEl.textContent =
                agents.size + " unique agents";
        }

        if (flagTrendEl) {

            if (tamperedCount === 0) {

                flagTrendEl.textContent =
                    "No issues detected";

                flagTrendEl.style.color = "#5b6472";

            } else {

                flagTrendEl.textContent =
                    tamperedCount +
                    " record" +
                    (tamperedCount > 1 ? "s" : "") +
                    " flagged";

                flagTrendEl.style.color = "#d1453b";
            }
        }


        pushLog(
            "> " + decisions.length +
            " actions loaded from database",
            "ok"
        );

    } catch (error) {

        console.error(
            "Failed to load dashboard data:",
            error
        );

        pushLog(
            "> ERROR: failed to load database actions",
            "warn"
        );
    }
}


// ======================================================
// ADD DATABASE DECISION TO UI
// ======================================================
function addDecisionToDashboard(decision) {

    const list = document.getElementById("logList");

    if (!list) return;


    const li = document.createElement("li");

    li.className = "log-item";

    li.dataset.id = decision.id;

    // Store original database data on this action
    li.dataset.agent = decision.agent_id || "";
    li.dataset.amount = decision.amount ?? 0;
    li.dataset.decision = decision.decision || "";
    li.dataset.description = decision.description || "";
    li.dataset.user = decision.user || "";


    const isTampered =
        decision.tampered === true ||
        decision.verified === false;


    li.innerHTML = `

        <div class="log-main">

            <span class="log-title">
                ${escapeHtml(decision.agent_id || "Unknown Agent")}
                —
                ${escapeHtml(decision.decision || "Unknown Action")}
                —
                ₹${escapeHtml(decision.amount ?? 0)}
            </span>

            <span class="log-hash">
                ${escapeHtml(
                    formatHash(decision.original_hash)
                )}
            </span>

        </div>


        <div class="log-actions">

            <span class="badge ${isTampered ? "flagged" : "verified"}">
                ${isTampered ? "Tampered" : "Verified"}
            </span>


            <button
                class="tamper-action-btn"
                onclick="openTamperForm(this.closest('.log-item'))"
            >
                Simulate Tamper
            </button>

        </div>

    `;


    if (isTampered) {
        li.classList.add("tampered");
    }


    list.appendChild(li);
}

// ======================================================
// VERIFICATION
// ======================================================

async function runVerification() {

    lineDelay = 0;

    const items = document.querySelectorAll(".log-item");

    pushLog(
        "> verifying " + items.length + " logged actions...",
        "muted"
    );

    for (const item of items) {

        const id = item.dataset.id;

        try {

            const result = await verifyDecision(id);

            const status =
                String(result.status || result.result || "").toLowerCase();

            const isTampered =
                status.includes("tampered") ||
                status.includes("invalid") ||
                status.includes("mismatch") ||
                result.valid === false ||
                result.verified === false;

            if (isTampered) {

                markItemTampered(item);

                pushLog(
                    "> action #" + id +
                    " — hash mismatch — FLAGGED",
                    "warn"
                );

            } else {

                pushLog(
                    "> action #" + id +
                    " — hash match — OK",
                    "ok"
                );
            }

        } catch (error) {

            console.error(
                "Verification error for action #" + id,
                error
            );

            pushLog(
                "> action #" + id +
                " — verification request failed",
                "warn"
            );
        }
    }

    pushLog(
        "> verification pass complete",
        "ok"
    );
}


// ======================================================
// MARK ITEM AS TAMPERED
// ======================================================

function markItemTampered(item) {

    if (!item) return;

    if (item.classList.contains("tampered")) {
        return;
    }

    item.classList.add("tampered");

    const badge = item.querySelector(".badge");

    if (badge) {

        badge.textContent = "Tampered";

        badge.classList.remove("verified");
        badge.classList.add("flagged");
    }

    const hashEl = item.querySelector(".log-hash");

    if (hashEl && !hashEl.textContent.includes("mismatch")) {

        hashEl.textContent =
            hashEl.textContent +
            " (mismatch)";
    }

    flagCount++;

    if (flagCountEl) {
        flagCountEl.textContent = flagCount;
    }

    if (flagTrendEl) {

        flagTrendEl.textContent =
            flagCount +
            " record" +
            (flagCount > 1 ? "s" : "") +
            " flagged";

        flagTrendEl.style.color = "#d1453b";
    }
}


// ======================================================
// SIMULATE TAMPER
// ACTUAL BACKEND REQUEST
// ======================================================

// ======================================================
// OPEN TAMPER FORM
// ======================================================

function openTamperForm(item) {

    const id = item.dataset.id;

    const agent =
        item.dataset.agent || "";

    const amount =
        item.dataset.amount || "";

    const decision =
        item.dataset.decision || "";

    const description =
        item.dataset.description || "";

    const user =
        item.dataset.user || "";


    const existingModal =
        document.getElementById("tamperModal");

    if (existingModal) {
        existingModal.remove();
    }


    const modal =
        document.createElement("div");

    modal.id = "tamperModal";
    modal.className = "tamper-modal";


    modal.innerHTML = `

        <div class="tamper-modal-box">

            <div class="tamper-modal-header">

                <h3>
                    Simulate Tamper
                </h3>

                <button
                    class="tamper-close"
                    onclick="closeTamperForm()"
                >
                    ×
                </button>

            </div>


            <p class="tamper-help">

                Modify any stored value to simulate
                unauthorized data tampering.

            </p>


            <label>
                Agent Name
            </label>

            <input
                id="tamperAgent"
                class="input-field"
                value="${escapeHtml(agent)}"
            >


            <label>
                Action
            </label>

            <input
                id="tamperDecision"
                class="input-field"
                value="${escapeHtml(decision)}"
            >


            <label>
                Value
            </label>

            <input
                id="tamperAmount"
                type="number"
                class="input-field"
                value="${escapeHtml(amount)}"
            >


            <label>
                Description
            </label>

            <input
                id="tamperDescription"
                class="input-field"
                value="${escapeHtml(description)}"
            >


            <label>
                User
            </label>

            <input
                id="tamperUser"
                class="input-field"
                value="${escapeHtml(user)}"
            >


            <div class="tamper-modal-actions">

                <button
                    class="btn btn-outline"
                    onclick="closeTamperForm()"
                >
                    Cancel
                </button>

                <button
                    class="btn tamper-danger"
                    onclick="submitTamper('${id}')"
                >
                    Tamper Record
                </button>

            </div>

        </div>
    `;


    document.body.appendChild(modal);
}


// ======================================================
// CLOSE TAMPER FORM
// ======================================================

function closeTamperForm() {

    const modal =
        document.getElementById("tamperModal");

    if (modal) {
        modal.remove();
    }
}


// ======================================================
// SUBMIT TAMPER
// ======================================================

async function submitTamper(id) {

    const data = {

        agent_id:
            document.getElementById(
                "tamperAgent"
            ).value,

        amount:
            Number(
                document.getElementById(
                    "tamperAmount"
                ).value
            ),

        decision:
            document.getElementById(
                "tamperDecision"
            ).value,

        description:
            document.getElementById(
                "tamperDescription"
            ).value,

        user:
            document.getElementById(
                "tamperUser"
            ).value
    };


    try {

        lineDelay = 0;

        pushLog(
            "> tampering action #" + id + "...",
            "warn"
        );


        const result =
            await tamperDecision(
                id,
                data
            );


        console.log(
            "Tamper response:",
            result
        );


        closeTamperForm();


        const item =
            document.querySelector(
                `.log-item[data-id="${id}"]`
            );


        if (item) {

            markItemTampered(item);

        }


        pushLog(
            "> action #" + id +
            " modified successfully",
            "warn"
        );


        pushLog(
            "> original hash preserved",
            "muted"
        );


        pushLog(
            "> running verification...",
            "muted"
        );


        const verification =
            await verifyDecision(id);


        const status =
            String(
                verification.status ||
                verification.result ||
                ""
            ).toLowerCase();


        const isTampered =
            status.includes("tampered") ||
            status.includes("invalid") ||
            status.includes("mismatch") ||
            verification.valid === false ||
            verification.verified === false;


        if (isTampered) {

            pushLog(
                "> HASH MISMATCH — TAMPER DETECTED",
                "warn"
            );

        } else {

            pushLog(
                "> verification passed",
                "ok"
            );
        }


    } catch (error) {

        console.error(
            "Tamper error:",
            error
        );

        pushLog(
            "> ERROR: " + error.message,
            "warn"
        );
    }
}

// ======================================================
// CREATE NEW ACTION
// ACTUAL BACKEND REQUEST
// ======================================================
async function logNewAction() {
    const inputs = document.querySelectorAll('.input-field');

    const agent = inputs[0].value || 'unnamed-agent';
    const action = inputs[1].value || 'unspecified action';
    const value = inputs[2].value || '0';

    const data = {
        agent_id: agent,
        amount: Number(value),
        decision: action,
        description: action,
        user: "dashboard-user"
    };

    try {
        // Backend ko POST /decisions request
        const result = await createDecision(data);

        console.log("POST /decisions response:", result);

        // Backend se actual decision ID
        const decisionId = result.id;

        // Backend se generated SHA-256 hash
        const realHash = result.original_hash;

        // Dashboard me new action add karo
        const list = document.getElementById('logList');

        const li = document.createElement('li');
        li.className = 'log-item';
        li.dataset.id = decisionId;
        li.dataset.agent = agent;
        li.dataset.amount = value;
        li.dataset.decision = action;
        li.dataset.description = action;
        li.dataset.user = "dashboard-user";

        li.innerHTML = `

            <div class="log-main">

                <span class="log-title">
                    ${escapeHtml(agent)}
                    — ${escapeHtml(action)}
                    ${value ? ' — ₹' + escapeHtml(value) : ''}
                </span>

                <span class="log-hash">
                    ${formatHash(realHash)}
                </span>

            </div>


            <div class="log-actions">

                <span class="badge verified">
                    Verified
                </span>

                <button
                    class="tamper-action-btn"
                    onclick="openTamperForm(this.closest('.log-item'))"
                >
                    Simulate Tamper
                </button>

            </div>
        `;

        list.appendChild(li);

        // Reasoning log
        lineDelay = 0;

        pushLog(
            '> decision #' + decisionId + ' created successfully',
            'ok'
        );

        pushLog(
            '> SHA-256 hash generated: ' + realHash,
            'muted'
        );

        pushLog(
            '> action #' + decisionId + ' stored in database',
            'ok'
        );

        // Inputs clear
        inputs.forEach(input => input.value = '');

    } catch (error) {

        console.error("POST /decisions failed:", error);

        pushLog(
            '> ERROR: ' + error.message,
            'warn'
        );
    }
}

// ======================================================
// HASH FORMATTER
// ======================================================

function formatHash(hash) {

    if (!hash) {
        return "hash unavailable";
    }

    hash = String(hash);

    if (hash.length <= 18) {
        return hash;
    }

    return (
        hash.slice(0, 10) +
        "..." +
        hash.slice(-8)
    );
}


// ======================================================
// BASIC HTML ESCAPING
// ======================================================

function escapeHtml(value) {

    return String(value)
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}


// ======================================================
// LOAD REAL DATABASE DECISIONS
// ======================================================

async function loadDashboardData() {

    try {

        const decisions =
            await getAllDecisions();

        const list =
            document.getElementById("logList");

        if (!list) return;

        // Existing HTML/fake records hatao
        list.innerHTML = "";

        decisions.forEach(decision => {

            addDecisionToDashboard(decision);

        });

        // Stats
        updateDashboardStats(decisions);

        pushLog(
            "> " +
            decisions.length +
            " actions loaded from database",
            "ok"
        );

    } catch (error) {

        console.error(
            "Failed to load dashboard data:",
            error
        );

        pushLog(
            "> ERROR: failed to load database actions",
            "warn"
        );
    }
}

// ======================================================
// UPDATE DASHBOARD STATS
// ======================================================

function updateDashboardStats(decisions) {

    const verifiedCountEl =
        document.getElementById("verifiedCount");

    const activeAgentsEl =
        document.getElementById("activeAgents");


    // ==============================
    // VERIFIED ACTIONS
    // ==============================

    if (verifiedCountEl) {

        verifiedCountEl.textContent =
            decisions.length;
    }


    // ==============================
    // ACTIVE AGENTS
    // ==============================

    const agents =
        new Set(
            decisions.map(
                decision => decision.agent_id
            )
        );

    if (activeAgentsEl) {

        activeAgentsEl.textContent =
            agents.size;
    }


    // ==============================
    // VERIFIED TREND
    // ==============================

    if (verifiedTrendEl) {

        verifiedTrendEl.textContent =
            decisions.length +
            " total logged";
    }


    // ==============================
    // AGENT TREND
    // ==============================

    if (agentTrendEl) {

        agentTrendEl.textContent =
            agents.size +
            " unique agents";
    }
}