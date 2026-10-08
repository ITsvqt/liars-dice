// ── Constants ──────────────────────────────────────────
const DICE_SYMBOLS = ['', '⚀', '⚁', '⚂', '⚃', '⚄', '⚅'];
const FACE_NAMES   = { 1:'Ones', 2:'Twos', 3:'Threes', 4:'Fours', 5:'Fives', 6:'Sixes' };
const minName = 3;
const maxName = 15;

// ── Setup state ────────────────────────────────────────
let setupData = null;
let aiCount   = null;

// ── Arena geometry ─────────────────────────────────────
const CX = 180, CY = 180, R = 128;
const NS = 'http://www.w3.org/2000/svg';

// ── Bid input state ────────────────────────────────────
let bidOpen = false;

// ── Setup elements ─────────────────────────────────────
const setupScreen  = document.getElementById('setup-screen');
const gameScreen   = document.getElementById('game-screen');
const playerNameEl = document.getElementById('player-name');
const nameHint     = document.getElementById('name-hint');
const takenNames   = document.getElementById('taken-names');
const aiCountEl    = document.getElementById('ai-count');
const aiDec        = document.getElementById('ai-dec');
const aiInc        = document.getElementById('ai-inc');
const wildOnes     = document.getElementById('wild-ones');
const setupError   = document.getElementById('setup-error');
const startBtn     = document.getElementById('start-btn');

// ── Game elements ──────────────────────────────────────
const challengeBtn = document.getElementById('challenge-btn');
const bidBtn       = document.getElementById('bid-btn');
const bidInputs    = document.getElementById('bid-inputs');
const bidFaceEl    = document.getElementById('bid-face');
const bidQtyEl     = document.getElementById('bid-qty');
const moveError    = document.getElementById('move-error');
const revealOverlay= document.getElementById('reveal-overlay');


// ════════════════════════════════════════════════════════
// SETUP SCREEN
// ════════════════════════════════════════════════════════

async function loadSetupData() {
    const response = await fetch('/setup');
    setupData = await response.json();

    playerNameEl.placeholder = setupData.suggested_name;
    takenNames.textContent   = 'Taken names: ' + setupData.ai_names.join(', ');
    wildOnes.checked         = setupData.suggested_wild_ones;
    aiCount                  = setupData.suggested_ai_count;
    updateStepper();
}

function updateStepper() {
    aiCountEl.textContent  = aiCount;
    aiDec.disabled         = aiCount <= setupData.min_ai;
    aiInc.disabled         = aiCount >= setupData.max_ai;
}

aiDec.addEventListener('click', () => { if (aiCount > setupData.min_ai) { aiCount--; updateStepper(); } });
aiInc.addEventListener('click', () => { if (aiCount < setupData.max_ai) { aiCount++; updateStepper(); } });

function validateName(name) {
    if (name.length < minName || name.length > maxName) return 'Illegal name length [3:15]';
    if (setupData.ai_names.includes(name))               return 'Name already taken';
    return null;
}

playerNameEl.addEventListener('input', () => {
    const error = validateName(playerNameEl.value);
    nameHint.textContent = error ?? '';
    nameHint.classList.toggle('error', !!error);
});

startBtn.addEventListener('click', async () => {
    const name  = playerNameEl.value.trim() || setupData.suggested_name;
    const error = validateName(name);
    if (error) { setupError.textContent = error; return; }

    const data = { player_name: name, cnt_ai: aiCount, wild_ones: wildOnes.checked };

    try {
        const response = await fetch('/setup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data)
        });

        if (!response.ok) throw new Error(`Server error: ${response.status}`);

        setupScreen.style.display = 'none';
        gameScreen.style.display  = 'flex';
        poll();

    } catch (err) {
        setupError.textContent = 'Could not start the game. Please try again.';
    }
});


// ════════════════════════════════════════════════════════
// ARENA — seats + arc
// ════════════════════════════════════════════════════════

function seatAngle(i, total) { return (2 * Math.PI * i / total) - Math.PI / 2; }
function seatPos(i, total) {
    const a = seatAngle(i, total);
    return { x: CX + R * Math.cos(a), y: CY + R * Math.sin(a) };
}

function drawArc(fromIdx, toIdx, total) {
    const svg = document.getElementById('arc-svg');
    const old = svg.querySelector('#trail-arc');
    if (old) old.remove();

    const aFrom = seatAngle(fromIdx, total);
    const aTo   = seatAngle(toIdx,   total);
    const totalAngle = (2 * Math.PI / total) * ((toIdx - fromIdx + total) % total);
    const px = a => CX + R * Math.cos(a);
    const py = a => CY + R * Math.sin(a);
    const x1 = px(aFrom), y1 = py(aFrom), x2 = px(aTo), y2 = py(aTo);

    let defs = svg.querySelector('defs');
    if (!defs) { defs = document.createElementNS(NS, 'defs'); svg.appendChild(defs); }

    let grad = defs.querySelector('#trail-grad');
    if (!grad) {
        grad = document.createElementNS(NS, 'linearGradient');
        grad.setAttribute('id', 'trail-grad');
        grad.setAttribute('gradientUnits', 'userSpaceOnUse');
        grad.innerHTML = `<stop offset="0%" stop-color="#7a6530"/>
                          <stop offset="100%" stop-color="#c9a84c"/>`;
        defs.appendChild(grad);
    }
    grad.setAttribute('x1', x1); grad.setAttribute('y1', y1);
    grad.setAttribute('x2', x2); grad.setAttribute('y2', y2);

    const pts = [];
    for (let s = 0; s <= 40; s++) {
        const a = aFrom + (totalAngle * s / 40);
        pts.push(`${px(a)},${py(a)}`);
    }

    const g = document.createElementNS(NS, 'g');
    g.setAttribute('id', 'trail-arc');

    [[6, 0.22], [2, 1]].forEach(([w, o]) => {
        const l = document.createElementNS(NS, 'polyline');
        l.setAttribute('points', pts.join(' ')); l.setAttribute('fill', 'none');
        l.setAttribute('stroke', 'url(#trail-grad)'); l.setAttribute('stroke-width', w);
        l.setAttribute('stroke-linecap', 'round');   l.setAttribute('opacity', o);
        g.appendChild(l);
    });

    [{ cx: x1, cy: y1, f: '#7a6530' }, { cx: x2, cy: y2, f: '#c9a84c' }].forEach(d => {
        const c = document.createElementNS(NS, 'circle');
        c.setAttribute('cx', d.cx); c.setAttribute('cy', d.cy);
        c.setAttribute('r', '3');   c.setAttribute('fill', d.f);
        g.appendChild(c);
    });

    svg.appendChild(g);
}

function buildSeats(players, currentPlayerName, bidHolderName) {
    const container = document.getElementById('seats');
    container.innerHTML = '';
    const n = players.length;

    // find indices by name
    const currentIdx   = players.findIndex(p => p.name === currentPlayerName);
    const bidHolderIdx = players.findIndex(p => p.name === bidHolderName);

    if (bidHolderIdx !== -1 && bidHolderIdx !== currentIdx) {
        drawArc(bidHolderIdx, currentIdx, n);
    } else {
        const svg = document.getElementById('arc-svg');
        const old = svg.querySelector('#trail-arc');
        if (old) old.remove();
    }

    players.forEach((p, i) => {
        const pos        = seatPos(i, n);
        const isCurrent  = i === currentIdx  && !p.eliminated;
        const isBidHolder= i === bidHolderIdx && !p.eliminated && i !== currentIdx;
        const initials   = p.name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();

        const seat = document.createElement('div');
        seat.className = 'seat'
            + (p.is_bot    ? ' bot'        : ' human')
            + (isCurrent   ? ' current'    : '')
            + (isBidHolder ? ' bid-holder' : '')
            + (p.eliminated ? ' eliminated' : '');
        seat.style.left = pos.x + 'px';
        seat.style.top  = pos.y + 'px';

        const diceEl = p.eliminated
            ? `<span style="font-size:11px">💀</span>`
            : `<div class="dice-pip">${Array(p.dice_count).fill('<span class="pip"></span>').join('')}</div>`;

        seat.innerHTML = `<div class="avatar">${initials}</div>
                          <div class="seat-name">${p.name}</div>
                          ${diceEl}`;
        container.appendChild(seat);
    });
}


// ════════════════════════════════════════════════════════
// CONTROLS
// ════════════════════════════════════════════════════════

function enforceBidMin(currentBid) {
    if (!currentBid) { bidFaceEl.min = 1; bidQtyEl.min = 1; return; }
    const f = parseInt(bidFaceEl.value) || 1;
    if (f === currentBid.face_value) {
        bidQtyEl.min = currentBid.quantity + 1;
        if (parseInt(bidQtyEl.value) <= currentBid.quantity) bidQtyEl.value = currentBid.quantity + 1;
    } else if (f > currentBid.face_value) {
        bidQtyEl.min = 1;
    } else {
        bidFaceEl.value = currentBid.face_value;
        bidQtyEl.min    = currentBid.quantity + 1;
        if (parseInt(bidQtyEl.value) <= currentBid.quantity) bidQtyEl.value = currentBid.quantity + 1;
    }
}

bidFaceEl.addEventListener('input', () => enforceBidMin(window._currentBid));

bidBtn.addEventListener('click', async () => {
    if (!bidOpen) {
        bidOpen = true;
        bidInputs.classList.add('open');
        bidBtn.textContent = 'Place';
        enforceBidMin(window._currentBid);
        return;
    }

    // Place bid
    const face = parseInt(bidFaceEl.value);
    const qty  = parseInt(bidQtyEl.value);
    moveError.textContent = '';

    if (face < 1 || face > 6 || qty < 1) { moveError.textContent = 'Invalid values.'; return; }

    const cb = window._currentBid;
    if (cb && !(face > cb.face_value || (face === cb.face_value && qty > cb.quantity))) {
        moveError.textContent = 'Bid must be higher than the current bid.';
        return;
    }

    try {
        await fetch('/move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ type: 'Bid', face, quantity: qty })
        });
    } catch (e) { moveError.textContent = 'Could not send move.'; return; }

    bidOpen = false;
    bidInputs.classList.remove('open');
    bidBtn.textContent = 'Bid';
    bidBtn.disabled    = true;
    challengeBtn.disabled = true;
});

challengeBtn.addEventListener('click', async () => {
    try {
        await fetch('/move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ type: 'Challenge' })
        });
    } catch (e) { moveError.textContent = 'Could not send move.'; }

    bidBtn.disabled       = true;
    challengeBtn.disabled = true;
});

document.getElementById('reveal-continue').addEventListener('click', () => {
    revealOverlay.classList.remove('show');
});


// ════════════════════════════════════════════════════════
// REVEAL OVERLAY
// ════════════════════════════════════════════════════════

function showReveal(state) {
    const { round, players, current_bid, reveal } = state;
    // reveal = { players_hands, face_counts, winner, loser, loser_eliminated, challenge_valid }

    document.getElementById('reveal-title').textContent = `Round ${round} — The Reveal`;

    // Player hands
    const handsEl = document.getElementById('player-hands');
    handsEl.innerHTML = '';
    reveal.players_hands.forEach(ph => {
        const isLoser  = ph.name === reveal.loser;
        const isWinner = ph.name === reveal.winner;
        const row = document.createElement('div');
        row.className = 'hand-row' + (isLoser ? ' loser' : isWinner ? ' winner' : '');
        const bg      = ph.is_bot ? '#2e4a2e' : '#3b5998';
        const initials = ph.name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();
        const faces   = ph.hand.map(v =>
            `<span class="die-face${v === current_bid.face_value ? ' bid-match' : ''}">${DICE_SYMBOLS[v]}</span>`
        ).join('');
        row.innerHTML = `<div class="hand-avatar" style="background:${bg}">${initials}</div>
                         <div class="hand-name">${ph.name}</div>
                         <div class="hand-dice">${faces}</div>`;
        handsEl.appendChild(row);
    });

    // Face counts
    const fc = document.getElementById('face-counts');
    fc.innerHTML = '';
    for (let f = 1; f <= 6; f++) {
        const cell = document.createElement('div');
        cell.className = 'face-cell' + (f === current_bid.face_value ? ' bid-face' : '');
        cell.innerHTML = `<span class="face-die">${DICE_SYMBOLS[f]}</span>
                          <span class="face-count">${reveal.face_counts[f] ?? 0}</span>
                          <span class="face-label">${f === current_bid.face_value ? 'bid' : ''}</span>`;
        fc.appendChild(cell);
    }

    // Result banner
    const banner  = document.getElementById('result-banner');
    const verdict = document.getElementById('result-verdict');
    const detail  = document.getElementById('result-detail');
    const actual  = reveal.face_counts[current_bid.face_value] ?? 0;

    if (reveal.challenge_valid) {
        banner.className   = 'result-banner challenger-wins';
        verdict.textContent = `${reveal.winner} wins the challenge!`;
        detail.textContent  = `Only ${actual} ${FACE_NAMES[current_bid.face_value]} on the table — bid was ${current_bid.quantity}.`;
    } else {
        banner.className   = 'result-banner bidder-wins';
        verdict.textContent = `${reveal.winner}'s bid holds!`;
        detail.textContent  = `${actual} ${FACE_NAMES[current_bid.face_value]} found — bid of ${current_bid.quantity} stands.`;
    }

    // Loser line
    const loserLine = document.getElementById('loser-line');
    loserLine.innerHTML = `<strong>${reveal.loser}</strong> loses a die.`
        + (reveal.loser_eliminated ? ` <span class="elim-tag">Eliminated</span>` : '');

    revealOverlay.classList.add('show');
}


// ════════════════════════════════════════════════════════
// RENDER — called every poll tick
// ════════════════════════════════════════════════════════

function render(state) {
    if (!state.is_running) return;

    // Round + turn header
    document.getElementById('round-label').textContent  = `Round ${state.round}`;
    document.getElementById('turn-label').textContent   = state.current_player
        ? (state.players.find(p => p.name === state.current_player)?.is_bot === false
            ? 'Your turn'
            : `${state.current_player}'s turn`)
        : '';

    // Current bid (center of table)
    const bidDisplay = document.getElementById('current-bid');
    const bidSub     = document.getElementById('bid-sub');
    if (state.current_bid) {
        bidDisplay.textContent = `${state.current_bid.quantity} × ${FACE_NAMES[state.current_bid.face_value]}`;
        bidSub.textContent     = 'current bid';
    } else {
        bidDisplay.textContent = '—';
        bidSub.textContent     = 'no bid yet';
    }
    window._currentBid = state.current_bid;

    // Seats
    buildSeats(state.players, state.current_player, state.bid_holder);

    // Action log
    if (state.log && state.log.length) {
        const log = document.getElementById('action-log');
        log.innerHTML = '';
        state.log.forEach((entry, i) => {
            const li = document.createElement('li');
            li.textContent = entry;
            if (i === state.log.length - 1) li.classList.add('highlight');
            log.appendChild(li);
        });
        log.scrollTop = log.scrollHeight;
    }

    // Controls visibility — only show when it's the human's turn
    const controls = document.getElementById('controls');
    const isMyTurn = state.current_player
        && state.players.find(p => p.name === state.current_player)?.is_bot === false;

    if (isMyTurn && !bidOpen) {
        challengeBtn.disabled = !state.current_bid;
        bidBtn.disabled       = false;
        bidBtn.textContent    = 'Bid';
    } else if (!isMyTurn) {
        challengeBtn.disabled = true;
        bidBtn.disabled       = true;
    }

    // Reveal overlay
    if (state.phase === 'reveal' && state.reveal) {
        showReveal(state);
    }

    // Game over
    if (state.winner) {
        document.getElementById('game-over').hidden     = false;
        document.getElementById('game-over-title').textContent = state.winner === state.players.find(p => !p.is_bot)?.name
            ? '🏆 You Win!'
            : 'Game Over';
        document.getElementById('game-over-msg').textContent =
            `${state.winner} wins the game!`;
    }
}


// ════════════════════════════════════════════════════════
// POLLING + INIT
// ════════════════════════════════════════════════════════

async function poll() {
    try {
        const response = await fetch('/state');
        const state    = await response.json();
        render(state);
    } catch (e) {
        console.error('Poll failed:', e);
    }
    setTimeout(poll, 300);
}

async function init() {
    const response = await fetch('/state');
    const state    = await response.json();

    if (state.is_running) {
        gameScreen.style.display = 'flex';
        render(state);
        poll();
    } else {
        setupScreen.style.display = 'flex';
        loadSetupData();
    }
}

init();
