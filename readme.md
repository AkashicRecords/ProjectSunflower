# ProjectSunflower

ProjectSunflower is a FastAPI-based application designed to download and store ChatGPT conversations. It uses trigger words to create new subject files and appends topics to existing subject files.

## Features

- Download and store ChatGPT conversations
- Create new subject files based on trigger words
- Append topics to existing subject files
- RESTful API for managing chat data

## Technologies Used

- Python 3.9
- FastAPI
- SQLAlchemy
- Docker

## Getting Started

### Prerequisites

- Docker
- Git

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/AkashicRecords/ProjectSunflower.git
   ```

2. Navigate to the project directory:
   ```
   cd ProjectSunflower
   ```

3. Build the Docker image:
   ```
   docker build -t projectsunflower .
   ```

4. Run the Docker container:
   ```
   docker run -p 8000:8000 projectsunflower
   ```

The application should now be running and accessible at `http://localhost:8000`.

## API Endpoints

- `POST /chats/`: Create a new chat
- `GET /chats/`: Retrieve all chats
- `GET /chats/{chat_id}`: Retrieve a specific chat

## Future Enhancements

- Integration with Evernote
- Integration with Google Drive
- Integration with OneDrive

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the [MIT License](LICENSE).
