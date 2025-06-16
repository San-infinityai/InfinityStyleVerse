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
