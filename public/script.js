let myPlayerId = null;

const BOARDS = {
    small: [null, null, "POLICY_PEEK", "EXECUTION", "EXECUTION", "FRAUDULENT_WIN"],
    medium: [null, "INVESTIGATE", "SPECIAL_ELECTION", "EXECUTION", "EXECUTION", "FRAUDULENT_WIN"],
    large: ["INVESTIGATE", "INVESTIGATE", "SPECIAL_ELECTION", "EXECUTION", "EXECUTION", "FRAUDULENT_WIN"]
};

async function joinGame() {
    const nameInput = document.getElementById('playerName');
    const name = nameInput.value.trim();
    const joinBtn = document.querySelector('#setup-ui button');
    if (!name) return alert("Enter a name!");

    joinBtn.innerText = "joining...";
    joinBtn.disabled = true;

    try{
        const response = await fetch('/join', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: name })
        });

        if (response.ok) {
            const data = await response.json();
            myPlayerId = data.id;
            localStorage.setItem('dirtyMoneyPlayerId', myPlayerId);
            document.getElementById('setup-ui').innerHTML = `<p style="color: var(--clr-authentic); font-family: var(--font-display); text-transform: uppercase;">✓ Joined as <b>${name}</b></p>`;
            console.log("Joined successfully! ID assigned:", myPlayerId);
            refreshLobby();
        } else {
            joinBtn.innerText = "enter";
            joinBtn.disabled = false;
            const errorData = await response.json();
            alert("Failed to join: " + (errorData.error || response.statusText));
        }
    } catch (err) {
        console.error("Network error:", err);
        joinBtn.innerText = "enter";
        joinBtn.disabled = false;
        alert("Could not connect to server.");
    }
}

document.getElementById('playerName').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        joinGame();
    }
});

async function toggleReady() {
    const btn = document.getElementById('readyBtn');
    const response = await fetch('/ready', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ playerId: myPlayerId })
    });

    if (response.ok) {
        const data = await response.json();
        btn.innerText = data.isReady ? "unready" : "mark ready";
    }
}

document.addEventListener('keypress', function (e) {
    if (e.target.tagName === 'INPUT' || e.target.tagName === 'TEXTAREA') {
        return;
    }
    if (e.key.toLowerCase() === 'r') {
        toggleReady();
    }
})

async function nominateSupplier(targetId) {
    const response = await fetch('/nominate', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            traderId: myPlayerId, 
            supplierId: targetId 
        })
    });

    if (response.ok) {
        console.log("Nomination sent!");
        refreshLobby();
    } else {
        const err = await response.json();
        alert(err.error);
    }
}

async function sendVote(isYes) {
    const response = await fetch('/vote', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            playerId: myPlayerId, 
            vote: isYes 
        })
    });
    if (response.ok) {
        console.log("Vote cast!");
        document.getElementById('voting-ui').style.display = 'none';
    }
}

document.addEventListener('keydown', (e) => {
    const votingUI = document.getElementById('voting-ui');
    if (votingUI.style.display === 'block') {
        const key = e.key.toLowerCase();
        if (key === 'y') sendVote(true);
        else if (key === 'n') sendVote(false);
    }
});

async function refreshLobby() {        
    try {
        const url = myPlayerId ? `/game-state?playerId=${myPlayerId}` : '/game-state';
        const response = await fetch(url);
        const data = await response.json();

        const setupUI = document.getElementById('setup-ui');
        const listElement = document.getElementById('playerList');

        if (!myPlayerId) {
            if (data.status !== 'LOBBY') {
                setupUI.innerHTML = `<p style="color: var(--clr-fraudulent);">🚫 Game in progress</p>`;
            } else if (data.players.length >= 10) {
                setupUI.innerHTML = `<p style="color: var(--clr-fraudulent);">🚫 Game Full (10/10)</p>`;
            }
        }

        listElement.innerHTML = '';
        if (data.players.length === 0) {
            const li = document.createElement('li');
            li.innerText = data.status !== 'LOBBY' ? "Game in progress..." : data.players.length >= 10 ? "Game Full" : "Waiting for players...";
            listElement.appendChild(li);
        }

        if (!myPlayerId) return;
        document.getElementById('gameStatus').innerText = data.status.toLowerCase();
        
        // Message box
        const msgBox = document.getElementById('game-message');
        if (data.lastResult) {
            msgBox.innerText = data.lastResult;
            msgBox.style.display = 'block';
            msgBox.classList.toggle('failure', data.lastResult.includes("FAIL") || data.lastResult.includes("FRAUDULENT"));
            msgBox.classList.toggle('success', !data.lastResult.includes("FAIL") && !data.lastResult.includes("FRAUDULENT"));
        } else {
            msgBox.style.display = 'none';
        }

        // Player list
        listElement.innerHTML = '';
        data.players.forEach((p, index) => {
            const li = document.createElement('li');
            const playerCard = document.createElement('div');
            playerCard.className = 'player-card';
            
            const readyUI = document.getElementById('ready-ui');
            readyUI.style.display = (myPlayerId && data.status === 'LOBBY') ? 'block' : 'none';

            if (!p.isAlive) {
                li.style.opacity = "0.5";
                const nameEl = document.createElement('span');
                nameEl.className = 'player-name';
                nameEl.innerHTML = `💀 <del>${p.name}</del>`;
                playerCard.appendChild(nameEl);
                const statusEl = document.createElement('span');
                statusEl.className = 'player-status eliminated';
                statusEl.innerText = 'fired';
                playerCard.appendChild(statusEl);
            } else {
                const nameEl = document.createElement('span');
                nameEl.className = 'player-name';
                nameEl.innerText = p.name;
                playerCard.appendChild(nameEl);

                const statusEl = document.createElement('span');
                statusEl.className = 'player-status';
                if (data.status === 'LOBBY' && p.isReady) {
                    statusEl.classList.add('ready');
                    statusEl.innerText = 'ready';
                } else if (data.status === 'VOTING' && data.votes[p.id] !== undefined) {
                    statusEl.classList.add('voted');
                    statusEl.innerText = 'voted';
                }
                if (statusEl.innerText) playerCard.appendChild(statusEl);

                // Identity badge
                if (p.identity && p.id !== myPlayerId) {
                    const badge = document.createElement('span');
                    badge.className = 'badge badge-identity';
                    badge.innerText = p.identity.toUpperCase();
                    playerCard.appendChild(badge);
                }

                // Trader badge
                if (data.status !== 'LOBBY' && index === data.traderIndex) {
                    const badge = document.createElement('span');
                    badge.className = 'badge badge-trader';
                    badge.innerText = 'trader';
                    playerCard.appendChild(badge);
                }

                // Supplier badge
                const isNominated = data.nominatedSupplierId === p.id;
                if (isNominated && (data.status === 'LEGISLATIVE' || data.status === 'POWER')) {
                    const badge = document.createElement('span');
                    badge.className = 'badge badge-supplier';
                    badge.innerText = 'supplier';
                    playerCard.appendChild(badge);
                }
            }
            li.appendChild(playerCard);
            listElement.appendChild(li);
        });

        // Identity Reveal
        const me = data.players.find(p => p.id === myPlayerId);
        if (me && me.identity) {
            const card = document.getElementById('role-card');
            const roleDisplay = document.getElementById('myRole');
            card.style.display = 'block';
            roleDisplay.innerText = me.identity.toUpperCase();
            roleDisplay.style.color = (me.identity === 'Authentic') ? 'var(--clr-authentic)' : 'var(--clr-fraudulent)';
        }

        // Election Logic
        const electionUI = document.getElementById('election-ui');
        const candidateZone = document.getElementById('supplier-candidates');
        const isMyTurn = (data.status === 'ELECTION' && data.players[data.traderIndex].id === myPlayerId);

        if (isMyTurn && !data.nominatedSupplierId) {
            electionUI.style.display = 'block';
            if (candidateZone.children.length === 0) {
                candidateZone.innerHTML = ''; 
                data.players.forEach(p => {
                    if (p.id !== myPlayerId) {
                        const btn = document.createElement('button');
                        btn.className = 'btn-primary';
                        btn.innerText = p.name;
                        btn.onclick = () => nominateSupplier(p.id);
                        candidateZone.appendChild(btn);
                    }
                });
            }
        } else {
            electionUI.style.display = 'none';
            candidateZone.innerHTML = '';
        }
        
        // Voting Logic
        const votingUI = document.getElementById('voting-ui');
        const votingAnnounce = document.getElementById('voting-announcement');
        const votingButtons = document.querySelectorAll('#voting-ui button');
        if (data.status === 'VOTING' && data.nominatedSupplierId) {
            votingUI.style.display = 'block';
            const haveVoted = data.votes && data.votes[myPlayerId] !== undefined;

            if (haveVoted) {
                votingAnnounce.innerText = "Waiting for others to vote...";
                votingButtons.forEach(b => b.style.display = 'none');
            } else {
                const supplier = data.players.find(p => p.id === data.nominatedSupplierId);
                votingAnnounce.innerText = `Should ${supplier.name} be the Supplier?`;
                votingButtons.forEach(b => b.style.display = 'inline-flex');
            }
        } else {
            votingUI.style.display = 'none';
            votingButtons.forEach(b => b.style.display = 'inline-flex');
        }

        // Legislative Logic
        const legUI = document.getElementById('legislative-ui');
        const handContainer = document.getElementById('policy-hand');
        const handInstruction = document.getElementById('hand-instruction');

        const isTrader = data.players[data.traderIndex].id === myPlayerId;
        const isSupplier = data.nominatedSupplierId === myPlayerId;

        if (data.status === 'LEGISLATIVE') { 
            legUI.style.display = 'block';
            const isTraderTurn = data.hand.length === 3;
            const isSupplierTurn = data.hand.length === 2;
            if (isTrader || isSupplier) {
                if (isTrader) {
                    handInstruction.innerText = isTraderTurn ? "you: select batch to discard" : "waiting for supplier...";
                } else if (isSupplier) {
                    handInstruction.innerText = isSupplierTurn ? "you: select batch to discard" : "waiting for trader...";
                }

                if ((isTrader && isTraderTurn) || (isSupplier && isSupplierTurn)) {
                    handContainer.innerHTML = '';
                    data.hand.forEach((policy, index) => {
                        const card = document.createElement('div');
                        card.className = `policy-card card-${policy.toLowerCase()}`;
                        card.innerText = policy;
                        card.onclick = () => discardCard(index);
                        handContainer.appendChild(card);
                    });
                } else {
                    handContainer.innerHTML = '';
                }
            } else {
                if (data.handCount === 3) {
                    handInstruction.innerText = "Trader is inspecting the batch...";
                    handContainer.innerHTML = `<div class="card-display">${getCardBackHTML()}${getCardBackHTML()}${getCardBackHTML()}</div>`;
                } else if (data.handCount === 2) {
                    handInstruction.innerText = "Supplier is choosing which batch to enact...";
                    handContainer.innerHTML = `<div class="card-display">${getCardBackHTML()}${getCardBackHTML()}</div>`;
                }
                else if (data.lastResult.includes('AUTHENTIC') || data.lastResult.includes('FRAUDULENT')) {
                    handInstruction.innerText = "Batch chosen!";
                    const result = data.lastResult.includes('AUTHENTIC') ? 'authentic' : 'fraudulent';
                    if (!document.getElementById('revealCard')) {
                        renderFlipReveal(result);
                    }
                }
            }
        } else {
            legUI.style.display = 'none';
        }

        // Scoreboard / Board Tracks
        const scoreboard = document.getElementById('scoreboard');
        const authenticTrack = document.getElementById('authentic-track');
        const fraudulentTrack = document.getElementById('fraudulent-track');
        const authScore = data.scores.authentic;
        const frScore = data.scores.fraudulent;

        if (data.status !== 'LOBBY') {
            scoreboard.style.display = 'flex';

            // Render Authentic Track (5 squares)
            authenticTrack.innerHTML = '';
            authenticTrack.style.gridTemplateColumns = 'repeat(6, 1fr)';
            for (let i = 0; i < 5; i++) {
                const square = document.createElement('div');
                square.className = `track-square authentic ${i < authScore ? 'filled' : ''}`;
                
                const miniCard = document.createElement('div');
                miniCard.className = 'mini-card card-authentic';
                miniCard.innerText = `<img src="authentic_card.svg" style="width: 100%; height: 100%; border-radius: 2px;">`;
                
                square.appendChild(miniCard);
                
                if (i === 4) {
                    const label = document.createElement('div');
                    label.className = 'square-label';
                    label.innerText = 'AUTHENTIC WIN';
                    square.appendChild(label);
                }
                
                authenticTrack.appendChild(square);
            }

            // Render Fraudulent Track (6 squares with power labels)
            fraudulentTrack.innerHTML = '';
            fraudulentTrack.style.gridTemplateColumns = 'repeat(6, 1fr)';
            const boardLabels = BOARDS[data.boardType] || BOARDS.small;
            for (let i = 0; i < 6; i++) {
                const square = document.createElement('div');
                square.className = `track-square fraudulent ${i < frScore ? 'filled' : ''}`;
                
                const miniCard = document.createElement('div');
                miniCard.className = 'mini-card card-fraudulent';
                miniCard.innerText = `<img src="fraudulent_card.svg" style="width: 100%; height: 100%; border-radius: 2px;">`;
                
                square.appendChild(miniCard);
                
                if (boardLabels[i]) {
                    const label = document.createElement('div');
                    label.className = 'square-label';
                    label.innerText = boardLabels[i].replace('_', ' ');
                    square.appendChild(label);
                }
                
                fraudulentTrack.appendChild(square);
            }
        } else {
            scoreboard.style.display = 'none';
        }

        // Power Phase Logic
        const powerUI = document.getElementById('power-ui');
        const privateResult = document.getElementById('private-result');
        const targetZone = document.getElementById('power-targets');

        if (data.powerResult && isTrader && data.status !== 'END') {
            privateResult.style.display = 'block';
            privateResult.innerHTML = `
            <div>👁️ private intel</div>
            <div style="margin: var(--space-md) 0;">${data.powerResult}</div>
            <button class="btn-secondary" onclick="endPowerTurn()" style="margin-top: var(--space-md); width: 100%;">continue</button>
            `;
        } else {
            privateResult.style.display = 'none';
        }

        if (data.status === 'POWER' && isTrader && data.activePower && !data.powerResult) {
            powerUI.style.display = 'block';
            document.getElementById('power-title').innerText = data.activePower.replace('_', ' ');

            targetZone.innerHTML = '';
            if (data.activePower === 'INVESTIGATE' || data.activePower === 'EXECUTION' || data.activePower === 'SPECIAL_ELECTION') {
                data.players.forEach(p => {
                    if (p.id !== myPlayerId && p.isAlive) {
                        const btn = document.createElement('button');
                        if (data.activePower === 'EXECUTION') {
                            btn.className = 'btn-danger';
                            btn.innerText = `fire ${p.name}`;
                        } else if (data.activePower === 'INVESTIGATE') {
                            btn.className = 'btn-secondary';
                            btn.innerText = `investigate ${p.name}`;
                        } else if (data.activePower === 'SPECIAL_ELECTION') {
                            btn.className = 'btn-secondary';
                            btn.innerText = `appoint ${p.name}`;
                        }
                        btn.onclick = () => usePower(p.id);
                        targetZone.appendChild(btn);
                    }
                });
            } else if (data.activePower === 'POLICY_PEEK') {
                const btn = document.createElement('button');
                btn.className = 'btn-secondary';
                btn.innerText = "view top 3 cards";
                btn.onclick = () => usePower(null);
                targetZone.appendChild(btn);
            }
        } else {
            powerUI.style.display = 'none';
        }

        // Funds Tracker
        const fundsDisplay = document.getElementById('funds-amount');
        const fundsTracker = document.getElementById('funds-tracker');
        
        if (data.status === 'LOBBY' || data.status === 'END') {
            fundsTracker.style.display = 'none';
        } else {
            fundsTracker.style.display = 'block';
            fundsDisplay.innerText = `€${data.funds}M`;
            fundsTracker.classList.toggle('warning', data.funds <= 1);
        }

    } catch (err) {
        console.error("Polling error:", err);
    }
}

async function discardCard(index) {
    const response = await fetch('/discard', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ 
            playerId: myPlayerId, 
            cardIndex: index 
        })
    });

    if (response.ok) {
        console.log("Card discarded");
        refreshLobby();
    } else {
        const err = await response.json();
        alert(err.error);
    }
}

function getCardBackHTML() {
    return `
        <div class="batch-card">
            <div class="card-face card-back">
                <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                    <rect x="2" y="6" width="20" height="12" rx="2" />
                    <circle cx="12" cy="12" r="2" />
                    <path d="M6 12h.01M18 12h.01" />
                </svg>
            </div>
        </div>
    `;
}

function renderFlipReveal(enacted) {
    const handContainer = document.getElementById('policy-hand');
    const svgUrl = enacted === 'authentic' ? 'authentic_card.svg' : 'fraudulent_card.svg';
    
    handContainer.innerHTML = `
        <div class="card-display">
            <div class="batch-card" id="revealCard">
                <div class="card-face card-back">
                    <svg width="30" height="30" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <rect x="2" y="6" width="20" height="12" rx="2" />
                        <circle cx="12" cy="12" r="2" />
                        <path d="M6 12h.01M18 12h.01" />
                    </svg>
                </div>
                <div class="card-face card-front policy-card card-${enacted}">
                    <img src="${svgUrl}" alt="${enacted}" style="width: 100%; height: 100%; border-radius: 8px;">
                </div>
            </div>
        </div>
    `;

    // Trigger the flip after a tiny delay so the eye can follow
    setTimeout(() => {
        const card = document.getElementById('revealCard');
        if (card) card.classList.add('flipped');
    }, 300);
}

async function usePower(targetId) {
    console.log("Using power on:", targetId);
    const response = await fetch('/use-power', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ playerId: myPlayerId, targetId: targetId })
    });
    if (response.ok) {
        console.log("Power used!");
        refreshLobby();
    } else {
        const err = await response.json();
        alert(err.error);
    }
}

async function endPowerTurn() {
    await fetch('/end-power', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ playerId: myPlayerId })
    });
    refreshLobby();
}

window.onload = async () => {
    const savedId = localStorage.getItem('dirtyMoneyPlayerId');
    if (savedId) {
        const response = await fetch(`/game-state?playerId=${savedId}`);
        const data = await response.json();
        const stillInGame = data.players.find(p => p.id === savedId);
        
        if (stillInGame) {
            myPlayerId = savedId;
            document.getElementById('setup-ui').innerHTML = 
                `<p style="color: var(--clr-authentic); font-family: var(--font-display); text-transform: uppercase;">✓ Reconnected as <b>${stillInGame.name}</b></p>`;
            console.log("Reconnected successfully:", myPlayerId);
        } else {
            localStorage.removeItem('dirtyMoneyPlayerId');
        }
    }
};

document.getElementById('playerName').focus();
setInterval(refreshLobby, 2000);