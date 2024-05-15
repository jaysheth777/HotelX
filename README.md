## Project Overview: HotelX

### HotelX is an intelligent hotel recommendation system designed to provide users with highly relevant and personalized Airbnb listings. The primary purpose of HotelX is to simplify the search process for users looking for accommodations by leveraging advanced text embedding models and efficient search algorithms. This application is particularly useful for users planning vacations, business trips, or any other travel needs.

### Architecture
The architecture of HotelX is built on the following components:
- Streamlit Frontend: Provides an interactive user interface where users can enter their queries and receive recommendations. The frontend also includes predefined prompts to help users get started quickly.
- MongoDB Database: Stores the Airbnb listings and their corresponding text embeddings. MongoDB's vector search capabilities are utilized to efficiently retrieve the most relevant listings based on user queries.
- Together API: A powerful API for generating text embeddings. The model used is the togethercomputer/m2-bert-80M-8k-retrieval, which converts text into high-dimensional vectors that can be compared for similarity.
- Embedding Generation Script: A Jupyter Notebook (.ipynb) script that processes Airbnb listings, generates embeddings for the text fields, and stores these embeddings back in the MongoDB database.

### User Interaction Guide
- Initial Setup: Users must ensure they have their MongoDB connection URI and Together API key stored in a .env file.
- Launching the App: After installing all dependencies, Run the Streamlit application using the command `streamlit run app.py`. The interface will provide a header, an introduction, and options to enter a custom query or select a predefined prompt.
- Entering Queries: Users can either type in their specific requirements or choose from example prompts such as "Apartment with a great view near a coast or beach for 4 people."
- Viewing Results: Upon submitting a query, the application generates the text embeddings, performs a vector search in the MongoDB database, and displays the most relevant Airbnb listings. Each listing includes details like the name, summary, amenities, price, and a link to the Airbnb page.

### Screenshots:
![image](https://github.com/jaysheth777/HotelX/assets/131223228/3e856e31-564c-4498-a8ac-4d5ee5628878)
![image](https://github.com/jaysheth777/HotelX/assets/131223228/b875e13d-bcfd-4fc0-b8a9-d8e060c34202)
