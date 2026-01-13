document.getElementById("translate").onclick = async () => {
  const role = document.getElementById("role").value.trim();

  if (!role) {
    document.getElementById("output").innerText =
      " Please enter a role.";
    return;
  }

  const [tab] = await chrome.tabs.query({
    active: true,
    currentWindow: true
  });

  if (!tab.url || !tab.url.includes("/browse/")) {
    document.getElementById("output").innerText =
      " Open a Jira issue page.";
    return;
  }

  // ✅ Extract issue key from URL
  // Example: https://xyz.atlassian.net/browse/DEV-123
  const issueKey = tab.url.split("/browse/")[1].split("?")[0];

  const res = await fetch("http://localhost:8000/translate-task", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      issue_key: issueKey,
      role: role
    })
  });

  const data = await res.json();

  document.getElementById("output").innerText =
    JSON.stringify(data, null, 2);
};
