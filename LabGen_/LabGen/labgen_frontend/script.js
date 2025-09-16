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

    // Backend API base
    const API_BASE = "http://127.0.0.1:8000/api/v1";

    // Polling helper
    const pollStatus = async (taskId) => {
        while (true) {
            const res = await fetch(`${API_BASE}/status/${taskId}`);
            const data = await res.json();

            console.log("Polling status:", data);

            if (data.status === "COMPLETED") {
                return `${API_BASE}/video/${taskId}`;
            } else if (data.status === "FAILED") {
                throw new Error("Video generation failed on backend.");
            }

            statusText.textContent = `Current status: ${data.status}...`;
            await new Promise(r => setTimeout(r, 2000)); // wait 2 sec
        }
    };

    // Handle video generation
    const generateVideo = async () => {
        const protocolText = protocolInput.value.trim();
        if (!protocolText) {
            alert("Please paste your protocol before generating.");
            protocolInput.focus();
            return;
        }

        generateButton.disabled = true;

        inputSection.classList.add("hidden");
        statusSection.classList.remove("hidden");
        videoSection.classList.add("hidden");

        statusHeading.textContent = "Processing Request";
        statusText.textContent = "Sending protocol to backend...";

        try {
            // Send protocol to backend
            const response = await fetch(`${API_BASE}/generate`, {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ protocol: protocolText })
            });

            if (!response.ok) throw new Error(`Server error: ${response.status}`);
            const result = await response.json();

            console.log("Backend response:", result);

            statusText.textContent = "Task accepted. Waiting for video...";

            // 🔄 Poll status until video is ready
            const videoUrl = await pollStatus(result.task_id);

            statusSection.classList.add("hidden");
            videoSection.classList.remove("hidden");
            videoPlaceholder.classList.add("hidden");

            const existingVideo = document.getElementById("video-player");
            if (existingVideo) existingVideo.remove();

            // Insert video element with backend response URL
            const videoElement = document.createElement("video");
            videoElement.id = "video-player";
            videoElement.controls = true;
            videoElement.classList.add("w-full", "h-full");
            videoElement.src = videoUrl;
            videoPlayerContainer.appendChild(videoElement);

        } catch (err) {
            console.error("Error generating video:", err);
            statusHeading.textContent = "Error!";
            statusText.textContent = "Failed to generate video. Please try again.";
            generateButton.disabled = false;
        }
    };

    // Reset UI back to input mode
    const resetView = () => {
        videoSection.classList.add("hidden");
        statusSection.classList.add("hidden");
        inputSection.classList.remove("hidden");

        protocolInput.value = '';
        generateButton.disabled = false;

        statusHeading.textContent = "Processing Request";
        statusText.textContent = "Initializing generation...";
    };

    generateButton.addEventListener('click', generateVideo);
    resetButton.addEventListener('click', resetView);
});
