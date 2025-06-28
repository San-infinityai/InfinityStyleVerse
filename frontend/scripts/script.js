//add product
const fileInput = document.getElementById('product-images');
const previewContainer = document.getElementById('preview-container');

fileInput.addEventListener('change', function () {
  previewContainer.innerHTML = '';
  const files = this.files;

  Array.from(files).forEach(file => {
    const reader = new FileReader();
    reader.onload = function (e) {
      const img = document.createElement('img');
      img.src = e.target.result;
      previewContainer.appendChild(img);
    };
    reader.readAsDataURL(file);
  });
});


//onboarding

window.addEventListener('load', () => {
  const modal = new bootstrap.Modal(document.getElementById('welcomeModal'));
  modal.show();
});

function goToHome() {
  window.location.href = "index.html";
}

//profile

 function showTab(tabId, event) {
      document.querySelectorAll('.tab').forEach(tab => tab.classList.remove('active'));
      document.querySelectorAll('.tab-content').forEach(content => content.classList.remove('active'));
      document.getElementById(tabId).classList.add('active');
      event.target.classList.add('active');
    }

    function saveCard(button) {
      const card = button.closest('.card');
      card.classList.add('saved');
      button.disabled = true;
      button.textContent = '✔';
      setTimeout(() => {
        card.classList.remove('saved');
        button.disabled = false;
        button.textContent = '💾';
      }, 2000);
    }
