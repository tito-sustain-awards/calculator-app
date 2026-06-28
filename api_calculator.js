const API_URL = "http://localhost:5000/api/calc";

const apiCalculate = async ({ action, left, right, value }) => {
  const response = await fetch(API_URL, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ action, left, right, value }),
  });

  if (!response.ok) {
    const payload = await response.json();
    throw new Error(payload.error || "API error");
  }

  const payload = await response.json();
  return payload.result;
};

export default apiCalculate;
