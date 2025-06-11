// Show different dashboard sections
function showSection(sectionId) {
  const sections = document.querySelectorAll(".content-section");
  sections.forEach(sec => sec.style.display = "none");

  const target = document.getElementById(sectionId);
  if (target) target.style.display = "block";
}

// Handle Upload Form Submission
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

  // Show Bootstrap success modal
  const modal = new bootstrap.Modal(document.getElementById('uploadModal'));
  modal.show();

  this.reset();
});

// Fetch and display products
function fetchProducts() {
  fetch("http://localhost:5000/api/products")
    .then(res => res.json())
    .then(data => {
      displayProducts(data);
    })
    .catch(err => {
      console.error("Error loading products:", err);
    });
}

// Display products with feedback form
function displayProducts(data) {
  const container = document.getElementById("product-container");
  container.innerHTML = "";

  data.forEach(product => {
    const ratingStars = "⭐".repeat(Math.floor(product.rating || 0)) + "☆".repeat(5 - Math.floor(product.rating || 0));
    container.innerHTML += `
  <div class="product-card">
    <img src="${product.image_url}" alt="${product.title}">
    <h4>${product.title}</h4>
    <p>${product.category}</p>
    
    <!-- Feedback Display -->
    <p>Rating: ${"⭐".repeat(product.rating || 0)}</p>
    <p>${product.comment || "No feedback yet."}</p>

    <!-- Feedback Form -->
    <form onsubmit="submitFeedback(event, ${product.id})" class="feedback-form">
      <label>Rate:</label><br>
      <input type="radio" name="rating-${product.id}" value="5">5
      <input type="radio" name="rating-${product.id}" value="4">4
      <input type="radio" name="rating-${product.id}" value="3">3
      <input type="radio" name="rating-${product.id}" value="2">2
      <input type="radio" name="rating-${product.id}" value="1">1
      <br>
      <textarea name="comment-${product.id}" placeholder="Write your comment here..." required></textarea><br>
      <button type="submit">Submit Feedback</button>
    </form>
  </div>`;

  });
}

// Filter products by category
function filterByCategory(category) {
  fetch("http://localhost:5000/api/products")
    .then(res => res.json())
    .then(data => {
      const filtered = category === "All"
        ? data
        : data.filter(p => p.category === category);
      displayProducts(filtered);
    })
    .catch(err => {
      console.error("Filter failed:", err);
    });
}

// Submit product feedback
function submitFeedback(e, productId) {
  e.preventDefault();
  const form = e.target;
  const rating = form.querySelector(`input[name="rating-${productId}"]:checked`)?.value;
  const comment = form.querySelector(`textarea[name="comment-${productId}"]`).value;

  if (!rating || !comment.trim()) {
    alert("Please provide a rating and comment.");
    return;
  }

  fetch("http://localhost:5000/api/feedback", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      product_id: productId,
      stars: parseInt(rating),
      comment: comment.trim()
    })
  })
    .then(res => res.json())
    .then(data => {
      alert("Feedback submitted!");
      form.reset();
    })
    .catch(err => {
      console.error("Error submitting feedback:", err);
      alert("Failed to submit feedback.");
    });
}

// Initial call to load products on page load
fetchProducts();

function fetchRecommendations(userId) {
  fetch(`http://localhost:5000/api/recommendations/${userId}`)
    .then(res => res.json())
    .then(data => {
      const container = document.getElementById("recommend-container");
      container.innerHTML = "";

      if (!data.length) {
        container.innerHTML = "<p>No recommendations available right now.</p>";
        return;
      }

      data.forEach(product => {
        container.innerHTML += `
          <div class="product-card">
            <img src="${product.image_url}" alt="${product.title}">
            <h4>${product.title}</h4>
            <p>${product.category}</p>
          </div>
        `;
      });
    })
    .catch(err => {
      console.error("Error fetching recommendations:", err);
    });
}

document.addEventListener("DOMContentLoaded", () => {
  const userId = 101; // Replace this with the actual logged-in user ID
  fetchRecommendations(userId);
});

// Notification
function showNotification(message) {
  const bar = document.getElementById("notification-bar");
  bar.textContent = message;
  bar.style.display = "block";
  bar.style.animation = "fadeIn 0.5s ease-in-out";

  // Hide after 4 seconds
  setTimeout(() => {
    bar.style.animation = "fadeOut 0.5s ease-in-out";
    setTimeout(() => {
      bar.style.display = "none";
    }, 500); // Match fadeOut duration
  }, 4000);
}
