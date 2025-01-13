from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os
import time
import random

# Define scopes for Blogger API
SCOPES = ["https://www.googleapis.com/auth/blogger"]

def authenticate_blogger():
    creds = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build("blogger", "v3", credentials=creds)

def get_blog_id(blogger, blog_url):
    request = blogger.blogs().getByUrl(url=blog_url)
    response = request.execute()
    return response["id"]

def get_blog_posts(blogger, blog_id):
    posts = []
    next_page_token = None
    while True:
        request = blogger.posts().list(blogId=blog_id, maxResults=50, pageToken=next_page_token)
        response = request.execute()
        posts.extend(response.get("items", []))
        next_page_token = response.get("nextPageToken")
        if not next_page_token:
            break
    return posts

def update_blog_post(blogger, blog_id, post_id, title, content, retries=5):
    for attempt in range(retries):
        try:
            update_request = blogger.posts().patch(
                blogId=blog_id,
                postId=post_id,
                body={"title": title, "content": content}
            )
            update_request.execute()
            print(f"Updated post ID {post_id}")
            time.sleep(2)
            break  # Exit loop if successful
        except Exception as e:
            wait_time = 2 ** attempt + random.uniform(0, 1)
            print(f"Error updating post ID {post_id}: {e}. Retrying in {wait_time:.2f} seconds...")
            time.sleep(wait_time)
    else:
        print(f"Failed to update post ID {post_id} after {retries} attempts.")

def main():
    old_text = "OLD_TEXT_TO_REPLACE"
    new_text = "NEW_TEXT_TO_REPLACE_WITH"
    blog_url = "YOUR_BLOG_URL"  # Replace with your blog URL


    blogger = authenticate_blogger()
    blog_id = get_blog_id(blogger, blog_url)
    posts = get_blog_posts(blogger, blog_id)

    for post in posts:
        title = post["title"]
        content = post["content"]
        updated_content = content.replace(old_text, new_text)
        if content != updated_content:
            update_blog_post(blogger, blog_id, post["id"], title, updated_content)

if __name__ == "__main__":
    main()