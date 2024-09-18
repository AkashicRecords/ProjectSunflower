import React, { useState, useRef } from 'react';
import { WebView } from 'react-native-webview';
import { Button, View, Text, StyleSheet } from 'react-native';

const API_URL = 'http://your-actual-api-url:8000';

const ChatGPTWebView = () => {
  const [conversation, setConversation] = useState('');
  const webViewRef = useRef(null);

  const injectedJavaScript = `
    (function() {
      function captureConversation() {
        const messages = document.querySelectorAll('.markdown');
        return Array.from(messages).map(m => m.textContent).join('\n\n');
      }

      window.captureAndSendConversation = function() {
        const content = captureConversation();
        window.ReactNativeWebView.postMessage(JSON.stringify({
          type: 'export',
          content: content
        }));
      }
    })();
  `;

  const handleMessage = (event) => {
    const data = JSON.parse(event.nativeEvent.data);
    if (data.type === 'export') {
      setConversation(data.content);
      exportConversation(data.content);
    }
  };

  const exportConversation = (content) => {
    fetch(`${API_URL}/export-conversation/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        title: "ChatGPT Conversation",
        content: content
      }),
    })
    .then(response => response.json())
    .then(data => console.log('Conversation exported successfully:', data))
    .catch((error) => console.error('Error exporting conversation:', error));
  };

  return (
    <View style={styles.container}>
      <WebView
        ref={webViewRef}
        source={{ uri: 'https://chat.openai.com/' }}
        injectedJavaScript={injectedJavaScript}
        onMessage={handleMessage}
        style={styles.webview}
      />
      <View style={styles.buttonContainer}>
        <Button
          title="Export Conversation"
          onPress={() => {
            webViewRef.current.injectJavaScript('window.captureAndSendConversation();');
          }}
          color="#4CAF50"
        />
      </View>
      {conversation ? <Text style={styles.exportedText}>Conversation exported!</Text> : null}
    </View>
  );

  const styles = StyleSheet.create({
    container: {
      flex: 1,
    },
    webview: {
      flex: 1,
    },
    buttonContainer: {
      padding: 10,
      backgroundColor: '#f0f0f0',
    },
    exportedText: {
      padding: 10,
      backgroundColor: '#4CAF50',
      color: 'white',
      textAlign: 'center',
    },
  });
};

export default ChatGPTWebView;