from flask import Flask, render_template, request, redirect, url_for, Response
from scripts.crawler import Crawler
from scripts.fetch_from_api import FetchFromAPI
import pandas as pd

app = Flask(__name__)

# Route for index.html (home page)
@app.route('/')
def home():
    return render_template("index.html")

# Route for app.html (form page)
@app.route('/app')
def app_page():
    return render_template("app.html")

# Route for handling form submission
@app.route('/submit_form', methods=['POST'])
def submit_form():
    # Get form data
    email = request.form.get('email')
    password = request.form.get('password')
    api_key = request.form.get('api_key')
    company = request.form.get('company')
    department = request.form.get('department')
    num_pages = int(request.form.get('num_pages'))

    crawler = Crawler(email, password)
    fetcher = FetchFromAPI(api_key)
    
    profiles = []
    for i in range(1,num_pages + 1):
        links = crawler.crawl(company, department, i)
        for link in links:
            profiles.append(fetcher.fetch(link))
    
    crawler.close()

    df = pd.DataFrame(profiles)
    df = df[df['username'].notna() & (df['username'] != '')]
    
    # Convert DataFrame to CSV format
    csv_data = df.to_csv(index=False)

    # Create a response object with the CSV content
    response = Response(
        csv_data,
        mimetype="text/csv",
        headers={
            "Content-Disposition": "attachment;filename=profiles.csv"
        }
    )

    return response

if __name__ == "__main__":
    app.run()
