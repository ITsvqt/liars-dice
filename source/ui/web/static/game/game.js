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
    const response = await fetch('/setup')
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

    const name = playerNameEl.value.trim() || setupData.suggested_name;
    const error = validateName(name);
    
    if (error){
        setupError.textContent = error;
        return;
    }

     const data = {
        player_name: name,
        cnt_ai: aiCount,
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

        console.log('setup response:', response.status);

        if (!response.ok) {
            const error = await response.text();  //! REMOVE THIS
            console.error('Server response:', error); //! REMOVE THIS
            throw new Error(`Server error: ${response.status}`);
        }

        const result = await response.json();

        console.log('Setup successful:', result);

        // Switch to game screen
        setupScreen.style.display = 'none';
        gameScreen.style.display = 'block';

    } catch (error) {
        console.error('Setup failed:', error); //! REMOVE THIS
        setupError.textContent = error.message
        //setupError.textContent = 'Could not start the game. Please try again.'; // ! UNCOMMENT THIS
    }
});
// ── Polling ───────────────────────────────────────────
async function poll() {
    const response = await fetch('/state')
    const state = await response.json()

    render(state)

    setTimeout(poll, 100)
}

// ── Render ────────────────────────────────────────────
function render(state) {
    // TODO: update all elements from state
}

// ── Init ──────────────────────────────────────────────
async function init() {

    const response = await fetch('/state');
    const state = await response.json();
    console.log('STATE:', state); // ! rEMOVE  THIS
    
    if (state.is_running) {
        // skip setup, go straight to game screen
        gameScreen.style.display = 'flex';
        
        render(state)
        poll()
        // start polling
    } else {
        setupScreen.style.display = 'flex';
        loadSetupData();
    }
}

init();
