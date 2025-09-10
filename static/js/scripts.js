// postForm
document.addEventListener('DOMContentLoaded', () => {
    const imageInput = document.getElementById('imageInput');
    const canvas = document.getElementById('previewCanvas');
    const ctx = canvas.getContext('2d');
    const croppedImageInput = document.getElementById('croppedImageInput');
    const cropWidth = 300;
    const cropHeight = 400;

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

