document.addEventListener('DOMContentLoaded', function () {
    const selectElement = document.getElementById('talle-select');
    if (selectElement) { // Asegúrate de que el elemento existe
        selectElement.addEventListener('change', function () {
            const selectedValue = this.value;
            if (selectedValue) {
                window.location.href = selectedValue; // Redirige a la URL seleccionada
            }
        });
    }
});
