function filterUsers(role) {
  const rows = document.querySelectorAll("#user-table tbody tr");
  rows.forEach(row => {
    const userRole = row.children[1].textContent.trim();
    const status = row.children[2].textContent.trim();

    if (role === "all") {
      row.style.display = "";
    } else if (role === "Inactive") {
      row.style.display = status === "Inactive" ? "" : "none";
    } else {
      row.style.display = userRole === role ? "" : "none";
    }
  });
}
