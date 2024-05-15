import os
import pymongo
import together
import streamlit as st
from typing import List
from dotenv import load_dotenv
from llama_index.embeddings.together import TogetherEmbedding

# Load environment variables
load_dotenv()

# Streamlit configuration
st.set_page_config(
    page_title="HotelX, Your smart goto Hotel assistant 😎", 
    page_icon="🏨", 
    layout="centered", 
    initial_sidebar_state="expanded"
)

# Retrieve environment variables
# For Local
# MONGO_CONN_URI = os.getenv('MONGO_CONN_URI')
# TOGETHER_API_KEY = os.getenv('TOGETHER_API_KEY')

# For streamlit cloud
MONGO_CONN_URI = st.secrets['MONGO_CONN_URI']
TOGETHER_API_KEY = st.secrets['TOGETHER_API_KEY']

# Check for necessary environment variables
if not (MONGO_CONN_URI and TOGETHER_API_KEY):
    st.error("Please create a .env file and store MongoDB URL and Together AI API key.")
    st.stop()

# Initialize MongoDB client
client = pymongo.MongoClient(MONGO_CONN_URI)
collection = client['sample_airbnb']['listingsAndReviews']

VECTOR_DATABASE_FIELD_NAME = 'embedding_together_m2-bert-8k-retrieval'
embed_model = TogetherEmbedding(
    model_name="togethercomputer/m2-bert-80M-8k-retrieval", 
    api_key=TOGETHER_API_KEY
)

keys_to_extract = [
    "name", "summary", "space", "description", "neighborhood_overview", 
    "notes", "transit", "access", "interaction", "house_rules", 
    "property_type", "room_type", "bed_type", "minimum_nights", 
    "maximum_nights", "accommodates", "bedrooms", "beds"
]

# Streamlit interface
example_prompts = [
    "Apartment with a great view near a coast or beach for 4 people",
    "Luxury penthouse with a city skyline view, suitable for a weekend stay for 2 people",
    "Cozy cabin in a quiet neighborhood, perfect for a family of 5 with easy access to public transit",
    "Charming cottage by the lake, ideal for a romantic getaway, min. stay of 3 nights"
]

with st.sidebar:
    st.title("About HotelX")
    st.write("""
    **HotelX** is your smart go-to hotel assistant that helps you find the perfect stay for your vacation, job, or any other need.
    Using advanced embedding models, we provide highly accurate and relevant Airbnb listings based on your queries.
    """)
    st.subheader("Embedding Model")
    st.write("""
    Used the **togethercomputer/m2-bert-80M-8k-retrieval** model for generating text embeddings. This model allows us to effectively search and match Airbnb listings to your specific requirements.
    """)
    st.subheader("Vector Search")
    st.write("""
    We utilize MongoDB vector search to efficiently search embeddings and retrieve the most relevant Airbnb listings for you.
    """)
    st.write("Created by [Jay](https://github.com/jaysheth777)")

st.header("HotelX, Your smart goto hotel assistant 😎")
st.markdown("<h4>Looking for hotels for vacation, job, etc.? I've got you covered!!</h4>", unsafe_allow_html=True)
st.image('hotelx-logo.webp')
st.markdown("<h6>Simply enter your needs in the text field below or choose from one of the predefined prompts 🙂👇</h6>", unsafe_allow_html=True)

query_initiated = False
if not query_initiated:
    button_cols = st.columns(2)
    button_cols_2 = st.columns(2)
    button_pressed = ""
    if button_cols[0].button(example_prompts[0]):
        button_pressed = example_prompts[0]
    elif button_cols[1].button(example_prompts[1]):
        button_pressed = example_prompts[1]
    elif button_cols_2[0].button(example_prompts[2]):
        button_pressed = example_prompts[2]
    elif button_cols_2[1].button(example_prompts[3]):
        button_pressed = example_prompts[3]

st.markdown("<p style='text-align: center; font-size: 16px; margin-bottom: 0px;'>OR</p>", unsafe_allow_html=True)
if query := (st.text_input("Enter query:") or button_pressed):
    query_initiated = True
    query_embeddings = embed_model.get_text_embedding(query)

    results = collection.aggregate([
        {
            "$vectorSearch": {
                "queryVector": query_embeddings,
                "path": VECTOR_DATABASE_FIELD_NAME,
                "numCandidates": 100,
                "limit": 10,
                "index": "SemanticSearch",
            }
        }
    ])
    results_as_dict = {doc['name']: doc for doc in results}
    st.write(f'From your query "{query}", the following Airbnb listings were found:\n')
    for i, name in enumerate(results_as_dict.keys()):
        listing = results_as_dict[name]
        st.markdown(f"""
        <div style="border: 1px solid #ddd; padding: 10px; margin-bottom: 10px;">
            <strong>{i + 1}. Name:</strong> {name} <br>
            <strong>Summary:</strong> {listing.get('summary', 'No summary available')} <br>
            <strong>Amenities:</strong> {", ".join(listing.get('amenities', []))} <br>
            <strong>Price:</strong> {listing.get('price', 'Price not available')} <br>
            <strong>Link:</strong> <a href={listing.get('listing_url', "Link not available")}>{listing.get('listing_url', "Link not available")}</a>
        </div>
        """, unsafe_allow_html=True)
