let gameSeq = [];
let userSeq = [];
let buttons = ["btn1", "btn2", "btn3", "btn4"];
let start = false;
let level = 0;
let h2 = document.querySelector(".level");

let gameFlash = function (btn) {
    btn.classList.add("flash");
    setTimeout(function () {
        btn.classList.remove("flash");
    }, 250);
};

let userFlash = function (btn) {
    btn.classList.add("userFlash");
    setTimeout(function () {
        btn.classList.remove("userFlash");
    }, 250);
};

let levelUp = function () {
    level++;
    h2.innerText = `Level ${level}`;
    let i = Math.floor(Math.random() * 4);  
    let id = buttons[i];
    let btn = document.querySelector(`#${id}`);
    gameSeq.push(id);
    gameFlash(btn);
    userSeq = [];  
};

let userPress = function () {
    let btn = this;
    userFlash(btn);
    let userColor = btn.getAttribute("id");
    userSeq.push(userColor);
    checkColor(); 
};

let allBtns = document.querySelectorAll(".btn");
for (let btn of allBtns) {
    btn.addEventListener("click", userPress);
}

document.addEventListener("keydown", function () {
    if (!start) {
        start = true;
        levelUp();
    }
});

// Function to check if the user's sequence matches the game's sequence
let checkColor = function() {
    let index = userSeq.length - 1;  // Get the index of the last pressed button
    if (userSeq[index] === gameSeq[index]) {
        // If the user pressed the correct color
        if (userSeq.length === gameSeq.length) {
            setTimeout(levelUp,1000); // Move to the next level after a short delay
        }
    } else {
        // Game over logic
        h2.innerText = `Game Over! You reached Level ${level}. Your highest Score ${level}.Press any key to start.`;
        resetGame();  // Reset the game for a new round
    }
};

// Reset the game after game over
let resetGame = function() {
    gameSeq = [];
    userSeq = [];
    level = 0;
    start = false;
};
