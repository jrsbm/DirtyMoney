import express from 'express';
import type { Request, Response } from 'express';
import path from 'path';
import { fileURLToPath } from 'url';

import { lobbyRoutes } from './routes/lobby';
import { electionRoutes } from './routes/election';
import { legislativeRoutes } from './routes/legislative';
import { Player } from './types';
import { gameState } from './state';

const app = express();
const PORT = process.env.PORT || 3000;

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

app.use(express.static(path.join(__dirname, '../public')));
app.use(express.json());

app.use('/', lobbyRoutes);
app.use('/', electionRoutes);
app.use('/', legislativeRoutes);

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

app.listen(PORT, () => {
    console.log(`🚀 Server ready at: http://localhost:${PORT}`);
});