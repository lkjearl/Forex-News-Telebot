import asyncio
import json
import bot
from myfxbook_api import login, get_community_sentiment, logout
from decouple import config

# Load environment variables from .env
email = config("MYFXBOOK_EMAIL")
password = config("MYFXBOOK_PASSWORD")

async def main():
    login_response = login(email, password)

    if not login_response["error"]:
        session_id = login_response["session"]
        print(f"Login successful. Session ID: {session_id}")

        sentiment_response = get_community_sentiment(session_id)

        if not sentiment_response["error"]:
            symbols = sentiment_response["symbols"]
            sentiment_data = {}

            for symbol_data in symbols:
                symbol_name = symbol_data["name"]

                if symbol_name in ["EURUSD", "GBPUSD", "AUDUSD", "NZDUSD", "XAUUSD", "USDCHF", "USDCAD", "USDJPY", "EURJPY", "GBPJPY"]:
                    short_percentage = symbol_data["shortPercentage"]
                    long_percentage = symbol_data["longPercentage"]
                    sentiment_data[symbol_name] = {"shorts": short_percentage, "longs": long_percentage}

            with open("sentiment_data.json", "w") as f:
                json.dump(sentiment_data, f, indent=2)
                print("Sentiment data saved to sentiment_data.json")
        else:
            print(f"Failed to get community sentiment. Error message: {sentiment_response['message']}")

        logout_response = logout(session_id)

        if not logout_response["error"]:
            print("Logged out successfully.")
        else:
            print(f"Logout failed. Error message: {logout_response['message']}")
    else:
        print(f"Login failed. Error message: {login_response['message']}")
    
    # Call and pass data to bot function
    await bot.send_sentiment_data()

if __name__ == "__main__":
    asyncio.run(main())
