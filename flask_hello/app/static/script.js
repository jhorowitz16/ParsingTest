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
}


function setScoreText() {
  const text = document.correct + " / " + document.total;
  document.getElementById("score").innerText = text;
}
