function registerUser(event) {
  event.preventDefault();

  const firstName = document.getElementById("firstName").value.trim();
  const lastName = document.getElementById("lastName").value.trim();
  const address = document.getElementById("address").value.trim();
  const gender = document.getElementById("gender").value;
  const dob = document.getElementById("dob").value;
  const aadhaar = document.getElementById("aadhaar").value.trim();
  const voterKey = document.getElementById("newVoterKey").value.trim();

  const age = calculateAge(dob);
  if (age < 18) {
    alert("You must be at least 18 years old to register.");
    return;
  }

  const voterId = generateVoterId(firstName, lastName, dob);

  const user = {
    firstName,
    lastName,
    address,
    gender,
    dob,
    age,
    aadhaar,
    voterId,
    voterKey
  };

  const users = JSON.parse(localStorage.getItem("users")) || [];
  users.push(user);
  localStorage.setItem("users", JSON.stringify(users));

  document.getElementById("signUpBox").style.display = "none";
  document.getElementById("successMessage").style.display = "block";
  document.getElementById("generatedVoterId").textContent = voterId;
}

function calculateAge(dob) {
  const birthDate = new Date(dob);
  const currentDate = new Date();
  let age = currentDate.getFullYear() - birthDate.getFullYear();
  const m = currentDate.getMonth() - birthDate.getMonth();
  if (m < 0 || (m === 0 && currentDate.getDate() < birthDate.getDate())) {
    age--;
  }
  return age;
}

function generateVoterId(firstName, lastName, dob) {
  const datePart = dob.split("-").reverse().join("");
  return `${firstName[0].toUpperCase()}${lastName[0].toUpperCase()}${datePart}`;
}

function loginUser(event) {
  event.preventDefault();

  const voterId = document.getElementById("voterId").value.trim().toUpperCase();
  const voterKey = document.getElementById("voterKey").value;

  const users = JSON.parse(localStorage.getItem("users")) || [];
  const user = users.find(u => u.voterId === voterId && u.voterKey === voterKey);

  if (user) {
    localStorage.setItem("loggedInUser", voterId);
    window.location.href = "dashboard.html";
  } else {
    alert("Invalid Voter ID or Voter Key.");
  }
}

function logout() {
  localStorage.removeItem("loggedInUser");
  window.location.href = "index.html";
}
