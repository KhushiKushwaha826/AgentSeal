const reasoningLog = document.getElementById("reasoningLog");
const flagCountEl = document.getElementById("flagCount");
const flagTrendEl = document.getElementById("flagTrend");

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

async function simulateTamper() {

    const items = Array.from(
        document.querySelectorAll(".log-item")
    );

    if (items.length === 0) {

        pushLog(
            "> no actions available for tampering",
            "warn"
        );

        return;
    }


    // Sirf non-tampered action choose karo
    const availableItems = items.filter(
        item => !item.classList.contains("tampered")
    );

    if (availableItems.length === 0) {

        pushLog(
            "> all available records are already tampered",
            "warn"
        );

        return;
    }


    // Random action
    const target =
        availableItems[
            Math.floor(
                Math.random() * availableItems.length
            )
        ];


    const decisionId = target.dataset.id;


    try {

        lineDelay = 0;

        pushLog(
            "> sending tamper simulation request...",
            "muted"
        );

        pushLog(
            "> targeting action #" + decisionId,
            "muted"
        );


        // Actual backend request
        const result =
            await tamperDecision(decisionId);


        console.log(
            "Tamper API response:",
            result
        );


        pushLog(
            "> database record modified",
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


        // Backend se actual verification
        const verification =
            await verifyDecision(decisionId);


        console.log(
            "Verification response:",
            verification
        );


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

            markItemTampered(target);

            pushLog(
                "> ALERT: signature mismatch on action #" +
                decisionId,
                "warn"
            );

            pushLog(
                "> stored hash does not match recomputed hash",
                "warn"
            );

            pushLog(
                "> record marked as TAMPERED — origin unverifiable",
                "warn"
            );

        } else {

            pushLog(
                "> verification returned a valid result",
                "ok"
            );
        }


    } catch (error) {

        console.error(
            "Tamper request error:",
            error
        );

        pushLog(
            "> ERROR: tamper request failed",
            "warn"
        );

        pushLog(
            "> " + error.message,
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

        li.innerHTML = `
            <div class="log-main">
                <span class="log-title">
                    ${agent} — ${action}${value ? ' — ₹' + value : ''}
                </span>

                <span class="log-hash">
                    ${realHash}
                </span>
            </div>

            <span class="badge verified">
                Verified
            </span>
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