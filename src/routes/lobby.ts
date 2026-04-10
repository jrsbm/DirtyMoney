import express from 'express';
import { Player } from '../types';
import { gameState } from '../state';
import { startGameLogic } from '../gameLogic';

const router = express.Router();

// Join route
router.post('/join', (req, res) => {
    const { name } = req.body;

    if (!name) {
        console.log("Join failed: No name provided");
        return res.status(400).json({ error: "Name is required" });
    }

    const cleanName = name.trim();
/*    const existingPlayer = gameState.players.find(
        p => p.name.toLowerCase() === cleanName.toLowerCase()
    );
    if (existingPlayer) {
        console.log(`${cleanName} reconnected.`);
        return res.json(existingPlayer); 
    }
*/
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
router.post('/ready', (req, res) => {
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

export { router as lobbyRoutes };