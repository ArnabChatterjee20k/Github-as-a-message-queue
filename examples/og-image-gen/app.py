from flask import Flask, render_template, redirect, request, url_for
import uuid
import redis
from utils import produce
import os

# Initialize the Flask app
app = Flask(__name__)

# Connect to Redis
r =  redis.Redis(
    host='redis-15902.c256.us-east-1-2.ec2.redns.redis-cloud.com',
    port=15902,
    decode_responses=True,
    username="default",
    password=os.environ.get("REDIS_PASSWORD"),
)

# Route for homepage (input field for URL)
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        website_url = request.form['website_url']
        # Produce an event to the GitHub message queue
        uid = produce(website_url)
        # Save UUID and website URL to Redis
        r.set(uid, "producing...")
        # Redirect to the UUID page
        return redirect(url_for('view_website', uuid=uid))
    return render_template('index.html')

# Route for displaying the UUID page
@app.route('/<uuid>')
def view_website(uuid):
    # Check if the UUID exists in Redis
    website_url = r.get(uuid)
    if website_url:
        return render_template('website_view.html', uuid=uuid, website_url=website_url)
    return "URL not found", 404

if __name__ == "__main__":
    app.run(debug=True)
