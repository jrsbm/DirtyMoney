import express from 'express';
import type { Request, Response } from 'express';
import path from 'path';
import { fileURLToPath } from 'url';

const app = express();
const PORT = 3000;

// Re-create __dirname for ES Modules
const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Roles (Secret Identities)
type Identity = 'Authentic' | 'Fraudulent' | 'Trick-Meister' | null;
// Policies (The Cards)
type Policy = 'Authentic' | 'Fraudulent';

interface Player {
    id: string;
    name: string;
    isReady: boolean;
    identity: Identity;
    isAlive: boolean;
}

interface GameState {
    players: Player[];
    status: 'LOBBY' | 'ELECTION' | 'VOTING' | 'LEGISLATIVE' | 'POWER' | 'END';
    policyDeck: Policy[];
    discardPile: Policy[];
    traderIndex: number;
    nominatedSupplierId: string | null;
    votes: Record<string, boolean>;
    lastResult: string | null;
    hand: Policy[];
    scores: { authentic: number; fraudulent: number };
    boardType: 'small' | 'medium' | 'large';
    activePower: string | null;
    powerResult: string | null;
    originalTraderIndex: number | null;
    tempNextTrader: number | null;
    funds: number;
}

let gameState: GameState = {
    players: [],
    status: 'LOBBY',
    policyDeck: [],
    discardPile: [],
    traderIndex: 0,
    nominatedSupplierId: null,
    votes: {},
    lastResult: null,
    hand: [],
    scores: { authentic: 0, fraudulent: 0 },
    boardType: 'small',
    activePower: null,
    powerResult: null,
    originalTraderIndex: null,
    tempNextTrader: null,
    funds: 3
};

app.use(express.static(path.join(__dirname, '../public')));
app.use(express.json());

// Game state route
app.get('/game-state', (req: Request, res: Response) => {
    const playerId = req.query.playerId as string;
    const safeState = JSON.parse(JSON.stringify(gameState));
    safeState.players = safeState.players.map((p: Player) => {
        if (p.id === playerId) return p;

        // Logic for "Fraudulent" players to see each other (but not for Authentic)
        const me = gameState.players.find(player => player.id === playerId);
        if (!me) return { ...p, identity: null };

        const isSmallGame = gameState.players.length <= 6;

        // Logic for Fraudulent Team visibility
        if (me.identity === 'Fraudulent') {
            // Fraudulents always see other Fraudulents. 
            // They only see the Trick-Meister in small games.
            if (p.identity === 'Fraudulent' || (isSmallGame && p.identity === 'Trick-Meister')) {
                return p;
            }
        }

        if (me.identity === 'Trick-Meister' && isSmallGame) {
            // Trick-Meister only sees the team in small games
            if (p.identity === 'Fraudulent') return p;
        }

        return { ...p, identity: null };
    });
    safeState.policyDeck = []; 
    safeState.deckCount = gameState.policyDeck.length;

    const isTrader = gameState.players[gameState.traderIndex]?.id === playerId;
    const isSupplier = gameState.nominatedSupplierId === playerId;

    if (gameState.status === 'LEGISLATIVE') {
        if ((gameState.hand.length === 3 && !isTrader) || (gameState.hand.length === 2 && !isSupplier)) {
            safeState.hand = []; // Hide cards from unauthorized eyes
        }
    } else {
        safeState.hand = []; // Hide hand when not in legislative phase
    }

    if (!isTrader) {
        safeState.powerResult = null; // Hide the investigation result from everyone else
    }
    
    res.json(safeState);


});

// Join route
app.post('/join', (req: Request, res: Response) => {
    const { name } = req.body;

    if (!name) {
        console.log("Join failed: No name provided");
        return res.status(400).json({ error: "Name is required" });
    }

    const cleanName = name.trim();
    const nameExists = gameState.players.some(
        p => p.name.toLowerCase() === cleanName.toLowerCase()
    );

    if (nameExists) {
        return res.status(400).json({ error: "That name is already taken!" });
    }

    if (gameState.players.length >= 10) {
        return res.status(403).json({ error: "Game is full" });
    }

    if (gameState.status !== 'LOBBY') {
        return res.status(403).json({ error: "Game already in progress" });
    }

    const newPlayer: Player = {
        id: Math.random().toString(36).substr(2, 9),
        name: name,
        isReady: false,
        identity: null,
        isAlive: true,
    };
    gameState.players.push(newPlayer);
    console.log(`${name} joined the game.Total players: ${gameState.players.length}`);
    res.json(newPlayer);
});

// Ready route
app.post('/ready', (req: Request, res: Response) => {
    const { playerId } = req.body;
    const player = gameState.players.find(p => p.id === playerId);

    if (!player) return res.status(404).json({ error: "Player not found" });
    if (gameState.status !== 'LOBBY') return res.status(400).json({ error: "Game already started" });

    // Toggle state
    player.isReady = !player.isReady;

    // Check if everyone is ready AND there are at least 5 players
    const allReady = gameState.players.length >= 5 && gameState.players.every(p => p.isReady);

    if (allReady) {
        // Trigger your existing start game logic here
        startGameLogic(); 
        console.log("Everyone ready! Starting game...");
    }

    res.json({ isReady: player.isReady, gameStarted: allReady });
});

// Start route
function startGameLogic() {
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

// Boards by player count
const BOARDS = {
    small: [null, null, "POLICY_PEEK", "EXECUTION", "EXECUTION", "WIN"], // 5-6 players
    medium: [null, "INVESTIGATE", "SPECIAL_ELECTION", "EXECUTION", "EXECUTION", "WIN"], // 7-8 players
    large: ["INVESTIGATE", "INVESTIGATE", "SPECIAL_ELECTION", "EXECUTION", "EXECUTION", "WIN"] // 9-10 players
};


// Nominate route
app.post('/nominate', (req: Request, res: Response) => {
    const {traderId, supplierId } = req.body;

    // Validate Trader
    const currentTrader = gameState.players[gameState.traderIndex];
    if (!currentTrader || currentTrader.id !== traderId) {
        return res.status(403).json({ error: "It is not your turn to nominate!"});
    }

    // No self-nomination
    if (traderId === supplierId) {
        return res.status(400).json({ error: "You cannot nominate yourself!"});
    }

    // No dead players
    const target = gameState.players.find(p => p.id === supplierId);
    if (!target || !target.isAlive) {
        return res.status(400).json({ error: "Target is not eligible!" });
    }

    // Update game state
    gameState.nominatedSupplierId = supplierId;
    gameState.status = 'VOTING';
    gameState.votes = {};
    gameState.lastResult = null;
    gameState.powerResult = null;

    const supplierName =gameState.players.find(p => p.id === supplierId)?.name;
    console.log(`${currentTrader.name} nominated ${supplierName} for the Supply Team.`);
    res.json({ message: "Nomination successful, voting begins."});
});

// Vote route
app.post('/vote', (req: Request, res: Response) => {
    const { playerId, vote } = req.body;

    // 1. Only allow voting during the VOTING phase
    if (gameState.status !== 'VOTING') {
        return res.status(400).json({ error: "No election is active." });
    }

    // 2. Record the vote
    gameState.votes[playerId] = vote;
    console.log(`Vote received from ${playerId}. Total: ${Object.keys(gameState.votes).length}/${gameState.players.length}`);

    // 3. Check if everyone has voted
    const livingPlayers = gameState.players.filter(p => p.isAlive);
    if (Object.keys(gameState.votes).length === gameState.players.length) {
        const yesVotes = Object.values(gameState.votes).filter(v => v === true).length;
        const totalPlayers = gameState.players.length;

        if (yesVotes > totalPlayers / 2) {
            // SUCCESS: Election Passes
            console.log("Election Passed!");
            gameState.lastResult = 'PASS';
            gameState.status = 'LEGISLATIVE';
            gameState.hand = gameState.policyDeck.splice(0, 3);
        } else {
            // FAILURE: Election Fails
            console.log("Election Failed! Moving to next Trader.");
            gameState.lastResult = 'FAIL - Funds decreased by €1M';
            adjustFunds(-1);
            gameState.status = 'ELECTION';
            rotateTrader();
            gameState.nominatedSupplierId = null;
        }
        
        // Reset votes for the next round
        gameState.votes = {};
    }

    res.json({ message: "Vote cast successfully" });
});

// Check win
function checkWinConditions() {
    if (gameState.scores.authentic >= 5) {
        gameState.status = 'END';
        gameState.lastResult = "🏆 AUTHENTIC TEAM WINS!";
    } else if (gameState.scores.fraudulent >= 6) {
        gameState.status = 'END';
        gameState.lastResult = "💀 FRAUDULENT TEAM WINS!";
    }
}

// Trigger power logic
function triggerPowerLogic() {
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

function rotateTrader() {
    do {
        gameState.traderIndex = (gameState.traderIndex + 1) % gameState.players.length;
    } while (!gameState.players[gameState.traderIndex].isAlive);
    gameState.nominatedSupplierId = null;
    gameState.hand = [];
}

// Discard route
app.post('/discard', (req: Request, res: Response) => {
    const { playerId, cardIndex } = req.body;
    
    // 1. Is it the Trader's turn to discard? (3 cards in hand)
    const isTrader = gameState.players[gameState.traderIndex].id === playerId;
    const isSupplier = gameState.nominatedSupplierId === playerId;

    if (gameState.hand.length === 3 && isTrader) {
        const discarded = gameState.hand.splice(cardIndex, 1);
        gameState.discardPile.push(discarded[0]);
        return res.json({ message: "Trader discarded. Supplier's turn." });
    }

    // 2. Is it the Supplier's turn to discard? (2 cards in hand)
    if (gameState.hand.length === 2 && isSupplier) {
        const discarded = gameState.hand.splice(cardIndex, 1);
        gameState.discardPile.push(discarded[0]);
        const enacted = gameState.hand.pop()!;
        console.log(`BATCH SELECTED: ${enacted}`);
        
        if (enacted === 'Authentic') {
            gameState.scores.authentic++;
            gameState.lastResult = `📜 A batch was selected: AUTHENTIC. \n€2M added to company funds`;
            adjustFunds(2);
        } else {
            gameState.scores.fraudulent++;
            gameState.lastResult = `📜 A batch was selected: FRAUDULENT. \n€1M deducted from company funds`;
            triggerPowerLogic();
            if (gameState.activePower) {
                gameState.lastResult += `\n ⚠️ Power Triggered: ${gameState.activePower.replace('_', ' ')}.`;
            }
            adjustFunds(-1);
        }

        // Check for Win Conditions
        checkWinConditions();        
        if (gameState.status !== 'END' && gameState.status !== 'POWER') {
            // Reset for next round
            gameState.status = 'ELECTION';
            rotateTrader();
        }
        
        return res.json({ message: `Selected ${enacted}` });
    }

    res.status(400).json({ error: "Not your turn to discard or invalid action." });
});

// Power route
app.post('/use-power', (req: Request, res: Response) => {
    const { playerId, targetId } = req.body;
    const isTrader = gameState.players[gameState.traderIndex].id === playerId;

    if (!isTrader || gameState.status !== 'POWER') {
        return res.status(403).json({ error: "Not your turn to use a power." });
    }
    
    if (gameState.activePower === 'POLICY_PEEK') {
        const topThree = gameState.policyDeck.slice(0, 3).join(", ");
        gameState.powerResult = `The next three cards are: ${topThree}`;
        gameState.activePower = null;
        return res.json({ message: "Power used" });
    }

    // Powers that require a target
    const target = gameState.players.find(p => p.id === targetId);
    if (!target) {
        return res.status(400).json({ error: "Target not found" });
    }

    if (gameState.activePower === 'INVESTIGATE') {
        gameState.powerResult = `${target.name} is ${target.identity}`;
    } 

    if (gameState.activePower === 'EXECUTION') {
        target.isAlive = false;
        
        // Check if Trick-Meister died
        if (target.identity === 'Trick-Meister') {
            gameState.status = 'END';
            gameState.lastResult = `🏆 THE TRICK-MEISTER (${target.name}) WAS FIRED! AUTHENTIC TEAM WINS!`;
            gameState.powerResult = null;
            return res.json({ message: "Game Over" });
        } else {
            // If a Fraudulent was executed, check if that causes the Authentic team to win
            const remainingFraudulent = gameState.players.filter(p => p.isAlive && (p.identity === 'Fraudulent' || p.identity === 'Trick-Meister')).length;
            if (remainingFraudulent === 0) {
                gameState.status = 'END';
                gameState.lastResult = `🏆 ALL FRAUDULENT PLAYERS FIRED! AUTHENTIC TEAM WINS!`;
                gameState.powerResult = null;
                return res.json({ message : "Game Over" });
            } else {
                gameState.lastResult = `💀 ${target.name} has been FIRED but was NOT the Trick-Meister.`;
                gameState.powerResult = `Success, ${target.name} was fired.`;
            }
        }
    }

    if (gameState.activePower === 'SPECIAL_ELECTION') {
        // 1. Store who was SUPPOSED to be next (if we haven't already)
        if (gameState.originalTraderIndex === null) {
            gameState.originalTraderIndex = gameState.traderIndex;
        }

        // 2. Find the index of the chosen player
        const newTraderIndex = gameState.players.findIndex(p => p.id === targetId);
        
        // 3. Set them as the current trader, but keep status in POWER 
        // until the current trader clicks "OK"
        gameState.powerResult = `Election Override: ${target.name} will be the next Trader.`;
        gameState.lastResult = `📢 SPECIAL ELECTION: ${target.name} has been appointed as the next Trader!`;
        gameState.tempNextTrader = newTraderIndex;
    }

    gameState.activePower = null;
    res.json({ message: "Power used" });
});

app.post('/end-power', (req: Request, res: Response) => {
    const { playerId } = req.body;
    const isTrader = gameState.players[gameState.traderIndex].id === playerId;

    if (!isTrader) return res.status(403).json({ error: "Forbidden" });
    gameState.status = 'ELECTION';

    if (gameState.tempNextTrader !== null) {
        gameState.traderIndex = gameState.tempNextTrader;
        gameState.tempNextTrader = null; 
    } else {
        // Normal rotation
        // If we were in a special turn, we return to the original rotation
        if (gameState.originalTraderIndex !== null) {
            gameState.traderIndex = gameState.originalTraderIndex;
            gameState.originalTraderIndex = null;
        }
        do {
            gameState.traderIndex = (gameState.traderIndex + 1) % gameState.players.length;
        } while (!gameState.players[gameState.traderIndex].isAlive);
    }
    gameState.powerResult = null;
    res.json({ message: "Turn ended" });
});

// Funds function
function adjustFunds(amount: number) {
    gameState.funds += amount;
    console.log(`Funds adjusted by ${amount}M. Current: €${gameState.funds}M`);

    if (gameState.funds <= 0) {
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
                if (gameState.activePower) {
                    gameState.lastResult += ` (New Power: ${gameState.activePower.replace('_', ' ')})`;
                }
            }
        }
        
        // Reset funds
        gameState.funds = 3;
        // Check for wins after the forced card
        checkWinConditions(); 
    }
}

app.listen(PORT, () => {
    console.log(`🚀 Server ready at: http://localhost:${PORT}`);
});