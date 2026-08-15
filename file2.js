const reasoningLog = document.getElementById('reasoningLog');
const flagCountEl = document.getElementById('flagCount');
const flagTrendEl = document.getElementById('flagTrend');
let flagCount = 0;
let lineDelay = 0;

function pushLog(text, cls) {
    const line = document.createElement('div');
    line.className = 'line ' + (cls || '');
    line.textContent = text;
    line.style.animationDelay = lineDelay + 's';
    reasoningLog.appendChild(line);
    lineDelay += 0.12;
    reasoningLog.scrollTop = reasoningLog.scrollHeight;
}

function bootLog() {
    pushLog('> initializing trust layer session...', 'muted');
    pushLog('> connected to Polygon Amoy testnet', 'ok');
    pushLog('> 3 agents registered, keys loaded', 'muted');
    pushLog('> awaiting action stream...', 'muted');
}
bootLog();

function runVerification() {
    lineDelay = 0;
    pushLog('> recomputing hashes for all logged actions...', 'muted');
    document.querySelectorAll('.log-item').forEach((item, i) => {
        setTimeout(() => {
            if (!item.classList.contains('tampered')) {
                pushLog('> action #' + item.dataset.id + ' — hash match — OK', 'ok');
            } else {
                pushLog('> action #' + item.dataset.id + ' — hash mismatch — FLAGGED', 'warn');
            }
        }, i * 300);
    });
    setTimeout(
        () => pushLog('> verification pass complete', 'ok'),
        document.querySelectorAll('.log-item').length * 300 + 200
    );
}

function simulateTamper() {
    const items = document.querySelectorAll('.log-item');
    const target = items[Math.floor(Math.random() * items.length)];

    if (target.classList.contains('tampered')) return;

    target.classList.add('tampered');
    const badge = target.querySelector('.badge');
    badge.textContent = 'Tampered';
    badge.classList.remove('verified');
    badge.classList.add('flagged');

    const hashEl = target.querySelector('.log-hash');
    hashEl.textContent = hashEl.textContent.slice(0, 6) + '...???? (mismatch)';

    flagCount++;
    flagCountEl.textContent = flagCount;
    flagTrendEl.textContent = flagCount + ' record' + (flagCount > 1 ? 's' : '') + ' flagged';
    flagTrendEl.style.color = '#d1453b';

    lineDelay = 0;
    pushLog('> ALERT: signature mismatch on action #' + target.dataset.id, 'warn');
    pushLog('> stored hash does not match recomputed hash', 'warn');
    pushLog('> record marked as TAMPERED — origin unverifiable', 'warn');
}

let nextId = 4;
function logNewAction() {
    const inputs = document.querySelectorAll('.input-field');
    const agent = inputs[0].value || 'unnamed-agent';
    const action = inputs[1].value || 'unspecified action';
    const value = inputs[2].value || '';

    const list = document.getElementById('logList');
    const li = document.createElement('li');
    li.className = 'log-item';
    li.dataset.id = nextId++;
    li.style.opacity = '0';
    li.style.transform = 'translateY(10px)';

    const fakeHash = '0x' + Math.random().toString(16).slice(2, 6) + '...' + Math.random().toString(16).slice(2, 6);

    li.innerHTML = `
        <div class="log-main">
            <span class="log-title">${agent} — ${action}${value ? ' — ' + value : ''}</span>
            <span class="log-hash">${fakeHash}</span>
        </div>
        <span class="badge verified">Verified</span>
    `;
    list.appendChild(li);

    requestAnimationFrame(() => {
        li.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        li.style.opacity = '1';
        li.style.transform = 'translateY(0)';
    });

    lineDelay = 0;
    pushLog('> signing new action with agent private key...', 'muted');
    pushLog('> hash generated: ' + fakeHash, 'muted');
    pushLog('> anchored to chain — action #' + li.dataset.id + ' verified', 'ok');

    inputs.forEach(i => i.value = '');
}