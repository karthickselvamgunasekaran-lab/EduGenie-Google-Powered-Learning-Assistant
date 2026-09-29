const $ = (id) => document.getElementById(id);

async function request(url, options = {}) {
  const response = await fetch(url, {
    headers: { "Content-Type": "application/json", ...(options.headers || {}) },
    ...options,
  });
  const data = await response.json().catch(() => ({}));
  if (!response.ok) {
    throw new Error(data.detail || data.error || `Request failed (${response.status})`);
  }
  return data;
}

function setLoading(element, loading) {
  element.classList.toggle("loading", loading);
  if (loading) element.textContent = "";
}

function setError(element, error) {
  element.classList.remove("loading");
  element.className = "result error";
  element.textContent = error.message || String(error);
}

async function runAction(action) {
  const map = {
    qna: ["qna-input", "qna-result"],
    explain: ["explain-input", "explain-result"],
    summarize: ["summary-input", "summary-result"],
    quiz: ["quiz-input", "quiz-result"],
    learn: ["learn-input", "learn-result"],
  };

  const [inputId, resultId] = map[action];
  const input = $(inputId);
  const result = $(resultId);
  const value = input.value.trim();

  if (!value) {
    result.className = "result error";
    result.textContent = "Please enter some content first.";
    return;
  }

  setLoading(result, true);

  try {
    let data;
    if (action === "qna") {
      data = await request(`/api/qna?question=${encodeURIComponent(value)}`);
      result.textContent = data.answer;
    } else if (action === "explain") {
      data = await request("/api/explain", {
        method: "POST",
        body: JSON.stringify({ topic: value }),
      });
      result.textContent = data.explanation;
    } else if (action === "summarize") {
      data = await request("/api/summarize", {
        method: "POST",
        body: JSON.stringify({ text: value }),
      });
      result.textContent = data.summary;
    } else if (action === "quiz") {
      data = await request("/api/quiz", {
        method: "POST",
        body: JSON.stringify({ text: value }),
      });
      renderQuiz(result, data.quiz);
    } else if (action === "learn") {
      data = await request(`/api/learn/recommendations?topic=${encodeURIComponent(value)}`);
      result.textContent = data.recommendation;
    }
  } catch (error) {
    setError(result, error);
  }
}

function renderQuiz(result, questions) {
  result.classList.remove("loading", "error");
  result.innerHTML = "";

  questions.forEach((item, index) => {
    const box = document.createElement("div");
    box.className = "quiz-question";

    const title = document.createElement("strong");
    title.textContent = `Q${index + 1}. ${item.question}`;
    box.appendChild(title);

    item.options.forEach((option) => {
      const label = document.createElement("label");
      const radio = document.createElement("input");
      radio.type = "radio";
      radio.name = `q${index}`;
      radio.value = option;
      label.appendChild(radio);
      label.append(` ${option}`);
      box.appendChild(label);
    });

    const check = document.createElement("button");
    check.textContent = "Check Answer";
    check.type = "button";
    check.addEventListener("click", () => {
      const selected = box.querySelector("input:checked");
      if (!selected) return;
      box.querySelectorAll("label").forEach((l) => l.style.fontWeight = "400");
      if (selected.value === item.answer) {
        box.insertAdjacentHTML("beforeend", `<div><strong>Correct!</strong></div>`);
      } else {
        box.insertAdjacentHTML("beforeend", `<div class="error">Not quite. Review the concept and try again.</div>`);
      }
    });
    box.appendChild(check);

    result.appendChild(box);
  });
}

document.querySelectorAll("button[data-action]").forEach((button) => {
  button.addEventListener("click", async () => {
    button.disabled = true;
    try {
      await runAction(button.dataset.action);
    } finally {
      button.disabled = false;
    }
  });
});

async function checkHealth() {
  try {
    const data = await request("/api/health");
    $("status").textContent = data.demo_mode
      ? "API online · demo mode"
      : `API online · ${data.ai_provider}`;
  } catch {
    $("status").textContent = "API unavailable";
  }
}

checkHealth();
