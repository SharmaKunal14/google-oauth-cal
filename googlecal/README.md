# Backend Intern Task

## Run Locally

Clone the project

```bash
  git clone https://github.com/SharmaKunal14/google-oauth-cal.git
```

Go to the project directory

```bash
  cd google-cal-oauth-django/googlecal
```

Create a project on the GCP, go to the API and Services and make an OAuth app with the following modifications.

-   In the scope add - profile, email, openid and https://www.googleapis.com/auth/calendar
-   Add an email that you own in the test users and save.

Now go to Crenditials and make an OAuth Client ID with the following modification.

-   In the _Authorised redirect URIs_ add the URI - http://127.0.0.1:8000/rest/v1/calendar/redirect/

-   After saving, download the credentials.

After completing the above mentioned setup we are ready to go.

In the _views.py_ file under the _users_ folders, replace GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET with the values mentioned in the json file downloaded.

Once that's done, start the server

```bash
  python3 manage.py runserver
```

Navigate to the url - http://127.0.0.1:8000/rest/v1/calendar/init

After completing the OAuth flow, you will get the output as follows

https://drive.google.com/file/d/1TbvOCKIdfuxeNmH2q-7TLbLFOIZiqDuD/view?usp=share_link
