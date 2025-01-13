Script for updating Blogger posts in bulk
We need to use the Blogger API

Steps to Proceed:
-Enable the Blogger API in the Google Cloud Console
-Download the OAuth 2.0 client_secrets.json and place it in the script folder
-Replace the old text with new text in the content
-Replace "YOUR_BLOG_URL" with your actual blog URL in the script
-Run the script

Expected errors:
1. When too many requests are sent in a short time, you will encounter the error that is due to rate limiting by the Blogger API
   To avoid hitting the rate limit, introduce a small delay (e.g., 1–2 seconds) after each post update
   This will slow down the requests, preventing the 429 Quota exceeded the error
2. 503 Service Unavailable error means the Blogger API server is temporarily down or overloaded.
   This usually resolves on its own, but we can make the script more resilient by implementing automatic retries with exponential backoff

The script automatically retries with exponential backoff for failed updates. 
If a post fails to update, the script will retry up to 5 times, waiting longer after each attempt.
