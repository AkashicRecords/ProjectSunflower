import React from 'react';
import { SafeAreaView } from 'react-native';
import ChatGPTWebView from './ChatGPTWebView';

const App = () => {
  return (
    <SafeAreaView style={{ flex: 1 }}>
      <ChatGPTWebView />
    </SafeAreaView>
  );
};

export default App;