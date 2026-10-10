// ── Constants ──────────────────────────────────────────
const DICE_SYMBOLS = ['', '⚀', '⚁', '⚂', '⚃', '⚄', '⚅'];
const FACE_NAMES   = { 1:'Ones', 2:'Twos', 3:'Threes', 4:'Fours', 5:'Fives', 6:'Sixes' };
const minName = 3, maxName = 15;

// ── Arena geometry ─────────────────────────────────────
// Larger arena: 480x480, radius 168
const CX = 260, CY = 260, R = 182;
const NS = 'http://www.w3.org/2000/svg';

// ── Permanent seat order — set once on first render ────
let seatOrder = null;   // array of player names in seat positions

// (inputs always visible — no toggle state needed)
let revealShown = false;   // guard so overlay only fires once per reveal

// ── Setup state ────────────────────────────────────────
let setupData = null, aiCount = null;

// ── Elements ───────────────────────────────────────────
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
const challengeBtn  = document.getElementById('challenge-btn');
const bidBtn        = document.getElementById('bid-btn');
const bidFaceEl     = document.getElementById('bid-face');
const bidQtyEl      = document.getElementById('bid-qty');
const moveError     = document.getElementById('move-error');
const revealOverlay = document.getElementById('reveal-overlay');


// ════════════════════════════════════════════════════════
// SETUP
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
    aiCountEl.textContent = aiCount;
    aiDec.disabled = aiCount <= setupData.min_ai;
    aiInc.disabled = aiCount >= setupData.max_ai;
}

aiDec.addEventListener('click', () => { if (aiCount > setupData.min_ai) { aiCount--; updateStepper(); } });
aiInc.addEventListener('click', () => { if (aiCount < setupData.max_ai) { aiCount++; updateStepper(); } });

function validateName(name) {
    if (name.length < minName || name.length > maxName) return 'Illegal name length [3:15]';
    if (setupData.ai_names.includes(name)) return 'Name already taken';
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

    try {
        const response = await fetch('/setup', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ player_name: name, cnt_ai: aiCount, wild_ones: wildOnes.checked })
        });
        if (!response.ok) throw new Error();
        setupScreen.style.display = 'none';
        gameScreen.style.display  = 'flex';
        poll();
    } catch {
        setupError.textContent = 'Could not start the game. Please try again.';
    }
});


// ════════════════════════════════════════════════════════
// ARENA
// ════════════════════════════════════════════════════════

function seatAngle(i, total) { return (2 * Math.PI * i / total) - Math.PI / 2; }
function seatPos(i, total) {
    const a = seatAngle(i, total);
    return { x: CX + R * Math.cos(a), y: CY + R * Math.sin(a) };
}

// Draw arc between two alive players, skipping eliminated ones.
// fromIdx and toIdx are indices into seatOrder.
function drawArc(players, fromName, toName) {
    const svg = document.getElementById('arc-svg');
    const old = svg.querySelector('#trail-arc');
    if (old) old.remove();

    const n        = seatOrder.length;
    const fromIdx  = seatOrder.indexOf(fromName);
    const toIdx    = seatOrder.indexOf(toName);
    if (fromIdx === -1 || toIdx === -1 || fromIdx === toIdx) return;

    // Walk forward from fromIdx to toIdx skipping eliminated seats
    // Build arc points seat-by-seat through alive players only
    const playerMap = {};
    players.forEach(p => playerMap[p.name] = p);

    // Collect the arc angle spans: from center of fromSeat to center of toSeat
    // going clockwise (forward in seatOrder)
    const aFrom = seatAngle(fromIdx, n);
    const aTo   = seatAngle(toIdx, n);
    const totalAngle = ((toIdx - fromIdx + n) % n) * (2 * Math.PI / n);

    const px = a => CX + R * Math.cos(a);
    const py = a => CY + R * Math.sin(a);
    const x1 = px(aFrom), y1 = py(aFrom);
    const x2 = px(aTo),   y2 = py(aTo);

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

    [[6, 0.2], [2, 1]].forEach(([w, o]) => {
        const l = document.createElementNS(NS, 'polyline');
        l.setAttribute('points', pts.join(' ')); l.setAttribute('fill', 'none');
        l.setAttribute('stroke', 'url(#trail-grad)'); l.setAttribute('stroke-width', w);
        l.setAttribute('stroke-linecap', 'round');   l.setAttribute('opacity', o);
        g.appendChild(l);
    });

    [{ cx: x1, cy: y1, f: '#7a6530' }, { cx: x2, cy: y2, f: '#c9a84c' }].forEach(d => {
        const c = document.createElementNS(NS, 'circle');
        c.setAttribute('cx', d.cx); c.setAttribute('cy', d.cy);
        c.setAttribute('r', '3.5'); c.setAttribute('fill', d.f);
        g.appendChild(c);
    });

    svg.appendChild(g);
}

function buildSeats(players, currentPlayerName, bidHolderName) {
    // Set permanent seat order on first call
    if (!seatOrder) {
        seatOrder = players.map(p => p.name);
    }

    const container = document.getElementById('seats');
    container.innerHTML = '';
    const n = seatOrder.length;

    // Build a map for fast lookup
    const playerMap = {};
    players.forEach(p => playerMap[p.name] = p);

    // Draw arc between bid holder and current player (only alive players)
    if (bidHolderName && currentPlayerName && bidHolderName !== currentPlayerName) {
        drawArc(players, bidHolderName, currentPlayerName);
    } else {
        const old = document.getElementById('arc-svg').querySelector('#trail-arc');
        if (old) old.remove();
    }

    seatOrder.forEach((name, i) => {
        const p = playerMap[name];
        if (!p) return;

        const pos         = seatPos(i, n);
        const isCurrent   = name === currentPlayerName  && !p.eliminated;
        const isBidHolder = name === bidHolderName      && !p.eliminated && name !== currentPlayerName;
        const initials    = name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();

        const seat = document.createElement('div');
        seat.className = 'seat'
            + (p.is_bot     ? ' bot'        : ' human')
            + (isCurrent    ? ' current'    : '')
            + (isBidHolder  ? ' bid-holder' : '')
            + (p.eliminated ? ' eliminated' : '');
        seat.style.left = pos.x + 'px';
        seat.style.top  = pos.y + 'px';

        const diceEl = p.eliminated
            ? `<span style="font-size:12px">💀</span>`
            : `<div class="dice-pip">${Array(p.dice_count).fill('<span class="pip"></span>').join('')}</div>`;

        seat.innerHTML = `<div class="avatar">${initials}</div>
                          <div class="seat-name">${name}</div>
                          ${diceEl}`;
        container.appendChild(seat);
    });
}


// ════════════════════════════════════════════════════════
// LEFT PANEL
// ════════════════════════════════════════════════════════

function buildPlayerPanel(players, currentPlayerName, bidHolderName, diceTotal, wildOnesMode) {
    const list = document.getElementById('player-list');
    list.innerHTML = '';

    const order = seatOrder || players.map(p => p.name);
    const playerMap = {};
    players.forEach(p => playerMap[p.name] = p);

    order.forEach(name => {
        const p = playerMap[name];
        if (!p) return;

        const isCurrent = name === currentPlayerName && !p.eliminated;

        const li = document.createElement('li');
        li.className = 'panel-player'
            + (isCurrent    ? ' current'    : '')
            + (p.eliminated ? ' eliminated' : '');

        // Solid number with "x" prefix, hidden when eliminated
        const countEl = p.eliminated
            ? ''
            : `<span class="panel-dice-count">×${p.dice_count}</span>`;

        li.innerHTML = `<span class="panel-player-name">${name}</span>${countEl}`;
        list.appendChild(li);
    });

    // Actual total: sum of all alive players' dice
    const total = players
        .filter(p => !p.eliminated)
        .reduce((sum, p) => sum + (p.dice_count || 0), 0);

    document.getElementById('dice-total').textContent = total || '—';

    // Wild ones flag
    const wildFlag = document.getElementById('wild-flag');
    if (wildFlag) wildFlag.hidden = !wildOnesMode;
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
        const res = await fetch('/move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ type: 'Bid', face, quantity: qty })
        });
        if (!res.ok) { moveError.textContent = 'Invalid move, try again.'; return; }
    } catch { moveError.textContent = 'Could not send move.'; return; }

    bidBtn.disabled       = true;
    challengeBtn.disabled = true;
});

challengeBtn.addEventListener('click', async () => {
    try {
        await fetch('/move', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ type: 'Challenge' })
        });
    } catch { moveError.textContent = 'Could not send move.'; }
    bidBtn.disabled = true;
    challengeBtn.disabled = true;
});


document.getElementById('reveal-continue').addEventListener('click', async () => {
    revealOverlay.classList.remove('show');
    revealShown = false;
    await fetch('/reveal_continue', { method: 'POST' });
});


// ════════════════════════════════════════════════════════
// REVEAL OVERLAY
// ════════════════════════════════════════════════════════

function showReveal(state) {
    console.log('showReveal called', JSON.stringify(state.reveal));  //! remove this
    console.log('current_bid', JSON.stringify(state.current_bid));  //! remove this
    if (state.phase === 'reveal' && state.reveal && state.reveal.winner && !revealShown) {
    console.log('reveal trigger hit', state.reveal.winner, revealShown);
    revealShown = true;
    showReveal(state);
    }                                                               //! Remove this
    const { round, players, current_bid, reveal } = state;

    document.getElementById('reveal-title').textContent = `Round ${round} — The Reveal`;

    // Player hands
    const handsEl = document.getElementById('player-hands');
    handsEl.innerHTML = '';
    reveal.player_hands.forEach(ph => {
        const isLoser  = ph.name === reveal.loser;
        const isWinner = ph.name === reveal.winner;
        const row = document.createElement('div');
        row.className = 'hand-row' + (isLoser ? ' loser' : isWinner ? ' winner' : '');
        const bg       = ph.is_bot ? '#2e4a2e' : '#3b5998';
        const initials = ph.name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();
        const faces    = ph.hand.map(v =>
            `<span class="die-face${v === current_bid.face_value ? ' bid-match' : ''}">${DICE_SYMBOLS[v]}</span>`
        ).join('');
        row.innerHTML = `<div class="hand-avatar" style="background:${bg}">${initials}</div>
                         <div class="hand-name">${ph.name}</div>
                         <div class="hand-dice">${faces}</div>`;
        handsEl.appendChild(row);
    });

    // Face counts — keys are strings from Python dict
    const fc = document.getElementById('face-counts');
    fc.innerHTML = '';
    for (let f = 1; f <= 6; f++) {
        const cell = document.createElement('div');
        cell.className = 'face-cell' + (f === current_bid.face_value ? ' bid-face' : '');
        cell.innerHTML = `<span class="face-die">${DICE_SYMBOLS[f]}</span>
                          <span class="face-count">${reveal.face_counts[String(f)] ?? 0}</span>
                          <span class="face-label">${f === current_bid.face_value ? 'bid' : ''}</span>`;
        fc.appendChild(cell);
    }

    // Result banner
    const banner  = document.getElementById('result-banner');
    const verdict = document.getElementById('result-verdict');
    const detail  = document.getElementById('result-detail');
    const actual  = reveal.face_counts[String(current_bid.face_value)] ?? 0;

    if (reveal.challenge_valid) {
        banner.className    = 'result-banner challenger-wins';
        verdict.textContent = `${reveal.winner} wins the challenge!`;
        detail.textContent  = `Only ${actual} ${FACE_NAMES[current_bid.face_value]} on the table — bid was ${current_bid.quantity}.`;
    } else {
        banner.className    = 'result-banner bidder-wins';
        verdict.textContent = `${reveal.winner}'s bid holds!`;
        detail.textContent  = `${actual} ${FACE_NAMES[current_bid.face_value]} found — bid of ${current_bid.quantity} stands.`;
    }

    const loserLine = document.getElementById('loser-line');
    loserLine.innerHTML = `<strong>${reveal.loser}</strong> loses a die.`
        + (reveal.loser_eliminated ? ` <span class="elim-tag">Eliminated</span>` : '');

    revealOverlay.classList.add('show');
}

// ════════════════════════════════════════════════════════
// RESTART BUTTON
// ════════════════════════════════════════════════════════


document.getElementById('play-again-btn').addEventListener('click', async () => {
    document.getElementById('game-over').hidden = true;
    await fetch('/restart', { method: 'POST' });
    // poll will pick up the new state automatically
});

// ════════════════════════════════════════════════════════
// RENDER
// ════════════════════════════════════════════════════════

function render(state) {
    if (!state.is_running) return;

    // Header
    document.getElementById('round-label').textContent = `Round ${state.round}`;
    document.getElementById('turn-label').textContent  = state.current_player
        ? (state.players.find(p => p.name === state.current_player)?.is_bot === false
            ? 'Your turn'
            : `${state.current_player}'s turn`)
        : '';

    // Center bid
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
    window._wildOnes   = state.wild_ones;

    // Arena seats
    buildSeats(state.players, state.current_player, state.bid_holder);

    // Left panel
    buildPlayerPanel(state.players, state.current_player, state.bid_holder, state.dice_count, state.wild_ones);

    // Log — rebuild with full state.log; append round result lines when in reveal phase
    const log    = document.getElementById('action-log');
    const logBox = log.parentElement;
    const entries = [...(state.log || [])];

    // If reveal is complete, append result summary as extra lines
    if (state.phase === 'reveal' && state.reveal && state.reveal.winner) {
        const cb     = state.current_bid;
        const actual = cb ? (state.reveal.face_counts[String(cb.face_value)] ?? 0) : 0;
        if (state.reveal.challenge_valid) {
            entries.push(`✓ Bluff! Only ${actual} × ${FACE_NAMES[cb?.face_value]} on table.`);
            entries.push(`${state.reveal.winner} wins the challenge.`);
        } else {
            entries.push(`✗ Bid stands. ${actual} × ${FACE_NAMES[cb?.face_value]} found.`);
            entries.push(`${state.reveal.winner}'s bid holds.`);
        }
        entries.push(`${state.reveal.loser} loses a die.${state.reveal.loser_eliminated ? ' Eliminated.' : ''}`);
    }

    log.innerHTML = '';
    entries.forEach((entry, i) => {
        const li = document.createElement('li');
        li.textContent = entry;
        if (i === entries.length - 1) li.classList.add('highlight');
        log.appendChild(li);
    });

    const spacer = document.createElement('li');
    spacer.className = 'spacer';
    log.appendChild(spacer);
    logBox.scrollTop = logBox.scrollHeight;

    // Controls — enable only on human turn
    const isMyTurn = state.current_player
        && state.players.find(p => p.name === state.current_player)?.is_bot === false;

    if (isMyTurn) {
        challengeBtn.disabled = !state.current_bid;
        bidBtn.disabled       = false;
        enforceBidMin(state.current_bid);
    } else {
        challengeBtn.disabled = true;
        bidBtn.disabled       = true;
    }

    // Reveal overlay — show once per reveal, not on every poll tick
    if (state.phase === 'reveal' && state.reveal && state.reveal.winner && !revealShown) {
        revealShown = true;
        showReveal(state);
    }
    // Reset guard when phase leaves reveal
    if (state.phase !== 'reveal') {
        revealShown = false;
    }

    // Game over
    if (state.winner) {
        document.getElementById('game-over').hidden = false;
        document.getElementById('game-over-title').textContent =
            state.winner === state.players.find(p => !p.is_bot)?.name ? '🏆 You Win!' : 'Game Over';
        document.getElementById('game-over-msg').textContent = `${state.winner} wins the game!`;
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
