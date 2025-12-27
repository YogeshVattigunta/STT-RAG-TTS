const statusEl = document.getElementById("status");
const youEl = document.getElementById("you");
const assistantEl = document.getElementById("assistant");
const robot = document.querySelector("model-viewer");

let polling = false;

function applyAnimation(status) {
  robot.animationName = "Idle Animation";

  statusEl.className = "";
  statusEl.classList.add(status);

  if (status === "listening") {
    robot.timeScale = 1.1;
  } else if (status === "thinking") {
    robot.timeScale = 0.6;
  } else if (status === "speaking") {
    robot.timeScale = 1.4;
  } else {
    robot.timeScale = 1.0;
  }
}

async function pollStatus() {
  if (!polling) return;

  try {
    const res = await fetch("http://localhost:8000/status");
    const data = await res.json();

    statusEl.innerText = data.status;
    applyAnimation(data.status);

    if (data.you_said) youEl.innerText = "You: " + data.you_said;
    if (data.assistant) assistantEl.innerText = "Agent: " + data.assistant;

  } catch (e) {
    console.error("Polling error:", e);
  }

  setTimeout(pollStatus, 700);
}

document.getElementById("start").onclick = async () => {
  statusEl.innerText = "listening";
  youEl.innerText = "";
  assistantEl.innerText = "";
  polling = true;

  await fetch("http://localhost:8000/record/start", { method: "POST" });
  pollStatus();
};

document.getElementById("stop").onclick = async () => {
  statusEl.innerText = "processing";
  await fetch("http://localhost:8000/record/stop", { method: "POST" });
};
