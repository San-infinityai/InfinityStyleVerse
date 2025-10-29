document.addEventListener("DOMContentLoaded", function () {
  // Product Filtering
  const filterButtons = document.querySelectorAll(".filter-buttons button");
  const productCards = document.querySelectorAll(".product-card");

  filterButtons.forEach(button => {
    button.addEventListener("click", () => {
      const filter = button.getAttribute("data-filter");
      productCards.forEach(card => {
        const tags = card.getAttribute("data-tags");
        if (tags && tags.includes(filter)) {
          card.style.display = "block";
        } else {
          card.style.display = "none";
        }
      });
    });
  });

  // Section Switching
  window.showSection = function (sectionId) {
    const sections = document.querySelectorAll(".content-section");
    sections.forEach(section => {
      section.style.display = "none";
    });

    const targetSection = document.getElementById(sectionId);
    if (targetSection) {
      targetSection.style.display = "block";
    }
  };

  // Show default section on load
  showSection("home");
});
