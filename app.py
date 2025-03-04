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

def fetch_eia_news():
    # Fetch RSS feed
    feed_url = "https://www.eia.gov/rss/todayinenergy.xml"
    feed = feedparser.parse(feed_url)
    return feed

def format_date(date_str):
    # Parse the date string to datetime object
    dt = datetime.strptime(date_str, '%a, %d %b %Y %H:%M:%S %Z')
    # Convert to US Eastern timezone
    eastern = pytz.timezone('US/Eastern')
    dt = eastern.localize(dt)
    # Format date
    return dt.strftime('%B %d, %Y')

def main():
    # Add header
    st.title("🔋 EIA Today in Energy News")
    st.markdown("Latest news and updates from the U.S. Energy Information Administration")
    
    # Fetch news
    feed = fetch_eia_news()
    
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
