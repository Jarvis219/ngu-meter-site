// "Try it" quiz on the landing page: a few gotchas from the app, played right here.
// Data comes from the #demo-data JSON written by scripts/build_pages.py. No network, no storage.
(() => {
  const section = document.querySelector(".demo");
  const blob = document.getElementById("demo-data");
  if (!section || !blob) return;
  const data = JSON.parse(blob.textContent);
  const text = data.text;
  const card = section.querySelector(".demo-card");
  section.classList.add("is-live");

  let round = [], index = 0, wrong = 0;

  const shuffled = (list) => {
    const out = list.slice();
    for (let i = out.length - 1; i > 0; i--) {
      const j = Math.floor(Math.random() * (i + 1));
      [out[i], out[j]] = [out[j], out[i]];
    }
    return out;
  };
  const pick = (list) => list[Math.floor(Math.random() * list.length)];
  const fill = (template, values) => template.replace(/\{(\w+)\}/g, (_, key) => values[key]);
  const el = (tag, className, content) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (content !== undefined) node.textContent = content;
    return node;
  };

  function start() {
    round = shuffled(data.questions).slice(0, data.perRound);
    index = 0;
    wrong = 0;
    showQuestion();
  }

  function showQuestion() {
    const q = round[index];
    card.replaceChildren();
    const top = el("div", "demo-top");
    top.append(el("span", "demo-progress", fill(text.progress, { n: index + 1, total: round.length })), el("span", "demo-flames", "🔥🔥🔥"));
    const bar = el("div", "demo-bar");
    bar.style.setProperty("--done", `${(index / round.length) * 100}%`);
    const prompt = el("p", "demo-q", q.prompt);
    prompt.tabIndex = -1;
    const answers = el("div", "demo-answers");
    for (const answer of shuffled(q.answers)) {
      const button = el("button", "demo-answer", answer.text);
      button.type = "button";
      button.addEventListener("click", () => choose(q, answer, button, answers));
      answers.append(button);
    }
    card.append(top, bar, prompt, answers);
    if (index > 0) prompt.focus({ preventScroll: true });
  }

  function choose(q, answer, button, answers) {
    if (!answer.correct) wrong += 1;
    for (const b of answers.children) {
      b.disabled = true;
      const isCorrect = q.answers.find((a) => a.text === b.textContent).correct;
      if (isCorrect) b.classList.add("is-correct");
      else if (b === button) b.classList.add("is-wrong");
      else b.classList.add("is-dim");
    }
    const feedback = el("div", "demo-feedback");
    feedback.append(el("p", "demo-reaction", pick(answer.correct ? data.reactions.correct : data.reactions.wrong)));
    const why = el("div", "demo-why");
    why.append(el("b", null, `💡 ${text.why}`), el("p", null, q.why));
    feedback.append(why);
    const last = index === round.length - 1;
    const next = el("button", "button demo-next", last ? text.finish : text.next);
    next.type = "button";
    next.addEventListener("click", () => {
      index += 1;
      if (last) showResult();
      else showQuestion();
    });
    feedback.append(next);
    card.append(feedback);
    next.focus({ preventScroll: true });
    if (feedback.getBoundingClientRect().bottom > window.innerHeight) {
      feedback.scrollIntoView({ behavior: "smooth", block: "nearest" });
    }
  }

  function showResult() {
    const score = Math.round((wrong / round.length) * 100);
    const tier = data.tiers.find((t) => score <= t.max) || data.tiers[data.tiers.length - 1];
    card.replaceChildren();
    const result = el("div", "demo-result");
    const img = el("img");
    img.src = tier.image;
    img.alt = "";
    img.width = 150;
    img.height = 150;
    const heading = el("p", "demo-score-label", text.score);
    const value = el("p", "demo-score", String(score));
    value.tabIndex = -1;
    result.append(img, heading, value, el("p", "demo-tier", tier.title),
      el("p", "demo-count", fill(text.wrong, { w: wrong, t: round.length })), el("p", "demo-more", text.more));
    const again = el("button", "button secondary demo-again", text.again);
    again.type = "button";
    again.addEventListener("click", start);
    result.append(again);
    card.append(result);
    value.focus({ preventScroll: true });
  }

  start();
})();
