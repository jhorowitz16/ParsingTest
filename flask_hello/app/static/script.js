document.correct = 0;
document.total = 0;


function checkAnswer(guess) {
  var answer = document.getElementById("answer").innerText;
  console.log(guess);
  console.log(answer);
  if (answer === guess) {
    console.log("correct");
    document.correct += 1;
    document.total += 1;
  } else {
    console.log("wrong");
    document.total += 1;
  }
  setScoreText();
  makeAnswerVisible();
  disableButtons();
}

function next() {
  makeAnswerInvisible();
  enableButtons();
}


/* ============================================= */
/* ================== HELPERS ================== */
/* ============================================= */

function setScoreText() {
  const text = document.correct + " / " + document.total;
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
}

function enableButtons() {
  document.getElementById("button--J").disabled = false;
  document.getElementById("button--W").disabled = false;
}
