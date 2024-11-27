# Turkish AI Teacher Chatbot

This project is designed to create an AI-powered chatbot for teaching Turkish Semantic Events and sentence structures. By employing the Socratic teaching method, the chatbot provides interactive learning experiences, guiding students through open-ended questions and responses. It integrates OpenAI, ChromaDB, and PDF processing to deliver dynamic and personalized educational content.
------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Project Overview

Project Overview
The chatbot facilitates Turkish language learning by:

-Teaching concepts like semantic events in sentences.
-Engaging users through Socratic questioning, encouraging critical thinking.
-Utilizing content extracted from PDF documents to enrich learning.
-Adapting dynamically to user responses and conversation contexts.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Key Features


- Socratic Method: Guides users through questions to enhance understanding.
- Interactive Dialogs: Adjusts based on user input, ensuring contextual relevance.
- PDF Integration: Extracts and organizes content from PDF files for educational purposes.
- ChromaDB: Stores and retrieves processed PDF data for quick access.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Installation

### Prerequisites
Ensure the following are installed:

- Python (version 3.8 or higher)
- Pip (Python package manager)

### Setup Steps
1. **Clone or Download the Repository:**
   Clone the repository to your local machine:
   git clone https://github.com/memreeozdemir/TurkishAITeacherChatbot.git

2. **Create a Virtual Environment: It's recommended to use a virtual environment to manage dependencies:**

python -m venv chatbot-env

3. **Activate the Virtual Environment: For Windows:**

chatbot-env\Scripts\activate

4. **Install Dependencies: Install required Python libraries:**

pip install -r requirements.txt

5. **Set up API Keys: Create a .env file and include your OpenAI API key:**

OPENAI_API_KEY=your_openai_api_key

------------------------------------------------------------------------------------------------------------------------------------------------------------------------


1. **PDF Document Processing**
Place educational PDFs in the data/ folder.

Process the PDFs into ChromaDB by running:

python pdf_to_chromadb.py


2. **Running the Application**
To start the chatbot interface:

streamlit run main.py
This will launch the application in your web browser.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------

## Code Components

1. **main.py**
- Manages the user interface and interactions.
- Starts the chatbot, processes user input, and generates responses.
- Implements Socratic dialog flow for topic teaching.
2. **pdf_to_chromadb.py**
- Extracts text from PDF documents.
- Stores the data in ChromaDB, enabling fast content retrieval.
3. **ChromaDB Integration**
- Provides functions to add, retrieve, and query document data.
- Ensures the chatbot can access relevant information during conversations.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------
## Code Explanation


This section provides an overview of the key components and their functionality in the project.

1. **main.py - Chatbot Driver**
This is the main entry point of the application. It:

Initializes the Chatbot: Sets up the environment and loads the necessary APIs (e.g., OpenAI API key from the .env file).
Starts User Interaction: Handles user input and chatbot responses in a conversational loop.
LangChain Integration: Utilizes LangChain to manage the flow and memory of conversations.
Streamlit Interface: Provides a web-based interface for interacting with the chatbot.
Functionality:

The chatbot listens for user input, processes it via OpenAI’s GPT model, and returns responses.
LangChain ensures the chatbot retains context, allowing for dynamic and relevant interactions.

2. **pdf_to_chromadb.py - PDF Processing**
This script is responsible for preparing the learning material by processing PDF files:

Reads PDF Content: Uses libraries like PyPDF2 to extract text from PDFs located in the data/ folder.
Stores Data in ChromaDB: Organizes and indexes the extracted content into a ChromaDB database.
Prepares Data for Queries: Enables efficient retrieval of relevant information during chatbot interactions.
Functionality:

After processing, the extracted information can be queried dynamically by the chatbot to provide additional insights to the user.

3. **LangChain Integration**
The project uses LangChain for:

Conversation Management: Maintains context across user interactions.
Enhanced Memory: Ensures the chatbot remembers key elements of the conversation.
Logical Flow: Structures the dialogue to align with teaching goals, such as explaining semantic events.
Key Features:

Retains context for multi-turn interactions.
Allows the chatbot to dynamically reference earlier parts of the conversation.

4. **ChromaDB Integration**
ChromaDB acts as a lightweight database for storing and retrieving educational materials:

Data Storage: Stores processed PDF content in an indexed format.
Querying Capability: Provides the chatbot with instant access to relevant information based on user questions.
Optimization: Ensures fast and accurate data retrieval, enhancing the user experience.
Functionality:

Queries are matched with the stored content to provide detailed answers or examples during lessons.

5. **Streamlit Integration**
The Streamlit library is used to create an interactive, web-based user interface:

Input Field: Allows users to type questions or interact with the chatbot.
Response Display: Shows the chatbot’s answers in a clean, readable format.
User-Friendly Interaction: Simplifies launching and using the chatbot, making it accessible to all users.
Functionality:

A Streamlit app runs the chatbot and provides an intuitive interface for interaction.
By combining these components, the chatbot achieves a seamless and intelligent learning experience, leveraging AI and database integration for enhanced functionality.

------------------------------------------------------------------------------------------------------------------------------------------------------------------------

**Possible Improvements**
While the chatbot provides a solid starting point for interactive language learning, there are several areas for potential improvement:

1. Multi-language Support:
Currently, the chatbot is designed specifically for Turkish, but adding support for other languages would allow it to be used for a wider range of learners.
2. Expand Knowledge Base:
Adding more PDFs and resources to ChromaDB will make the chatbot more comprehensive.
The chatbot could include more interactive features, like quizzes, examples, and exercises.
3. User Personalization:
Incorporating user progress tracking would allow the chatbot to tailor lessons based on the user's learning speed and performance.
4. Improved Feedback Mechanism:
The chatbot could offer more feedback on user input, pointing out mistakes and providing explanations.
5. Voice Interaction:
Allow users to interact with the chatbot using voice commands, adding accessibility for users who may prefer verbal communication.
6. Advanced Semantic Understanding:
Further improving the AI’s ability to understand and generate complex sentences and contextual meanings could enhance the learning experience.



