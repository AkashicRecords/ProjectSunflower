# ProjectSunflower

ProjectSunflower is a FastAPI-based application designed to import, categorize, and store ChatGPT conversations. It uses specific phrases and trigger words to categorize chats and provides powerful search capabilities.

## Features

- Import and store ChatGPT conversations from web and mobile interfaces
- Automatically categorize chats based on content and specific phrases
- Search chats by content, category, and date range
- RESTful API for managing chat data
- Chrome extension for web-based ChatGPT interactions
- React Native mobile app for iOS and Android

## Categorization

The application uses two specific phrases for categorization:

1. "Let's start a new topic called {topic}": This phrase creates a new category with the specified topic.
2. "Let's talk about {topic}": This phrase either uses an existing category with the specified topic or creates a new one if it doesn't exist.

If neither phrase is found, the application uses trigger words to categorize the chat.

## API Endpoints

- `POST /import-chats/`: Import multiple chats
- `GET /chats/`: Retrieve all chats
- `GET /chats/{chat_id}`: Retrieve a specific chat
- `GET /search/`: Search chats by content, category, and date range
- `POST /categories/`: Create a new category
- `GET /categories/`: Retrieve all categories
- `POST /trigger-words/`: Create a new trigger word
- `GET /trigger-words/`: Retrieve all trigger words
- `DELETE /trigger-words/{trigger_word_id}`: Delete a trigger word
- `POST /export-conversation/`: Export a completed conversation for categorization and storage
- `POST /intercept-chat/`: Intercept and store a chat message

## Search Functionality

The search endpoint (`/search/`) allows for powerful querying of chats. You can search by:

- Content: Any text in the chat title or body
- Category: The name of the category
- Date range: Specify a start date and/or end date

Example search query:

## Future Enhancements

- Integration with Evernote
- Integration with Google Drive
- Integration with OneDrive

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).

## Mobile App

A React Native mobile app is available for intercepting ChatGPT conversations on Android and iOS devices. The app provides a WebView interface to ChatGPT and sends conversation data to the ProjectSunflower API for categorization and storage.

To set up the mobile app:

1. Navigate to the ChatGPTInterceptor directory
2. Install dependencies: `npm install`
3. For iOS, install pods: `cd ios && pod install && cd ..`
4. Run the app:
   - For Android: `npx react-native run-android`
   - For iOS: `npx react-native run-ios`

## Exporting Voice Conversations

After completing a voice conversation with ChatGPT, you can export the conversation for categorization and storage using the `/export-conversation/` endpoint. This allows for post-conversation processing and categorization based on the entire context of the conversation.

To export a conversation:

1. Transcribe the voice conversation to text (this step would be handled by your voice interface with ChatGPT).
2. Send a POST request to `/export-conversation/` with the following JSON body:
