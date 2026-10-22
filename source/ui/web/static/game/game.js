// ── Constants ──────────────────────────────────────────
const DICE_SYMBOLS = ['', '⚀', '⚁', '⚂', '⚃', '⚄', '⚅'];
const FACE_NAMES   = { 1:'Ones', 2:'Twos', 3:'Threes', 4:'Fours', 5:'Fives', 6:'Sixes' };
const minName = 3, maxName = 15;

const CARD_LAYOUTS = {
    1: [{ col:'1/-1', row:'1/-1', center:true }],
    2: [{ col:1,row:1 },{ col:2,row:3 }],
    3: [{ col:1,row:1 },{ col:2,row:2 },{ col:1,row:3 }],
    4: [{ col:1,row:1 },{ col:2,row:1 },{ col:1,row:3 },{ col:2,row:3 }],
    5: [{ col:1,row:1 },{ col:2,row:1 },{ col:'1/-1',row:2,center:true },{ col:1,row:3 },{ col:2,row:3 }],
    6: [{ col:1,row:1 },{ col:2,row:1 },{ col:1,row:2 },{ col:2,row:2 },{ col:1,row:3 },{ col:2,row:3 }],
};

// ── Arena geometry ─────────────────────────────────────
// Arena: 572x572, radius 200
const CX = 286, CY = 286, R = 200;
const NS = 'http://www.w3.org/2000/svg';

// ── Permanent seat order — set once on first render ────
let seatOrder = null;   // array of player names in seat positions

// (inputs always visible — no toggle state needed)
let revealShown = false;   // guard so overlay only fires once per reveal
let _lastRound  = null;    // track round changes to reset bid inputs
let gameOverDismissed = false;  // stop poll loop from re-showing game-over after restart/quit

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
const bidQtyEl      = document.getElementById('bid-qty');
const qtyDec        = document.getElementById('qty-dec');
const qtyInc        = document.getElementById('qty-inc');
const faceBoxes     = Array.from(document.querySelectorAll('.face-box'));
let selectedFace    = 1;
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
        gameOverDismissed = false;   // fresh game — allow game-over card to show again later
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

    // Wild ones flag — always shown; ON (purple) or OFF (dim)
    const wildFlag = document.getElementById('wild-flag');
    if (wildFlag) {
        const badge = wildFlag.querySelector('.wild-flag-badge');
        if (badge) {
            badge.textContent = wildOnesMode ? 'ON' : 'OFF';
            badge.classList.toggle('on', wildOnesMode);
            badge.classList.toggle('off', !wildOnesMode);
        }
    }

}

let _lastHand = null;

/* Human player dice face value as cards */
function buildHandCards(hand) {

    // Terminate early if the hand hasn't changed
    const key = hand ? hand.join(',') : '';
    if (key === _lastHand) return;
    _lastHand = key;

    const wrap = document.getElementById('player-hand-cards');
    const divider = document.getElementById('hand-divider');
    const handTitle = document.getElementById('hand-title');
    if (!wrap) return;

    wrap.innerHTML = '';
    if (!hand || !hand.length) {
        divider.style.display = 'none';
        if (handTitle) handTitle.style.display = 'none';
        return;
    }
    divider.style.display = '';
    if (handTitle) handTitle.style.display = '';

    hand.forEach(v => {
        const cardWrap = document.createElement('div');
        cardWrap.className = 'card-wrap';

        const num = document.createElement('span');
        num.className = 'card-num';
        num.textContent = v;
        cardWrap.appendChild(num);

        const card = document.createElement('div');
        card.className = 'dice-card';
        CARD_LAYOUTS[v].forEach(p => {
            const pip = document.createElement('span');
            pip.className = 'pip-heart' + (p.center ? ' center' : '');
            pip.textContent = '♥';
            pip.style.gridColumn = p.col;
            pip.style.gridRow = p.row;
            card.appendChild(pip);
        });
        cardWrap.appendChild(card);
        wrap.appendChild(cardWrap);
    });
}


/* Current bid in the left panel — reuses the same die card as the hand */
function buildPanelBid(bid) {
    const qtyEl = document.getElementById('panel-bid-qty');
    const dieEl = document.getElementById('panel-bid-die');
    const xEl   = document.getElementById('panel-bid-x');
    if (!dieEl) return;
    if (!bid) {
        qtyEl.textContent = '—';
        dieEl.innerHTML = '';
        if (xEl) xEl.hidden = true;   // hide the × when there's no bid
        return;
    }
    qtyEl.textContent = bid.quantity;
    if (xEl) xEl.hidden = false;      // show the ×
    dieEl.innerHTML = '';
    const card = document.createElement('div');
    card.className = 'dice-card';
    (CARD_LAYOUTS[bid.face_value] || []).forEach(p => {
        const pip = document.createElement('span');
        pip.className = 'pip-heart' + (p.center ? ' center' : '');
        pip.textContent = '♥';
        pip.style.gridColumn = p.col;
        pip.style.gridRow = p.row;
        card.appendChild(pip);
    });
    dieEl.appendChild(card);
}


// ════════════════════════════════════════════════════════
// CONTROLS
// ════════════════════════════════════════════════════════

function renderFaceBoxes(currentBid) {
    const minFace = currentBid ? currentBid.face_value : 1;
    if (selectedFace < minFace) selectedFace = minFace;
    faceBoxes.forEach(box => {
        const f = parseInt(box.dataset.face);
        box.disabled = f < minFace;
        box.classList.toggle('selected', f === selectedFace);
    });
}

function enforceBidMin(currentBid) {
    renderFaceBoxes(currentBid);
    if (!currentBid) { bidQtyEl.min = 1; return; }
    if (selectedFace === currentBid.face_value) {
        bidQtyEl.min = currentBid.quantity + 1;
        if (parseInt(bidQtyEl.value) <= currentBid.quantity) bidQtyEl.value = currentBid.quantity + 1;
    } else {
        bidQtyEl.min = 1;
    }
}

faceBoxes.forEach(box => {
    box.addEventListener('click', () => {
        selectedFace = parseInt(box.dataset.face);
        renderFaceBoxes(window._currentBid);
        enforceBidMin(window._currentBid);
        bidQtyEl.value = bidQtyEl.min;   // reset qty to the floor for the chosen face
    });
});

qtyDec.addEventListener('click', () => {
    const floor = parseInt(bidQtyEl.min) || 1;
    const v = parseInt(bidQtyEl.value) || 1;
    if (v > floor) bidQtyEl.value = v - 1;
});

// Validate the quantity field; show "Invalid Bid" (red, under the controls) on failure
function validateQtyInput() {
    const raw   = bidQtyEl.value.trim();
    const qty   = parseInt(raw, 10);
    const floor = parseInt(bidQtyEl.min, 10) || 1;
    const ok    = /^\d+$/.test(raw) && Number.isInteger(qty) && qty >= floor;
    moveError.textContent = ok ? '' : 'Invalid Bid';
    return ok;
}
qtyInc.addEventListener('click', () => {
    const v = parseInt(bidQtyEl.value) || 1;
    bidQtyEl.value = v + 1;
});

bidBtn.addEventListener('click', async () => {
    const face = selectedFace;
    const qty  = parseInt(bidQtyEl.value, 10);
    moveError.textContent = '';

    if (face < 1 || face > 6 || !validateQtyInput()) return;
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
    await fetch('/reveal_continue', { method: 'POST' });
    revealShown = false;
});


// ════════════════════════════════════════════════════════
// REVEAL OVERLAY
// ════════════════════════════════════════════════════════

function showReveal(state) {
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
        const isWild = state.wild_ones && f === 1;
        const isBidFace = f === current_bid.face_value && !isWild;

        cell.className = 'face-cell'
            + (isBidFace ? ' bid-face' : '')
            + (isWild ? ' wild-face' : '');
        cell.innerHTML = `<span class="face-die">${DICE_SYMBOLS[f]}</span>
                      <span class="face-label"></span>
                      <span class="face-count">${reveal.face_counts[String(f)] ?? 0}</span>`;
        fc.appendChild(cell);
    }

    const rawCount  = reveal.face_counts[String(current_bid.face_value)] ?? 0;
    const wildCount = (state.wild_ones && current_bid.face_value !== 1)
        ? (reveal.face_counts["1"] ?? 0) : 0;
    const actual    = rawCount + wildCount;
    const wildNote  = wildCount > 0 ? ` (+${wildCount} wild)` : ``;

    // Result banner
    const banner  = document.getElementById('result-banner');
    const verdict = document.getElementById('result-verdict');
    const detail  = document.getElementById('result-detail');


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
// GAME END
// ════════════════════════════════════════════════════════


document.getElementById('restart-btn').addEventListener('click', async () => {
    document.getElementById('game-over').hidden = true;
    gameOverDismissed = true;   // suppress the poll loop from re-showing it during transition
    await fetch('/restart', { method: 'POST' });
    setupScreen.style.display = 'flex';
    gameScreen.style.display  = 'none';
    seatOrder = null;
    revealShown = false;
    revealOverlay.classList.remove('show');
});

// ════════════════════════════════════════════════════════
// RENDER
// ════════════════════════════════════════════════════════

function render(state) {
    if (!state.is_running) return;

    // Header
    document.getElementById('round-label').textContent = `Round ${state.round}`;

    // Reset bid inputs once per new round (guard vs. every 300ms poll, which would fight typing)
    if (state.round !== _lastRound) {
        _lastRound    = state.round;
        bidQtyEl.value = 1;
        bidQtyEl.min   = 1;
        selectedFace   = 1;
        renderFaceBoxes(null);
        validateQtyInput();
    }
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

    // Left-panel current bid
    buildPanelBid(state.current_bid);

    // Arena seats
    buildSeats(state.players, state.current_player, state.bid_holder);

    // Left panel
    buildPlayerPanel(state.players, state.current_player, state.bid_holder, state.dice_count, state.wild_ones);
    buildHandCards(state.player_hand);
    // Log — rebuild with full state.log; append round result lines when in reveal phase
    const log    = document.getElementById('action-log');
    const logBox = log.parentElement;
    const entries = [...(state.log || [])];

    // Check if user is at (or near) the bottom before rebuilding
    const isAtBottom = logBox.scrollHeight - logBox.scrollTop - logBox.clientHeight < 2;

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

    // Only auto-scroll if the user was already at the bottom
    if (isAtBottom) {
        logBox.scrollTop = logBox.scrollHeight;
    }

    // Always keep bid controls in sync with the current bid
    enforceBidMin(state.current_bid);

    // Controls — enable only on human turn
    const isMyTurn = state.current_player
        && state.players.find(p => p.name === state.current_player)?.is_bot === false;

    if (isMyTurn) {
        challengeBtn.disabled = !state.current_bid;
        bidBtn.disabled       = false;
    } else {
        challengeBtn.disabled = true;
        bidBtn.disabled       = true;
    }

    if (state.show_reveal){
        if(!revealShown){
            revealShown = true;
            showReveal(state);
        }
    }else{
        revealOverlay.classList.remove('show');
    }


    // Game over
    if (state.phase === 'game_over' && state.winner && !state.show_reveal && !gameOverDismissed){
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
