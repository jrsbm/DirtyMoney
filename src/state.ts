import { GameState } from './types';

export const createInitialState= (): GameState => {
    return {
        players: [],
        status: 'LOBBY',
        policyDeck: [],
        discardPile: [],
        traderIndex: 0,
        nominatedSupplierId: null,
        votes: {},
        lastResult: null,
        hand: [],
        handCount: 0,
        scores: { authentic: 0, fraudulent: 0 },
        boardType: 'small',
        activePower: null,
        powerResult: null,
        originalTraderIndex: null,
        tempNextTrader: null,
        funds: 3
    };
}