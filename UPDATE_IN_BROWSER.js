// PASTE THIS ENTIRE CODE INTO YOUR BROWSER CONSOLE ON THE APP PAGE
// Then press Enter to execute

console.log("🏈 Setting Final Score: SEA 29 - NE 13");
console.log("=".repeat(60));

// Get Firebase database reference (already initialized in your app)
const dbRef = firebase.database().ref();

// Final scores
const finalScores = {
    SEA: [3, 9, 7, 10],  // Q1: 3, Q2: 9, Q3: 7, Q4: 10
    NE: [0, 0, 0, 13]    // Q1: 0, Q2: 0, Q3: 0, Q4: 13
};

const finalMeta = {
    status: "STATUS_FINAL",
    period: 4,
    clock: "0:00",
    detail: "Final",
    seaTotal: 29,
    neTotal: 13
};

// Update the database
Promise.all([
    dbRef.child('scores').set(finalScores),
    dbRef.child('gameMeta').set(finalMeta)
]).then(() => {
    console.log("✅ FINAL SCORES UPDATED SUCCESSFULLY!");
    console.log("Q1: SEA 3 - NE 0");
    console.log("Q2: SEA 9 - NE 0");
    console.log("Q3: SEA 7 - NE 0");
    console.log("Q4: SEA 10 - NE 13");
    console.log("FINAL: SEA 29 - NE 13");
    console.log("=".repeat(60));
    console.log("🎉 Page will refresh in 2 seconds...");
    setTimeout(() => location.reload(), 2000);
}).catch(error => {
    console.error("❌ Error updating scores:", error);
});
