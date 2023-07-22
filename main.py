import time
import requests
from bs4 import BeautifulSoup
from aiogram import Bot, Dispatcher, types
import asyncio

# Replace 'YOUR_BOT_TOKEN' with the token you received from BotFather
bot = Bot(token='5843800619:AAE1pL_OsNYKjswpV1RDSCB9M3gAmF8P3oI')
dp = Dispatcher(bot)
channel_id = '@yakob_aau_blog'  # Replace with your news channel username or ID

# Function to scrape news from the website
def scrape_news():
    url = "http://www.aau.edu.et/blog/category/news/"  # Replace this with the URL of the website you want to scrape
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    news_articles = []

    # Adjust the CSS selector to match the HTML elements containing the news articles
    all_content = soup.find('div', id='content')
    article_elements = all_content.find_all('div', class_='post')


    for article in article_elements:
        title = article.h2.a.text
        description_content = article.find('div', class_="entry")
        description = description_content.p.text.strip()
        link = description_content.a['href']
        news_articles.append({'title': title, 'description': description, 'link': link})

    return news_articles

# Function to post news to the channel
async def post_news_to_channel(article):
    title = article.get('title', '')
    description = article.get('description', '')
    link = article.get('link', '')
    message = f"{title}\n\n{description}\n\nRead more: {link}"

    await bot.send_message(chat_id=channel_id, text=message, disable_web_page_preview=True)

# Set the time interval (in seconds) between news posts
time_interval = 20  # 20 seconds

async def main():
    while True:
        news_articles = scrape_news()
        for article in news_articles:
            await post_news_to_channel(article)
            await asyncio.sleep(2)  # Add a small delay between each message to avoid rate limiting
        await asyncio.sleep(time_interval)

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
