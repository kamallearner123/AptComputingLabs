
document.addEventListener("DOMContentLoaded", () => {
    // Initialize EmailJS
    // emailjs.init("85WnQ5VWJEXQ5HsYnV84K"); // Replace with your actual user ID

    const uploadForm = document.getElementById("upload-form");
    const galleryImages = document.getElementById("gallery-images");
    const carouselImages = document.querySelector(".carousel-images");
    const carouselItems = document.querySelectorAll(".carousel-item");
    const totalItems = carouselItems.length;
    let currentIndex = 0;

    // Function to show the current image
    function showImage(index) {
        const offset = -index * 100; // Calculate offset
        carouselImages.style.transform = `translateX(${offset}%)`; // Move carousel
    }

    // Next button functionality
    document.getElementById("nextBtn").addEventListener("click", () => {
        currentIndex = (currentIndex + 1) % totalItems; // Increment index
        showImage(currentIndex); // Show new image
    });

    // Previous button functionality
    document.getElementById("prevBtn").addEventListener("click", () => {
        currentIndex = (currentIndex - 1 + totalItems) % totalItems; // Decrement index
        showImage(currentIndex); // Show new image
    });

    // Handle the upload form submission
    uploadForm.addEventListener("submit", (e) => {
        e.preventDefault();
        const fileInput = document.getElementById("upload");
        const files = fileInput.files;

        if (files.length > 0) {
            const reader = new FileReader();
            reader.onload = function (event) {
                const newImage = document.createElement("div");
                newImage.classList.add("carousel-item");
                newImage.innerHTML = `
                    <img src="${event.target.result}" alt="Uploaded Image">
                    <div class="carousel-description">Uploaded Image</div>
                `;
                carouselImages.appendChild(newImage);
                // Update total items
                totalItems++;
            };
            reader.readAsDataURL(files[0]);
        }
    });


});