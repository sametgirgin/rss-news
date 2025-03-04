import streamlit as st
import feedparser
from datetime import datetime
import pytz

# Set page config
st.set_page_config(
    page_title="EIA Today in Energy News",
    page_icon="⚡",
    layout="wide"
)

@st.cache_data(ttl=3600)  # Cache for 1 hour
def fetch_eia_news():
    try:
        feed_url = "https://www.eia.gov/rss/todayinenergy.xml"
        feed = feedparser.parse(feed_url)
        if feed.status != 200:
            st.error("Unable to fetch news feed. Please try again later.")
            return None
        return feed
    except Exception as e:
        st.error(f"Error fetching news feed: {str(e)}")
        return None

def format_date(date_str):
    try:
        # First try the format with timezone name
        dt = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %z')
    except ValueError:
        try:
            # Try format without timezone
            dt = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S')
        except ValueError:
            # If both fail, return the original string
            return date_str
    
    # Convert to US Eastern timezone
    eastern = pytz.timezone('US/Eastern')
    if dt.tzinfo is None:
        # If the datetime has no timezone, assume UTC
        dt = pytz.UTC.localize(dt)
    dt = dt.astimezone(eastern)
    # Format date
    return dt.strftime('%B %d, %Y')

def main():
    st.title("🔋 EIA Today in Energy News")
    
    with st.spinner("Fetching latest energy news..."):
        feed = fetch_eia_news()
        
    if feed:
        # Display news items
        for entry in feed.entries:
            with st.container():
                st.subheader(entry.title)
                st.markdown(f"*Published on {format_date(entry.published)}*")
                st.write(entry.summary)
                st.markdown(f"[Read more]({entry.link})")
                st.divider()

if __name__ == "__main__":
    main() 
