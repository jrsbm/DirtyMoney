import express from 'express';
import { Player } from '../types';
import { lobbies } from '../server';
import { startGameLogic } from '../gameLogic';

const router = express.Router();

// Join route
router.post('/join', (req, res) => {
    const { name, lobbyId } = req.body;

    if(!lobbyId || !lobbies[lobbyId]) {
        return res.status(404).json({ error: "Lobby not found" });
    }

    const gameState = lobbies[lobbyId];

    if (!name) {
        console.log("Join failed: No name provided");
        return res.status(400).json({ error: "Name is required" });
    }

    const cleanName = name.trim();
    const existingPlayer = gameState.players.find(
        p => p.name.toLowerCase() === cleanName.toLowerCase()
    );
    if (existingPlayer) {
        console.log(`${cleanName} reconnected to ${lobbyId}.`);
        return res.json(existingPlayer); 
    }

    const nameExists = gameState.players.some(
        p => p.name.toLowerCase() === cleanName.toLowerCase()
    );
    if (nameExists) {
        return res.status(400).json({ error: "That name is already taken!" });
    }

    if (gameState.players.length >= 10) {
        return res.status(403).json({ error: "Lobby is full" });
    }

    if (gameState.status !== 'LOBBY') {
        return res.status(403).json({ error: "Lobby already in progress" });
    }

    const newPlayer: Player = {
        id: Math.random().toString(36).substring(2, 9),
        name: name,
        isReady: false,
        identity: null,
        isAlive: true,
    };
    gameState.players.push(newPlayer);
    console.log(`${name} joined lobby ${lobbyId}.Total players: ${gameState.players.length}`);
    res.json(newPlayer);
});

// Ready route
router.post('/ready', (req, res) => {
    const { playerId, lobbyId } = req.body;

    if (!lobbyId || !lobbies[lobbyId]) {
        return res.status(404).json({ error: "Lobby not found" });
    }

    const gameState = lobbies[lobbyId];
    const player = gameState.players.find(p => p.id === playerId);

    if (!player) return res.status(404).json({ error: "Player not found" });
    if (gameState.status !== 'LOBBY') return res.status(400).json({ error: "Game already started" });

    // Toggle state
    player.isReady = !player.isReady;

    // Check if everyone is ready AND there are at least 5 players
    const allReady = gameState.players.length >= 5 && gameState.players.every(p => p.isReady);

    if (allReady) {
        startGameLogic(gameState); 
        console.log(`[${lobbyId}] Everyone ready. Starting game...`);
    }

    res.json({ isReady: player.isReady, gameStarted: allReady });
});

export { router as lobbyRoutes };