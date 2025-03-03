# Green Guardian Web App

Green Guardian is an AI-powered web application built with Flask that allows users to:
- **Upload images of plastic** for classification using the Google Gemni API.
- **Earn points** for each scan and compete on a weekly leaderboard.
- **Schedule a pickup** for their plastic.

## Features
- **Plastic Scanning:** Upload an image to get labels via the Google Gemni API.
- **Competition:** Earn points for each scan and view the leaderboard.
- **Pickup Scheduling:** Schedule a date for plastic pickup.

## Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone[ https://your-repo-url.git](https://github.com/nik-100xdevz/green-guardian.git)
   cd green_guardian
Below is an example **README.md** file that explains the project, its features, setup instructions, and usage details.

---

```markdown
# Green Guardian

Green Guardian is a smart waste sorting web application built with Flask. It allows users to:

- **Scan Plastic Waste:** Upload an image of plastic waste and receive reuse suggestions based on AI processing.
- **Record Contributions:** Earn points for each scan via a customer contribution system.
- **User Authentication:** Sign up, log in, and log out to manage your account.
- **Schedule Pickups:** Submit a pickup request for your waste.
- **View Leaderboard & Rewards:** See top contributors and redeem rewards based on your points.

> **Note:**  
> The scanning page (`/scan`) lets the user upload an image. After processing, it displays predictions with reuse suggestions. It then prompts for a username to record the scan via an API call to `/api/record_scan`, awarding points to the user.

## Features

- **Plastic Scanning:**  
  Users can upload an image to scan their plastic waste. The system simulates AI processing and returns reuse suggestions (e.g., reuse PET plastic as a plant pot).

- **User Authentication:**  
  Users can sign up and log in to track their contributions and manage pickup requests.

- **Contribution Tracking:**  
  Each scan awards 10 points, which are added to the user’s profile. These contributions can be viewed on a leaderboard.

- **Pickup Scheduling:**  
  Users can submit their details and schedule a pickup for their waste.

- **Rewards:**  
  Users can redeem their points for rewards (e.g., eco-friendly tote bags, discounts, or reusable water bottles).

## Technologies Used

- **Backend:** Flask, Flask-SQLAlchemy, Flask-Bcrypt, Flask-Migrate  
- **Database:** SQLite (for development; can be swapped out for MySQL/PostgreSQL in production)
- **Frontend:** HTML, CSS (Bootstrap), JavaScript
- **Image Processing Simulation:** API endpoint that simulates waste scanning (to be replaced with a real AI model integration)

## Setup Instructions

### 1. Clone the Repository

```bash
git clone(https://github.com/nik-100xdevz/green-guardian.git)
cd green_guardian
```

### 2. Create and Activate a Virtual Environment

**On Windows (Git Bash or PowerShell):**
```bash
python -m venv venv
source venv/Scripts/activate
```

**On Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

Install required packages:
```bash
pip install Flask Flask-SQLAlchemy flask-bcrypt Flask-Migrate python-dotenv
```

### 4. Set Up the Database

If you are in development and can reset your data, delete the existing `green_guardian.db` file to use the new schema.  
Alternatively, use Flask-Migrate to update the schema:

1. **Set the FLASK_APP environment variable:**
   - On Windows (Git Bash or PowerShell):
     ```bash
     export FLASK_APP=app.py
     ```
   - On Windows CMD:
     ```cmd
     set FLASK_APP=app.py
     ```

2. **Initialize the Migration Repository:**
   ```bash
   flask db init
   ```

3. **Create a Migration Script:**
   ```bash
   flask db migrate -m "Initial migration with password_hash column"
   ```

4. **Apply the Migration:**
   ```bash
   flask db upgrade
   ```

### 5. Run the Application

Start the Flask server:
```bash
python app.py
```

Visit [http://localhost:5000](http://localhost:5000) in your browser.

## Usage

- **Home Page:**  
  The landing page displays the welcome message and a "Get Started" button linking to the scan page.

- **Scanning Page (`/scan`):**  
  - Users can upload an image of plastic waste.
  - After processing, the system shows reuse suggestions.
  - The user is prompted for their username (or uses the logged-in account) to record the scan, awarding points via the `/api/record_scan` endpoint.

- **User Authentication:**  
  - Navigate to **Login** or **Sign Up** from the navigation bar.
  - Once logged in, your username is displayed and you can access additional features.

- **Pickup Requests:**  
  - Use the Pickup page to fill out a form with your details, schedule a pickup, and submit the request.

- **Leaderboard & Rewards:**  
  - View the leaderboard to see top contributors.
  - Redeem your points for rewards.

## Folder Structure

```
green_guardian/
├── app.py
├── green_guardian.db         # SQLite database (auto-created)
├── migrations/               # Flask-Migrate migration files (if using migrations)
├── uploads/                  # Temporary folder for image uploads
└── templates/
    ├── base.html
    ├── index.html
    ├── login.html
    └── signup.html
```

## Additional Notes

- **API Integration:**  
  The `/scan` endpoint currently simulates image processing. Replace this with your real AI integration as needed.

- **Security:**  
  In production, secure API keys, use HTTPS, and consider more robust authentication mechanisms.

- **Environment Variables:**  
  Use a `.env` file to manage sensitive settings (with python-dotenv).

## License

This project is licensed under the MIT License.

## Acknowledgments

- Developed by [Nikhil rai & Nikhil Dubey].
- Inspired by sustainable waste management initiatives.

```

---

This README file explains the project purpose, features, setup steps, folder structure, and usage instructions. Adjust the details (like repository URL, author name, or further custom instructions) to fit your project specifics.
