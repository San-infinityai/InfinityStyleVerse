function showSection(sectionId) {
  const sections = document.querySelectorAll(".content-section");
  sections.forEach(sec => sec.style.display = "none");

  const target = document.getElementById(sectionId);
  if (target) target.style.display = "block";
}
document.getElementById("upload-form").addEventListener("submit", function (e) {
  e.preventDefault();

  const title = document.getElementById("title").value.trim();
  const description = document.getElementById("description").value.trim();
  const image = document.getElementById("image").files[0];
  const category = document.getElementById("category").value;

  if (!title || !description || !image || !category) {
    alert("Please fill out all fields correctly.");
    return;
  }

  // Simulate upload success
  alert("Design uploaded successfully!");

  // You can later replace this with fetch POST to backend
  this.reset();
});
