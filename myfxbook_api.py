import requests

def login(email, password):
    try:
        login_url = "https://www.myfxbook.com/api/login.json"
        response = requests.post(login_url, data={"email": email, "password": password})
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
        login_response = response.json()
        return login_response
    except requests.exceptions.RequestException as e:
        print(f"Error during login: {e}")
        return {"error": True, "message": f"Error during login: {e}"}

def get_community_sentiment(session_id):
    try:
        sentiment_url = "https://www.myfxbook.com/api/get-community-outlook.json"
        response = requests.get(sentiment_url, params={"session": session_id})
        response.raise_for_status()
        sentiment_response = response.json()
        return sentiment_response
    except requests.exceptions.RequestException as e:
        print(f"Error during getting community sentiment: {e}")
        return {"error": True, "message": f"Error during getting community sentiment: {e}"}

def logout(session_id):
    try:
        logout_url = "https://www.myfxbook.com/api/logout.json"
        response = requests.get(logout_url, params={"session": session_id})
        response.raise_for_status()
        logout_response = response.json()
        return logout_response
    except requests.exceptions.RequestException as e:
        print(f"Error during logout: {e}")
        return {"error": True, "message": f"Error during logout: {e}"}
