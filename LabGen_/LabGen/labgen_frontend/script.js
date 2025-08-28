
document.addEventListener('DOMContentLoaded', () => {
    lucide.createIcons();

    const generateButton = document.getElementById('generate-button');
    const resetButton = document.getElementById('reset-button');
    const protocolInput = document.getElementById('protocol-input');

    const inputSection = document.getElementById('protocol-input-section');
    const statusSection = document.getElementById('status-section');
    const videoSection = document.getElementById('video-section');

    const statusHeading = document.getElementById('status-heading');
    const statusText = document.getElementById('status-text');
    const videoPlayerContainer = document.getElementById('video-player-container');
    const videoPlaceholder = document.getElementById('video-placeholder');

    const statuses = [
        'Parsing protocol...',
        'Identifying lab equipment and reagents...',
        'Generating storyboard from steps...',
        'Creating 3D laboratory environment...',
        'Rendering video frames (1/2)...',
        'Rendering video frames (2/2)...',
        'Synthesizing procedural narration...',
        'Finalizing video...'
    ];

    const generateVideo = () => {
        const protocolText = protocolInput.value;
        if (protocolText.trim() === '') {
            alert('Please paste your protocol before generating.');
            protocolInput.focus();
            return;
        }


        generateButton.disabled = true;


        inputSection.classList.add('hidden');
        statusSection.classList.remove('hidden');
        videoSection.classList.add('hidden');


        let statusIndex = 0;
        statusHeading.textContent = "Processing Request";
        statusText.textContent = "Initializing generation...";

        const statusInterval = setInterval(() => {
            if (statusIndex < statuses.length) {
                statusText.textContent = statuses[statusIndex];
                statusIndex++;
            } else {
                clearInterval(statusInterval);
                statusHeading.textContent = "Generation Complete!";
                statusText.textContent = "Your video is now ready.";
                
                setTimeout(() => {

                    statusSection.classList.add('hidden');
                    videoSection.classList.remove('hidden');
                    videoPlaceholder.classList.remove('hidden');

                    const existingVideo = document.getElementById('video-player');
                    if (existingVideo) {
                        existingVideo.remove();
                    }
                }, 1500);
            }
        }, 1200);
    };
    
    const resetView = () => {
        videoSection.classList.add('hidden');
        statusSection.classList.add('hidden');
        inputSection.classList.remove('hidden');
        
        protocolInput.value = '';
        generateButton.disabled = false;
        
        statusHeading.textContent = "Processing Request";
        statusText.textContent = "Initializing generation...";
    };

    generateButton.addEventListener('click', generateVideo);
    resetButton.addEventListener('click', resetView);
});
