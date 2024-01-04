document.addEventListener('DOMContentLoaded', function () {
    const cameraGrid = document.getElementById('camera-grid');

    fetch('/cameras')
        .then(response => response.json())
        .then(cameras => {
            cameras.forEach(camera => {
                const cameraDiv = document.createElement('div');
                cameraDiv.className = 'col-md-6 camera';
                cameraDiv.innerHTML = `
                    <h5>${camera.name}</h5>
                    <img src="/stream/${camera.id}" />
                `;
                cameraGrid.appendChild(cameraDiv);
            });
        })
        .catch(error => {
            console.error('Error fetching camera data:', error);
            cameraGrid.innerHTML = `<p>Error loading cameras.</p>`;
        });
});
