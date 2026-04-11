import express from 'express';
import type { Request, Response } from 'express';
import { gameState } from '../state';
import { adjustFunds, rotateTrader, triggerPowerLogic, checkWinConditions, processBankruptcy } from '../gameLogic';

const router = express.Router();

// Discard route
router.post('/discard', (req: Request, res: Response) => {
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
router.post('/use-power', (req: Request, res: Response) => {
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

router.post('/end-power', (req: Request, res: Response) => {
    const { playerId } = req.body;
    const isTrader = gameState.players[gameState.traderIndex].id === playerId;

    if (!isTrader) return res.status(403).json({ error: "Forbidden" });

    gameState.powerResult = null;
    gameState.activePower = null;
    // Fraudulent-bankruptcy-fraudulent power chain
    if (gameState.funds <= 0) {
        processBankruptcy();
        if (gameState.status === 'POWER') {
            return res.json({ message: "Power resolved, but Bankruptcy triggered a new Power!" });
        }
    }

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

export { router as legislativeRoutes };