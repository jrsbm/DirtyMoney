import { STATUS_CODES } from "http";
import { GameState, Identity, Policy } from "./types";

// Boards by player count
const BOARDS = {
    small: [null, null, "POLICY_PEEK", "EXECUTION", "EXECUTION", "WIN"], // 5-6 players
    medium: [null, "INVESTIGATE", "SPECIAL_ELECTION", "EXECUTION", "EXECUTION", "WIN"], // 7-8 players
    large: ["INVESTIGATE", "INVESTIGATE", "SPECIAL_ELECTION", "EXECUTION", "EXECUTION", "WIN"] // 9-10 players
};

export function rotateTrader(state: GameState) {
    do {
        state.traderIndex = (state.traderIndex + 1) % state.players.length;
    } while (!state.players[state.traderIndex].isAlive);
    state.nominatedSupplierId = null;
    state.hand = [];
}

export function checkWinConditions(state: GameState) {
    if (state.scores.authentic >= 5) {
        state.status = 'END';
        state.lastResult = "🏆 AUTHENTIC TEAM WINS!";
    } else if (state.scores.fraudulent >= 6) {
        state.status = 'END';
        state.lastResult = "💀 FRAUDULENT TEAM WINS!";
    }
}

export function adjustFunds(state: GameState, amount: number) {
    state.funds += amount;
    console.log(`Funds adjusted by ${amount}M. Current: €${state.funds}M`);

    if (state.funds <= 0) {
        if (state.status === 'POWER') {
            console.log("Bankruptcy pending: Waiting for Power to resolve first.");
            return;
        } 
        processBankruptcy(state);
    }
}

export function processBankruptcy(state: GameState) {
    if (state.funds > 0) return;
        // Penalty: Enact the top card of the deck automatically
        const enacted = state.policyDeck.shift();
        if (enacted) {
            console.log(`BANKRUPTCY! Top card enacted: ${enacted}`);
            if (enacted === 'Authentic') state.scores.authentic++;
            else state.scores.fraudulent++;
            
            const bankruptcyMsg = `\n 📉 Funds hit €0. To keep up with supply pressures, the top batch was forced: ${enacted.toUpperCase()}. Funds reset to €3M.`;
            state.lastResult += bankruptcyMsg;

            if (enacted === 'Fraudulent') {
                triggerPowerLogic(state);
            }
        }
        
        state.funds = 3; // Reset funds
        checkWinConditions(state); // Check for wins after the forced card
};

export function startGameLogic(state: GameState) {
    const playerCount = state.players.length;

    // 1. Role Distribution logic
    let fraudulentCount = 1;
    if (playerCount >= 7) fraudulentCount = 2;
    if (playerCount >= 9) fraudulentCount = 3;

    let roles: Identity[] = ['Trick-Meister'];
    for (let i = 0; i < fraudulentCount; i++) roles.push('Fraudulent');
    while (roles.length < playerCount) roles.push('Authentic');

    // Shuffle Identities
    roles.sort(() => Math.random() - 0.5);
    state.players.forEach((p, i) => { p.identity = roles[i]; });

    // 2. Policy Deck (11 Fraudulent, 6 Authentic)
    const deck: Policy[] = [
        ...Array(11).fill('Fraudulent'),
        ...Array(6).fill('Authentic')
    ];
    deck.sort(() => Math.random() - 0.5);

    // 3. Board type
    if (playerCount <= 6) state.boardType = 'small';
    else if (playerCount <= 8) state.boardType = 'medium';
    else state.boardType = 'large';

    state.policyDeck = deck;
    state.status = 'ELECTION'; 
    state.traderIndex = Math.floor(Math.random() * playerCount); 
    
    console.log("Game setup complete. Status: ELECTION");
}

// Trigger power logic
export function triggerPowerLogic(state: GameState) {
    const slotIndex = state.scores.fraudulent - 1;
    const power = BOARDS[state.boardType][slotIndex];
    
    if (power && power !== "WIN" && state.status !== 'END') {
        state.activePower = power;
        state.status = 'POWER';
        console.log(`POWER TRIGGERED: ${power}`);
        state.nominatedSupplierId = null;
        state.hand = [];
    }
}   