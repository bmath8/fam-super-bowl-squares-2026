const https = require('https');

const DEFAULT = {
    grid: Array.from({ length: 10 }, () => Array(10).fill(null)),
    colNums: null, rowNums: null, isLocked: false,
    scores: { SEA: [null, null, null, null], NE: [null, null, null, null] },
    pool: { pricePerSquare: 5, payoutSplit: [25, 25, 25, 25], payoutPreset: "even", propBuyIn: 2 },
    settings: { maxPerPlayer: 0, showHeatMap: false },
    feed: [], playerMeta: {}, props: {}, propAnswers: {},
    feedReactions: {}, squareReactions: {},
    hostPin: "", zellePhone: "", zelleEmail: "", darkMode: true,
    trades: [], chat: [], payments: {}, propBuyIns: {}, paidPlayers: {},
    priorityMode: false, admins: [], auditLog: [],
    gameState: "PRE",
    tiebreaker: { question: "Total combined points in the game?", answers: {} },
};

const rooms = ["MAIN", "GAMETIME", "OFFICIAL", "TEST"];

function resetRoom(room) {
    return new Promise((resolve, reject) => {
        const data = JSON.stringify(DEFAULT);
        const url = `https://super-bowl-squares-fam-2026-default-rtdb.firebaseio.com/rooms/${room}.json`;

        const req = https.request(url, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
                'Content-Length': data.length
            }
        }, (res) => {
            console.log(`Room ${room} Reset Status: ${res.statusCode}`);
            resolve();
        });

        req.on('error', (e) => {
            console.error(`Error resetting ${room}: ${e.message}`);
            reject(e);
        });

        req.write(data);
        req.end();
    });
}

async function run() {
    for (const r of rooms) {
        await resetRoom(r);
    }
    console.log("All rooms reset successfully!");
}

run();
