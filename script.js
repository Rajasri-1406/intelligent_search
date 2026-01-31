async function search() {
  const q = document.getElementById("q").value;
  const resultDiv = document.getElementById("result");

  if (!q) {
    alert("Please enter a query");
    return;
  }

  resultDiv.innerHTML = "<i>Searching...</i>";

  try {
    const res = await fetch(
      "http://127.0.0.1:8000/search?query=" + encodeURIComponent(q)
    );

    const data = await res.json();

    // 🔥 Format answer with line breaks
    const formattedAnswer = data.answer
      .replace(/\n/g, "<br>")
      .replace(/(\d+\.)/g, "<br><b>$1</b>");

    resultDiv.innerHTML = `
      <b>Query:</b> ${data.query}<br><br>
      <b>Papers Used:</b> ${data.papers_used}<br>
      <b>Citations:</b> ${data.citations}<br><br>
      ${formattedAnswer}
    `;

  } catch (err) {
    resultDiv.innerHTML = "<b>Error:</b> Unable to fetch results";
    console.error(err);
  }
}
