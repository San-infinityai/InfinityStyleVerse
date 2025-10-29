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

function editProduct(id) {
  alert(`Editing product/user with ID ${id}`);
  // Future: open a form/modal to edit user or product
}

function deleteProduct(id) {
  if (!confirm("Are you sure you want to delete this item?")) return;

  fetch(`http://localhost:5000/api/products/${id}`, {
    method: "DELETE"
  })
    .then(res => {
      if (res.ok) {
        alert("Deleted successfully");
        location.reload();
      } else {
        alert("Failed to delete");
      }
    })
    .catch(err => {
      console.error("Delete error:", err);
    });
}
