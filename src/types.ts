export type Identity = 'Authentic' | 'Fraudulent' | 'Trick-Meister' | null;
export type Policy = 'Authentic' | 'Fraudulent';

export interface Player {
    id: string;
    name: string;
    isReady: boolean;
    identity: Identity;
    isAlive: boolean;
}

export interface GameState {
    id?: string;
    name?: string;
    players: Player[];
    status: 'LOBBY' | 'ELECTION' | 'VOTING' | 'LEGISLATIVE' | 'POWER' | 'END';
    policyDeck: Policy[];
    discardPile: Policy[];
    traderIndex: number;
    nominatedSupplierId: string | null;
    votes: Record<string, boolean>;
    lastResult: string | null;
    hand: Policy[];
    handCount: number;
    scores: { authentic: number; fraudulent: number };
    boardType: 'small' | 'medium' | 'large';
    activePower: string | null;
    powerResult: string | null;
    originalTraderIndex: number | null;
    tempNextTrader: number | null;
    funds: number;
}

export interface LobbySummary {
    id: string;
    playerCount: number;
    status: GameState['status'];
}