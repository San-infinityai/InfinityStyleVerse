
document.addEventListener("DOMContentLoaded", function () {
  const feedbackForms = document.querySelectorAll(".form-container");

  feedbackForms.forEach(form => {
    form.addEventListener("submit", function (e) {
      e.preventDefault();

      const formData = new FormData(form);
      fetch("/submit_feedback", {
        method: "POST",
        body: formData
      })
      .then(response => {
        if (response.ok) {
          alert("Thank you for your feedback!");
          form.reset();
        } else {
          alert("Failed to submit feedback. Please try again.");
        }
      })
      .catch(error => {
        console.error("Error submitting feedback:", error);
        alert("An error occurred.");
      });
    });
  });
});
