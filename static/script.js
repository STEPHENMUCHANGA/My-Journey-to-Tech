document.getElementById("tripForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const destination = document.getElementById("destination").value;
  const days = document.getElementById("days").value;
  const budget = document.getElementById("budget").value;

  const response = await fetch("/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ destination, days, budget })
  });

  const data = await response.json();
  const output = document.getElementById("itineraryOutput");

  if (data.itinerary) {
    output.textContent = data.itinerary;
  } else {
    output.textContent = "Error: " + data.error;
  }
});
