import { Identity, Policy } from "./types";
import { gameState } from './state';

// Boards by player count
const BOARDS = {
    small: [null, null, "POLICY_PEEK", "EXECUTION", "EXECUTION", "WIN"], // 5-6 players
    medium: [null, "INVESTIGATE", "SPECIAL_ELECTION", "EXECUTION", "EXECUTION", "WIN"], // 7-8 players
    large: ["INVESTIGATE", "INVESTIGATE", "SPECIAL_ELECTION", "EXECUTION", "EXECUTION", "WIN"] // 9-10 players
};

export function rotateTrader() {
    do {
        gameState.traderIndex = (gameState.traderIndex + 1) % gameState.players.length;
    } while (!gameState.players[gameState.traderIndex].isAlive);
    gameState.nominatedSupplierId = null;
    gameState.hand = [];
}

export function checkWinConditions() {
    if (gameState.scores.authentic >= 5) {
        gameState.status = 'END';
        gameState.lastResult = "🏆 AUTHENTIC TEAM WINS!";
    } else if (gameState.scores.fraudulent >= 6) {
        gameState.status = 'END';
        gameState.lastResult = "💀 FRAUDULENT TEAM WINS!";
    }
}

export function adjustFunds(amount: number) {
    gameState.funds += amount;
    console.log(`Funds adjusted by ${amount}M. Current: €${gameState.funds}M`);

    if (gameState.funds <= 0) {
        if (gameState.status === 'POWER') {
            console.log("Bankruptcy pending: Waiting for Power to resolve first.");
            return;
        } 
        processBankruptcy();
    }
}

export function processBankruptcy() {
    if (gameState.funds > 0) return;
        // Penalty: Enact the top card of the deck automatically
        const enacted = gameState.policyDeck.shift();
        if (enacted) {
            console.log(`BANKRUPTCY! Top card enacted: ${enacted}`);
            if (enacted === 'Authentic') gameState.scores.authentic++;
            else gameState.scores.fraudulent++;
            
            const bankruptcyMsg = `\n 📉 Funds hit €0. To keep up with supply pressures, the top batch was forced: ${enacted.toUpperCase()}. Funds reset to €3M.`;
            gameState.lastResult += bankruptcyMsg;

            if (enacted === 'Fraudulent') {
                triggerPowerLogic();
            }
        }
        
        gameState.funds = 3; // Reset funds
        checkWinConditions(); // Check for wins after the forced card
};

export function startGameLogic() {
    const playerCount = gameState.players.length;

    // 1. Role Distribution logic
    let fraudulentCount = 1;
    if (playerCount >= 7) fraudulentCount = 2;
    if (playerCount >= 9) fraudulentCount = 3;

    let roles: Identity[] = ['Trick-Meister'];
    for (let i = 0; i < fraudulentCount; i++) roles.push('Fraudulent');
    while (roles.length < playerCount) roles.push('Authentic');

    // Shuffle Identities
    roles.sort(() => Math.random() - 0.5);
    gameState.players.forEach((p, i) => { p.identity = roles[i]; });

    // 2. Policy Deck (11 Fraudulent, 6 Authentic)
    const deck: Policy[] = [
        ...Array(11).fill('Fraudulent'),
        ...Array(6).fill('Authentic')
    ];
    deck.sort(() => Math.random() - 0.5);

    // 3. Board type
    if (playerCount <= 6) gameState.boardType = 'small';
    else if (playerCount <= 8) gameState.boardType = 'medium';
    else gameState.boardType = 'large';

    gameState.policyDeck = deck;
    gameState.status = 'ELECTION'; 
    gameState.traderIndex = Math.floor(Math.random() * playerCount); 
    
    console.log("Game setup complete. Status: ELECTION");
}

// Trigger power logic
export function triggerPowerLogic() {
    const slotIndex = gameState.scores.fraudulent - 1;
    const power = BOARDS[gameState.boardType][slotIndex];
    
    if (power && power !== "WIN" && gameState.status !== 'END') {
        gameState.activePower = power;
        gameState.status = 'POWER';
        console.log(`POWER TRIGGERED: ${power}`);
        gameState.nominatedSupplierId = null;
        gameState.hand = [];
    }
}   