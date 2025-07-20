// document.getElementById('upload-form').addEventListener('submit', function(event) {
//     event.preventDefault();
//     const fileInput = document.getElementById('upload');
//     const file = fileInput.files[0];
//     if (file) {
//         const reader = new FileReader();
//         reader.onload = function(e) {
//             const img = document.createElement('img');
//             img.src = e.target.result;
//             img.alt = file.name;
//             img.style.maxWidth = '200px';
//             img.style.margin = '10px';
//             document.getElementById('gallery-images').appendChild(img);
//         };
//         reader.readAsDataURL(file);
//     }
// });

document.addEventListener("DOMContentLoaded", () => {
    const uploadForm = document.getElementById("upload-form");
    const galleryImages = document.getElementById("gallery-images");
    const currentImage = document.getElementById("current-image");

    let imageIndex = 0;
    let images = [];

    // Function to update the displayed image
    function showImage() {
        if (images.length > 0) {
            currentImage.src = images[imageIndex];
            imageIndex = (imageIndex + 1) % images.length;
        }
    }

    // Change image every 3 seconds
    setInterval(showImage, 3000);

    // Handle the upload form submission
    uploadForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const fileInput = document.getElementById("upload");
        const files = fileInput.files;

        if (files.length > 0) {
            const reader = new FileReader();
            reader.onload = function (event) {
                const newImage = document.createElement("img");
                newImage.src = event.target.result;
                galleryImages.appendChild(newImage);

                // Add the image to the slideshow array
                images.push(newImage.src);

                // If this is the first image, start showing it
                if (images.length === 1) {
                    showImage();
                }
            };
            reader.readAsDataURL(files[0]);
        }
    });
});
