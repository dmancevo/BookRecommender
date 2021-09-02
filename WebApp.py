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
    
    # Recommending engine.
    rec = get_recommender()
    
    query = st.text_input(("Try: \"medieval England\","
                           " \"outer space\" or"
                           " \"stories about women\"  "))
    if query:
        for title, description, url, image_url in rec(query, top_n=7):
            with st.container():
                st.subheader(f"[{title}]({url})")
                col1, col2 = st.columns([1,3])
                with col1:
                    st.image(image_url, width=150)
                with col2:
                    st.write(f"{description[:500]}...")