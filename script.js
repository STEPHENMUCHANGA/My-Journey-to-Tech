document.getElementById("recipeForm").addEventListener("submit", async (e) => {
  e.preventDefault();

  const ingredient = document.getElementById("ingredient").value;
  const servings = document.getElementById("servings").value;
  const prepTime = document.getElementById("prepTime").value;

  const response = await fetch("/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ingredient, servings, prepTime })
  });

  const data = await response.json();
  const output = document.getElementById("recipeOutput");

  if (data.recipe) {
    output.textContent = data.recipe;
  } else {
    output.textContent = "Error: " + data.error;
  }
});


  const response = await fetch("/generate", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ ingredient, servings, prepTime })
  });

  const data = await response.json();
  const output = document.getElementById("recipeOutput");

  if (data.recipe) {
    output.textContent = data.recipe;
  } else {
    output.textContent = "Error: " + data.error;
  }
  
