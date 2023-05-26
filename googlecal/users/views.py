from django.shortcuts import redirect, render
import requests
from django.contrib.auth import authenticate, login


# Create your views here.

GOOGLE_CLIENT_ID = 'INSERT_GOOGLE_CLIENT_ID_HERE'
GOOGLE_CLIENT_SECRET = 'INSERT_GOOGLE_SECRET_HERE'
GOOGLE_REDIRECT_URI = 'http://127.0.0.1:8000/rest/v1/calendar/redirect/'
GOOGLE_AUTHORIZATION_ENDPOINT = 'https://accounts.google.com/o/oauth2/auth'
GOOGLE_TOKEN_ENDPOINT = 'https://accounts.google.com/o/oauth2/token'
GOOGLE_USERINFO_ENDPOINT = 'https://www.googleapis.com/oauth2/v1/userinfo'


def google_auth(request):
    # Redirect the user to the Google OAuth authorization URL
    auth_url = f"{GOOGLE_AUTHORIZATION_ENDPOINT}?client_id={GOOGLE_CLIENT_ID}&redirect_uri={GOOGLE_REDIRECT_URI}&response_type=code&scope=openid%20email%20profile%20https://www.googleapis.com/auth/calendar"
    return redirect(auth_url)


def google_auth_callback(request):
    # Handle the callback URL where Google returns the authorization code
    code = request.GET.get('code')
    data = {
        'code': code,
        'client_id': GOOGLE_CLIENT_ID,
        'client_secret': GOOGLE_CLIENT_SECRET,
        'redirect_uri': GOOGLE_REDIRECT_URI,
        'grant_type': 'authorization_code'
    }

    # Exchange the authorization code for an access token
    response = requests.post(GOOGLE_TOKEN_ENDPOINT, data=data)
    access_token = response.json().get('access_token')
    # Use the access token to authenticate the user in your Django app
    headers = {'Authorization': f'Bearer {access_token}'}
    userinfo_response = requests.get(GOOGLE_USERINFO_ENDPOINT, headers=headers)
    userinfo = userinfo_response.json()
    # print("User info", userinfo['email'])
    # Authenticate the user using their email address as the username
    user = authenticate(request, email=userinfo['email'], password=None)
    # print("USER", user)
    if user is not None:
        # print("LOGGED IN")
        login(request, user)
        headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }

        # Make the API request to fetch the events
        response = requests.get(
            'https://www.googleapis.com/calendar/v3/calendars/primary/events', headers=headers)

        # Check the response status code
        if response.status_code == 200:
            # Events successfully fetched
            events = response.json()
            # print(events['items'][0]['description'])
            event_list = {'events': []}
            for event in events['items']:
                for key, value in event.items():
                    if key == 'summary':
                        event_list['events'].append(value)
            # print("EVENTS", event_list)
            return render(request, 'home.html', context=event_list)

        else:
            # Error occurred while fetching events
            return None

    # If the user is not authenticated, you can handle the case accordingly
    return render(request, 'authentication_failed.html')


def logged_in(request):
    return render(request, "home.html")
