import streamlit as st
import yaml
from BookRecommender import BookRecommender

@st.cache
def get_recommender() -> BookRecommender:
    with open("books.yaml", "r") as f:
        books = yaml.safe_load(f)
    return BookRecommender(books)


if __name__ == "__main__":
    st.header("Book Recommendations")
    st.subheader("The best book recommendations in town!")
    
    rec = get_recommender()
    
    with st.form("search_form"):
        query = st.text_input("Try: \"A story about medieval England\"")
        submitted = st.form_submit_button("Search")
        if submitted:
            st.write(query)
            for title, description, url, image_url in rec(query, top_n=4):
                st.write(title)
                st.image(image_url)
                st.write(description)