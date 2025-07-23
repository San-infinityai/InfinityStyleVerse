
document.addEventListener("DOMContentLoaded", function () {
  fetch("/api/recommendations")
    .then(response => response.json())
    .then(data => {
      const recommendationGrid = document.getElementById("recommendationGrid");
      recommendationGrid.innerHTML = "";

      data.forEach(product => {
        const card = document.createElement("div");
        card.className = "product-card";
        card.setAttribute("data-tags", product.tags.join(","));

        card.innerHTML = `
          <img src="\${product.image_url}" alt="\${product.name}" />
          <h4>\${product.name}</h4>
          <p>\${product.price}</p>
          <p>\${product.description}</p>
          <form class="form-container" method="POST" action="/submit_feedback">
            <label for="rating">Rate this product:</label>
            <select name="rating">
              <option value="5">★★★★★</option>
              <option value="4">★★★★</option>
              <option value="3">★★★</option>
              <option value="2">★★</option>
              <option value="1">★</option>
            </select>
            <label for="comment">Your feedback:</label>
            <textarea name="comment" rows="3" placeholder="Write your thoughts..."></textarea>
            <input type="hidden" name="product_id" value="\${product.id}" />
            <button type="submit">Submit Feedback</button>
          </form>
        `;
        recommendationGrid.appendChild(card);
      });
    })
    .catch(error => {
      console.error("Error fetching recommendations:", error);
    });
});
