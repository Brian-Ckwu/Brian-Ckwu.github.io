import os
import sys
import frontmatter
import tweepy

def get_post_content(file_path):
    """Extract post content and metadata from the markdown file."""
    post = frontmatter.load(file_path)

    # Skip if post is marked as hidden
    if post.metadata.get('hidden', False):
        return None

    title = post.metadata.get('title', '')

    # Get the content (everything after the frontmatter)
    content = post.content.strip()

    return {
        'title': title,
        'content': content
    }

def post_to_twitter(content):
    """Post to Twitter using API v2."""
    if 'twitter' not in content['social_media']:
        return

    client = tweepy.Client(
        consumer_key=os.environ['TWITTER_API_KEY'],
        consumer_secret=os.environ['TWITTER_API_SECRET'],
        access_token=os.environ['TWITTER_ACCESS_TOKEN'],
        access_token_secret=os.environ['TWITTER_ACCESS_SECRET']
    )

    # Create tweet text
    tweet = f"# {content['title']}\n{content['content']}"

    try:
        response = client.create_tweet(text=tweet)
        print(f"Posted to Twitter: {response}")
    except Exception as e:
        print(f"Error posting to Twitter: {e}")

def main():
    changed_files = sys.argv[1:]

    for file_path in changed_files:
        # TODO: if the datetime is in the far past, skip
        if not file_path.endswith('.md'):
            continue

        content = get_post_content(file_path)
        if not content:
            continue

        # Post to each configured platform
        post_to_twitter(content)
        # Add other platforms as needed

if __name__ == '__main__':
    main()
