// Function to send temperature to backend and get prediction
function predictSales() {
  let temperatureInput = document.getElementById("temperature");
  let temperature = temperatureInput.value.trim();

  // Validate input
  if (temperature === "") {
    alert("⚠️ Please enter a temperature!");
    return;
  }

  // Disable input & button while loading
  temperatureInput.disabled = true;
  document.getElementById("predict-btn").innerHTML = "⏳ Predicting...";
  document.getElementById("predict-btn").disabled = true;

  fetch("https://first-ml-project-7z8r.onrender.com", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ temperature: parseFloat(temperature) }),
  })
    .then((response) => response.json())
    .then((data) => {
      // Update UI with results and keep emojis
      document.getElementById(
        "result"
      ).innerHTML = `🍦 <b>Predicted Sales:</b> ${data.predicted_sales} units`;
      document.getElementById(
        "accuracy"
      ).innerHTML = `📊 <b>Model Accuracy (R² Score):</b> ${data.r2_score}`;

      // Restore button text and re-enable input
      document.getElementById("predict-btn").innerHTML = "🔮 Predict Sales";
      document.getElementById("predict-btn").disabled = false;
      temperatureInput.disabled = false;
    })
    .catch((error) => {
      console.error("Error:", error);
      alert("❌ An error occurred while predicting sales. Please try again.");

      // Restore button text and re-enable input on error
      document.getElementById("predict-btn").innerHTML = "🔮 Predict Sales";
      document.getElementById("predict-btn").disabled = false;
      temperatureInput.disabled = false;
    });
}
