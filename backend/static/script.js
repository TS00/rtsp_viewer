document.addEventListener('DOMContentLoaded', function () {
    // List of camera IDs, you can dynamically generate this list
    const cameraIds = ['Yard', 'Backdoor', 'Frontdoor']; // Add more camera IDs as needed

    const cameraGrid = document.getElementById('camera-grid');

    cameraIds.forEach(id => {
        const cameraDiv = document.createElement('div');
        cameraDiv.className = 'col-md-6 camera';
        cameraDiv.innerHTML = `
            <h5>${id}</h5>
            <img src="http://127.0.0.1:5000/video_feed/${id}" />
        `;
        cameraGrid.appendChild(cameraDiv);
    });
});
