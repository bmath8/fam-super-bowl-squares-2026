// Final Score Setter for Firebase
// Run with: node set-final-score.js

const firebase = require('firebase/compat/app');
require('firebase/compat/database');

const firebaseConfig = {
    apiKey: "AIzaSyAEEWLXshtNMrf317dgD5cDpDmETLDhueo",
    authDomain: "super-bowl-squares-fam-2026.firebaseapp.com",
    databaseURL: "https://super-bowl-squares-fam-2026-default-rtdb.firebaseio.com",
    projectId: "super-bowl-squares-fam-2026",
    storageBucket: "super-bowl-squares-fam-2026.firebasestorage.app",
    messagingSenderId: "393390824832",
    appId: "1:393390824832:web:d06bca315fd0a991bb7565"
};

firebase.initializeApp(firebaseConfig);
const db = firebase.database();

// FINAL SCORE: SEA 29 - NE 13
// You'll need to break this down by quarter
// Example breakdown (adjust based on actual quarter scores):
const finalScores = {
    SEA: [3, 6, 13, 7],  // Q1: 3, Q2: 6, Q3: 13, Q4: 7 = 29 total
    NE: [0, 0, 7, 6]     // Q1: 0, Q2: 0, Q3: 7, Q4: 6 = 13 total
};

const gameMeta = {
    status: "STATUS_FINAL",
    period: 4,
    clock: "0:00",
    detail: "Final",
    seaTotal: 29,
    neTotal: 13
};

async function setFinalScore() {
    try {
        console.log("Setting final score: SEA 29 - NE 13");

        // Replace 'YOUR_POOL_ID' with your actual pool ID
        const poolRef = db.ref('pools/YOUR_POOL_ID');

        await poolRef.update({
            scores: finalScores,
            gameMeta: gameMeta
        });

        console.log("✅ Final score set successfully!");
        console.log("Scores:", finalScores);
        console.log("Game Meta:", gameMeta);

        process.exit(0);
    } catch (error) {
        console.error("❌ Error setting score:", error);
        process.exit(1);
    }
}

setFinalScore();
