// // Make function globally accessible
// window.getJiraTask = () => {
//   try {
//     // Jira issue title
//     const titleEl = document.querySelector(
//       '[data-testid="issue.views.issue-base.foundation.summary.heading"]'
//     );

//     // Jira issue description
//     const descEl = document.querySelector(
//       '[data-testid="issue.views.field.rich-text.description"]'
//     );

//     const title = titleEl ? titleEl.innerText.trim() : "";
//     const desc = descEl ? descEl.innerText.trim() : "";

//     return {
//       title: title,
//       desc: desc
//     };
//   } catch (err) {
//     console.error("Error extracting Jira task:", err);
//     return {
//       title: "",
//       desc: ""
//     };
//   }
// };
