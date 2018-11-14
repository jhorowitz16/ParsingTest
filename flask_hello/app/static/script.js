function checkAnswer(guess) {
  initStorage();
  var answer = document.getElementById("answer").innerText;
  console.log(guess);
  console.log(answer);
  if (answer === guess) {
    console.log("correct");
    storeIncrement('correct');
    storeIncrement('total');
  } else {
    console.log("wrong");
    storeIncrement('total');
  }
  setScoreText();
  makeAnswerVisible();
  disableButtons();
}

function next() {
  makeAnswerInvisible();
  enableButtons();
  location.reload();
}


/* ============================================= */
/* ================== HELPERS ================== */
/* ============================================= */

function setScoreText() {
  const correct = localStorage.getItem('correct');
  const total = localStorage.getItem('total');
  const text = correct + " / " + total;
  document.getElementById("score").innerText = text;
}

function makeAnswerVisible() {
  document.getElementById("answer").style.display = "block";
}

function makeAnswerInvisible() {
  document.getElementById("answer").style.display = "none";
}

function disableButtons() {
  document.getElementById("button--J").disabled = true;
  document.getElementById("button--W").disabled = true;

  document.getElementById("button--next").disabled = false;
}

function enableButtons() {
  document.getElementById("button--J").disabled = false;
  document.getElementById("button--W").disabled = false;

  document.getElementById("button--next").disabled = true;
}

function storeGet(key) {
  const cached = localStorage.getItem(key);
  return (cached === null) ? null : parseInt(cached);
}

function storeIncrement(key) {
  const val = storeGet(key);
  if (val) {
    localStorage.setItem(key, val + 1)
  } else {
    localStorage.setItem(key, 1)
  }
}

function resetLocalStorage() {
    localStorage.setItem('correct', 0);
    localStorage.setItem('total', 0);
}

function initStorage() {
  const cachedCorrect = storeGet('correct');
  const cachedTotal = storeGet('total');

  if (cachedCorrect === null) {
    localStorage.setItem('correct', 0);
  }
  if (cachedTotal === null) {
    localStorage.setItem('total', 0);
  }
}

/* ============================================= */
/* =================== PREP ==================== */
/* ============================================= */

initStorage();

window.onload = setScoreText;
