console.log('Content script loaded');

chrome.runtime.onMessage.addListener((request, sender, sendResponse) => {
    const character = request.character;
    console.log('Received character in content script:', character);
    
    const activeElement = document.activeElement;
    console.log('Active element:', activeElement.tagName);
    
    if (activeElement.tagName === 'TEXTAREA' || activeElement.tagName === 'INPUT') {
        // Append the character to the value
        activeElement.value += character;
        
        // Create and dispatch input event
        const event = new Event('input', { bubbles: true });
        activeElement.dispatchEvent(event);
        
        console.log('Character appended to input field and input event dispatched.');
    } else {
        console.log('Active element is not a text input or textarea.');
    }
    
    sendResponse({status: 'done'});
});
