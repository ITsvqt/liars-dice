// ── Constants ─────────────────────────────────────────
const DICE_SYMBOLS = ['', '⚀', '⚁', '⚂', '⚃', '⚄', '⚅'];

const minName = 3
const maxName = 15

let setupData = null
let aiCount = null

// ── Elements ──────────────────────────────────────────
const setupScreen   = document.getElementById('setup-screen');
const gameScreen    = document.getElementById('game-screen');
const playerNameEl  = document.getElementById('player-name');
const nameHint      = document.getElementById('name-hint');
const takenNames    = document.getElementById('taken-names');
const aiCountEl     = document.getElementById('ai-count');
const aiDec         = document.getElementById('ai-dec');
const aiInc         = document.getElementById('ai-inc');
const wildOnes      = document.getElementById('wild-ones');
const setupError    = document.getElementById('setup-error');
const startBtn      = document.getElementById('start-btn');

// ── Load setup data ───────────────────────────────────
async function loadSetupData() {
    const response = await fetch('/setup') //todo implement the endpoint
    setupData = await response.json()

    playerNameEl.placeholder = setupData.suggested_name
    takenNames.textContent = "Taken names: " + setupData.ai_names.join(", ")
    wildOnes.checked = setupData.suggested_wild_ones
    aiCount = setupData.suggested_ai_count
    updateStepper()
}

// ── Stepper ───────────────────────────────────────────
function updateStepper() {
    aiCountEl.textContent = aiCount;
    aiDec.disabled = aiCount <= setupData.min_ai;
    aiInc.disabled = aiCount >= setupData.max_ai;
}

aiDec.addEventListener('click', () => {
    if (aiCount > setupData.min_ai) { aiCount--; updateStepper(); }
});

aiInc.addEventListener('click', () => {
    if (aiCount < setupData.max_ai) { aiCount++; updateStepper(); }
});

// ── Name validation ───────────────────────────────────
function validateName(name) {

    if (name.length < minName || name.length > maxName){
        return "Illegal name length [3:15]"
    }

    if (setupData.ai_names.includes(name)){
        return "Name already taken"
    }

    return null
}

playerNameEl.addEventListener('input', () => {
    const error = validateName(playerNameEl.value);
    nameHint.textContent = error ?? '';
    nameHint.classList.toggle('error', !!error);
});

// ── Submit setup ──────────────────────────────────────
startBtn.addEventListener('click', async () => {

     const data = {
        player_name: playerNameEl.value.trim(),
        ai_count: Number(aiCountEl.textContent),
        wild_ones: wildOnes.checked
    };

    try {
        const response = await fetch('/setup', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`Server error: ${response.status}`);
        }

        const result = await response.json();

        console.log('Setup successful:', result);

        // Switch to game screen
        setupScreen.style.display = 'none';
        gameScreen.style.display = 'block';

    } catch (error) {
        console.error('Setup failed:', error);
        setupError.textContent = 'Could not start the game. Please try again.';
    }
});
// ── Polling ───────────────────────────────────────────
async function poll() {
    // TODO: GET /state, call render(state), schedule next poll
}

// ── Render ────────────────────────────────────────────
function render(state) {
    // TODO: update all elements from state
}

// ── Init ──────────────────────────────────────────────
loadSetupData();
