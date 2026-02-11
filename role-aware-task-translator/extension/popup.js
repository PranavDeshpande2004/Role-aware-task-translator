document.getElementById("translate").onclick = async () => {
  const output = document.getElementById("output");
  const role = document.getElementById("role").value.trim();

  // ---- Step 1: Validate role ----
  if (!role) {
    output.innerText = "⚠️ Please enter a role.";
    return;
  }

  // ---- Step 2: Get active tab ----
  const [tab] = await chrome.tabs.query({
    active: true,
    currentWindow: true
  });

  if (!tab.url || !tab.url.includes("/browse/")) {
    output.innerText = "⚠️ Please open a Jira issue page.";
    return;
  }

  // ---- Step 3: Extract Jira issue key ----
  const issueKey = tab.url.split("/browse/")[1].split("?")[0];

  output.innerText = "⏳ Translating task...";

  try {
    // ---- Step 4: Call backend ----
    const res = await fetch("http://localhost:8000/translate-task", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        issue_key: issueKey,
        role: role
      })
    });

    if (!res.ok) {
      throw new Error("Backend error");
    }

    const data = await res.json();

    // ---- Step 5: Confidence indicator ----
    let confidenceIcon = "🟢";
    let confidenceNote = "";

    if (data.confidence_level === "MEDIUM") {
      confidenceIcon = "🟡";
      confidenceNote = "\n⚠️ Result may be incomplete.";
    }

    if (data.confidence_level === "LOW") {
      confidenceIcon = "🔴";
      confidenceNote = "\n⚠️ Low confidence — manual review recommended.";
    }

    // ---- Step 6: Render output ----
    output.innerText =
`${confidenceIcon} Role: ${data.role}

Confidence: ${data.confidence}% (${data.confidence_level})
${confidenceNote}

Generated Tasks:
${data.detailed_tasks}`;

  } catch (err) {
    output.innerText = "❌ Failed to translate task. Check backend.";
    console.error(err);
  }
};