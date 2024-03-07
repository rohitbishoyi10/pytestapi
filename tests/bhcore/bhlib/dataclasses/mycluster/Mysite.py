from pydantic import BaseModel


class Mysite_Creation_DC(BaseModel):
    title: str = 'Hello World'
    tagline: str = 'Welcome'
    site_url: str = ''
    plugins: list = ["optinmonster", "wpforms-lite", "google-analytics-for-wordpress"]
    admin_user_email: str = ''
