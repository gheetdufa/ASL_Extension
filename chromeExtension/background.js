chrome.runtime.onInstalled.addListener(() => {
    console.log("Extension Installed");
});

// Listen for messages from the Flask server
const eventSource = new EventSource("http://127.0.0.1:5000/listen"); // Correct endpoint
eventSource.onopen = () => {
    console.log("Connection to server opened.");
};
eventSource.onerror = (err) => {
    console.error("EventSource failed:", err);
};
eventSource.onmessage = (event) => {
    const data = JSON.parse(event.data);
    const character = data.character;
    console.log('Received character:', character); // Debugging line
    chrome.tabs.query({active: true, currentWindow: true}, (tabs) => {
        if (tabs.length > 0) {
            chrome.tabs.sendMessage(tabs[0].id, {character: character}, (response) => {
                if (chrome.runtime.lastError) {
                    console.error("Error sending message to content script:", chrome.runtime.lastError);
                } else {
                    console.log("Message sent to content script:", response);
                }
            });
        } else {
            console.log("No active tabs found.");
        }
    });
};
