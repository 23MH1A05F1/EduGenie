const $ = (id) => document.getElementById(id);

function toggleTheme(){
  document.body.classList.toggle("light");
}

function showTool(id, button){
  document.querySelectorAll(".tool-panel").forEach(x=>x.classList.remove("active"));
  document.querySelectorAll(".tab").forEach(x=>x.classList.remove("active"));
  $(id).classList.add("active");
  button.classList.add("active");
}

async function postJSON(url, data){
  const response = await fetch(url, {
    method:"POST",
    headers:{"Content-Type":"application/json"},
    body:JSON.stringify(data)
  });
  const result = await response.json();
  if(!response.ok) throw new Error(result.detail || "Request failed");
  return result;
}

async function askQuestion(){
  const input = $("questionInput");
  const question = input.value.trim();
  if(!question) return;

  addMessage(question, "user");
  input.value = "";
  addMessage("Thinking...", "bot");

  try{
    const data = await postJSON("/api/chat", {question, mode:"simple"});
    const messages = $("chatMessages");
    messages.lastElementChild.textContent = data.answer;
  }catch(e){
    $("chatMessages").lastElementChild.textContent = "Error: " + e.message;
  }
}

function addMessage(text, type){
  const div = document.createElement("div");
  div.className = "message " + type;
  div.textContent = text;
  $("chatMessages").appendChild(div);
  $("chatMessages").scrollTop = $("chatMessages").scrollHeight;
}

async function generateQuiz(){
  const result = $("quizResult");
  result.innerHTML = "<p class='muted'>Generating...</p>";
  try{
    const data = await postJSON("/api/quiz", {
      topic:$("quizTopic").value,
      difficulty:$("quizDifficulty").value,
      count:Number($("quizCount").value)
    });
    result.innerHTML = "";
    data.questions.forEach((q,i)=>{
      const card = document.createElement("div");
      card.className = "quiz-card";
      card.innerHTML = `<h4>Q${i+1}. ${escapeHtml(q.question)}</h4>` +
        q.options.map((o,j)=>`<label><input type="radio" name="q${i}" value="${escapeAttr(o)}"> ${escapeHtml(o)}</label>`).join("");
      card.dataset.answer = q.answer;
      card.dataset.explanation = q.explanation;
      result.appendChild(card);
    });
    const button = document.createElement("button");
    button.className = "primary quiz-submit";
    button.textContent = "Check Score";
    button.onclick = checkQuiz;
    result.appendChild(button);
  }catch(e){result.innerHTML = `<p>Error: ${escapeHtml(e.message)}</p>`;}
}

function checkQuiz(){
  const cards = document.querySelectorAll(".quiz-card");
  let score=0;
  cards.forEach((card,i)=>{
    const selected = document.querySelector(`input[name="q${i}"]:checked`);
    if(selected && selected.value === card.dataset.answer) score++;
  });
  const box=document.createElement("div");
  box.className="result";
  box.textContent=`Your Score: ${score}/${cards.length}\n\n${score === cards.length ? "Excellent! You answered everything correctly." : "Review the questions you missed and practice again."}`;
  $("quizResult").appendChild(box);
}

async function summarizeText(){
  const text=$("summaryText").value.trim();
  if(text.length<20){$("summaryResult").textContent="Please enter at least 20 characters.";return;}
  $("summaryResult").textContent="Creating summary...";
  try{
    const data=await postJSON("/api/summarize",{text});
    $("summaryResult").textContent=data.summary;
  }catch(e){$("summaryResult").textContent="Error: "+e.message;}
}

async function generateRoadmap(){
  const box=$("roadmapResult");
  box.innerHTML="<p class='muted'>Building roadmap...</p>";
  try{
    const data=await postJSON("/api/roadmap",{
      topic:$("roadmapTopic").value,
      level:$("roadmapLevel").value,
      weeks:Number($("roadmapWeeks").value)
    });
    box.innerHTML=data.roadmap.map(w=>`
      <div class="road-card">
        <h3>Week ${w.week}: ${escapeHtml(w.title)}</h3>
        <p><b>Topics:</b> ${w.topics.map(escapeHtml).join(" • ")}</p>
        <p><b>Practice:</b> ${escapeHtml(w.practice)}</p>
        <p><b>Milestone:</b> ${escapeHtml(w.milestone)}</p>
      </div>`).join("");
  }catch(e){box.innerHTML=`<p>Error: ${escapeHtml(e.message)}</p>`;}
}

function escapeHtml(s){
  return String(s).replace(/[&<>"']/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;","'":"&#039;"}[c]));
}
function escapeAttr(s){return String(s).replace(/"/g,"&quot;").replace(/'/g,"&#039;");}

$("questionInput").addEventListener("keydown", e=>{
  if(e.key==="Enter") askQuestion();
});
