const nextBtns = document.querySelectorAll(".next-btn");
const prevBtns = document.querySelectorAll(".prev-btn");
const formSteps = document.querySelectorAll(".form-step");
const progressSteps = document.querySelectorAll(".progress-step");
const progress = document.getElementById("progress");

let formStepsNum = 0;

nextBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    if (formStepsNum < formSteps.length - 1) {
      formStepsNum++;
      updateFormSteps();
      updateProgressbar();
    }
  });
});

prevBtns.forEach(btn => {
  btn.addEventListener("click", () => {
    if (formStepsNum > 0) {
      formStepsNum--;
      updateFormSteps();
      updateProgressbar();
    }
  });
});

function updateFormSteps() {
  formSteps.forEach(step => step.classList.remove("active"));
  formSteps[formStepsNum].classList.add("active");

  if (formStepsNum === 2) updateSummary();
}

function updateProgressbar() {
  progressSteps.forEach((step, idx) => {
    if (idx <= formStepsNum) step.classList.add("active");
    else step.classList.remove("active");
  });

  const actives = document.querySelectorAll(".progress-step.active");
  progress.style.width = ((actives.length - 1) / (progressSteps.length - 1)) * 100 + "%";
}

function updateSummary() {
  const personal = document.getElementById("summary-personal");
  const professional = document.getElementById("summary-professional");

  const first = document.querySelector("input[name='first_name']").value;
  const last = document.querySelector("input[name='last_name']").value;
  const email = document.querySelector("input[name='email']").value;
  const phone = document.querySelector("input[name='phone']").value;

  const qualification = document.querySelector("textarea[name='qualification']").value;
  const experience = document.querySelector("select[name='experience']").value;
  const subjects = document.querySelector("textarea[name='subjects']").value;
  const rate = document.querySelector("input[name='horuly_rate']").value;

  personal.innerHTML = `
    <li><strong>Name:</strong> ${first} ${last}</li>
    <li><strong>Email:</strong> ${email}</li>
    <li><strong>Phone:</strong> ${phone}</li>
  `;

  professional.innerHTML = `
    <li><strong>Qualification:</strong> ${qualification}</li>
    <li><strong>Experience:</strong> ${experience}</li>
    <li><strong>Subjects:</strong> ${subjects}</li>
    <li><strong>Hourly Rate:</strong> $${rate}</li>
  `;
}
