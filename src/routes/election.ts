import express from 'express';
import type { Request, Response } from 'express';
import { gameState } from '../state';
import { adjustFunds, rotateTrader } from '../gameLogic';

const router = express.Router();

// Nominate route
router.post('/nominate', (req: Request, res: Response) => {
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
router.post('/vote', (req: Request, res: Response) => {
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
    if (Object.keys(gameState.votes).length === livingPlayers.length){
        const yesVotes = Object.values(gameState.votes).filter(v => v === true).length;
        const playersAlive = livingPlayers.length;

        if (yesVotes > playersAlive / 2) {
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

export { router as electionRoutes };