const API_URL = 'http://your-actual-api-url:8000';

function sendToProjectSunflower(message) {
  fetch(`${API_URL}/export-conversation/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      title: "ChatGPT Conversation",
      content: message
    }),
  })
  .then(response => response.json())
  .then(data => console.log('Success:', data))
  .catch((error) => console.error('Error:', error));
}

function captureConversation() {
  const messages = document.querySelectorAll('.markdown');
  return Array.from(messages).map(m => m.textContent).join('\n\n');
}

// Add a button to the ChatGPT interface
function addExportButton() {
  const button = document.createElement('button');
  button.textContent = 'Export to ProjectSunflower';
  button.style.position = 'fixed';
  button.style.bottom = '20px';
  button.style.right = '20px';
  button.style.zIndex = '9999';
  button.style.padding = '10px 20px';
  button.style.backgroundColor = '#4CAF50';
  button.style.color = 'white';
  button.style.border = 'none';
  button.style.borderRadius = '5px';
  button.style.cursor = 'pointer';
  button.addEventListener('click', () => {
    const conversation = captureConversation();
    sendToProjectSunflower(conversation);
    button.textContent = 'Exported!';
    setTimeout(() => {
      button.textContent = 'Export to ProjectSunflower';
    }, 2000);
  });
  document.body.appendChild(button);
}

// Run when the page loads
window.addEventListener('load', addExportButton);