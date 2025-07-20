# app.py

import os
from flask import Flask, render_template, request
from markdown import markdown

# --- Local Imports ---
# 1. Import your form class from forms.py
#    I've assumed the class name is 'BlogGeneratorForm'. Update if yours is different.
from forms import BlogGeneratorForm

# 2. Import your crew from your crew.py file.
#    This assumes you have a file named 'crew.py' with a Crew object named 'yt_blog_crew'.
from crew import yt_blog_crew 

# --- Flask App Initialization ---
app = Flask(__name__)
# This is required for Flask-WTF to protect against CSRF attacks
app.config["SECRET_KEY"] = os.urandom(24)


# --- Main Application Route ---
@app.route("/", methods=["GET", "POST"])
def home():
    """
    This single route handles both displaying the form (GET request) 
    and processing the submitted URL (POST request).
    """
    form = BlogGeneratorForm()
    blog_content_html = None # Variable to hold the final result

    # This block executes only when the user submits a valid form
    if form.validate_on_submit():
        # Get the validated URL from the form object
        youtube_video_url = form.youtube_url.data

        # Prepare the input for your CrewAI crew
        inputs = {'youtube_video_url': youtube_video_url}

        # --- Kickoff the CrewAI process ---
        print(f"Starting Crew with URL: {youtube_video_url}")
        # kickoff() returns a CrewOutput object, not a string
        crew_output = yt_blog_crew.kickoff(inputs=inputs)
        print("Crew has finished its work.")

        # *** FIX APPLIED HERE ***
        # We access the .raw attribute to get the final string output
        # before passing it to the markdown function.
        if crew_output and crew_output.raw:
            blog_content_html = markdown(crew_output.raw, extensions=['fenced_code', 'tables'])
        else:
            # Handle case where there might be no output
            blog_content_html = "<p>Sorry, there was an error generating the content.</p>"


    # Render the main page template.
    # It will pass the form and the generated blog_content (if available) to the HTML.
    return render_template("index.html", title="YT to Blog", form=form, blog_content=blog_content_html)


# --- Run the Application ---
if __name__ == "__main__":
    # debug=True allows you to see errors and automatically reloads the server on changes.
    app.run(debug=True)
