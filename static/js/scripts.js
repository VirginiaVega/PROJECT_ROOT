/*!
* Start Bootstrap - Modern Business v5.0.7 (https://startbootstrap.com/template-overviews/modern-business)
* Copyright 2013-2023 Start Bootstrap
* Licensed under MIT (https://github.com/StartBootstrap/startbootstrap-modern-business/blob/master/LICENSE)
*/
// This file is intentionally blank
// Use this file to add JavaScript to your project


// body Dark Mode 
// document.addEventListener("DOMContentLoaded", function() {
//     const body = document.body;
//     const toggleBtn = document.getElementById("darkModeToggle");    

//         // Por defecto: oscuro, a menos que el usuario haya guardado "light"
//     if (localStorage.getItem("dark-mode") === "light") {
//         body.classList.remove("dark-mode");
//     } else {
//         body.classList.add("dark-mode");
//     }

//     if (toggleBtn) {
//         function updateButtonText() {
//             toggleBtn.textContent = body.classList.contains("dark-mode")
//                 ? "☀️ Modo claro"
//                 : "🌙 Modo oscuro";
//         }
//         updateButtonText();

//         toggleBtn.addEventListener("click", function() {
//             body.classList.toggle("dark-mode");
//             if (body.classList.contains("dark-mode")) {
//                 localStorage.setItem("dark-mode", "dark");
//             } else {
//                 localStorage.setItem("dark-mode", "light");
//             }
//             updateButtonText();
//         });
//     }
// });



// postForm
document.addEventListener('DOMContentLoaded', () => {
    const imageInput = document.getElementById('imageInput');
    const canvas = document.getElementById('previewCanvas');
    const ctx = canvas.getContext('2d');
    const croppedImageInput = document.getElementById('croppedImageInput');
    const cropWidth = 50;
    const cropHeight = 100;

    function drawCroppedImage(src) {
        const img = new Image();
        img.onload = function () {
            canvas.width = cropWidth;
            canvas.height = cropHeight;

            canvas.style.width = '';
            canvas.style.height = '';

            const scale = Math.max(
                cropWidth / img.width,
                cropHeight / img.height
            );

            const scaledWidth = img.width * scale;
            const scaledHeight = img.height * scale;

            const x = (cropWidth - scaledWidth) / 2;
            const y = (cropHeight - scaledHeight) / 2;

            ctx.clearRect(0, 0, cropWidth, cropHeight);
            ctx.drawImage(img, x, y, scaledWidth, scaledHeight);

            croppedImageInput.value = canvas.toDataURL('image/png');
        };
        img.src = src;
    }

    // Vista previa imagen Crear
    imageInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (!file) return;
        const reader = new FileReader();
        reader.onload = (event) => drawCroppedImage(event.target.result);
        reader.readAsDataURL(file);
    });


        // Cargar imagen existente Editar
    const existingImageInput = document.getElementById('existingImage');
    if (existingImageInput && existingImageInput.value) {
        console.log("Imagen existente:", existingImageInput.value); // debug
        drawCroppedImage(existingImageInput.value);
    }

});

