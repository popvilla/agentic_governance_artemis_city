# FinLit Application: Financial Literacy with Semantic Loop and Power BI Integration

FinLit is an interactive financial literacy application designed for students to manage mock investment funds, make trading decisions, and track their portfolio performance. Instructors can guide students through webinars, simulate market events, and provide personalized feedback. Administrators manage accounts, generate reports, and maintain content. A chatbot offers real-time financial literacy information, navigation help, and simulated market news.
This project integrates a Next.js/React frontend, a FastAPI (Python) backend, and a Supabase PostgreSQL database, with a focus on a "Semantic Loop" workflow using Power BI for data modeling and analytics.
Prerequisites
Before you begin, ensure you have the following software installed on your system:
  Node.js (v18 or higher) & npm: For the Next.js frontend.
  Check with: node -v and npm -v
  Install: nodejs.org
  Python (v3.11 or higher): For the FastAPI backend.
  Check with: python3 --version
  Install: python.org
  Poetry: Python dependency management (alternative to pip and venv).
  Check with: poetry --version
  Install: pip install poetry
  Supabase CLI: For local Supabase development and migrations.
  Check with: supabase --version
  Install: npm i -g supabase
  Power BI Desktop: (Optional, for Semantic Loop workflow) For data modeling and visualization.
  Download: powerbi.microsoft.com
  Git: For cloning the repository.
  Check with: git --version
  Install: git-scm.com
Setup & Installation
Follow these steps to get the FinLit application up and running locally.

1. Clone the Repository
git clone <repository-url>
cd finlit-app # Or whatever your project folder is named
2. Supabase Setup
a. Create a Supabase Project (Online)
 Go to Supabase Dashboard.
 Sign up or log in.
 Create a new project. Remember your Project URL and Service Role Key (found under Project Settings > API). You'll need these for the backend.
b. Local Supabase Environment
Initialize Supabase locally and apply the schema:
supabase init
supabase start
supabase db push
This will apply the initial database schema and Row-Level Security (RLS) policies defined in supabase/migrations/0001_initial_schema.sql to your local Supabase instance.
3. Backend Setup (FastAPI)
 Navigate to the backend directory:

    ```bash
    cd backend
    ```

 Install Python dependencies using Poetry:
    ```bash
    poetry install
    ```
 Create a .env file in the backend directory based on .env.example:
    ```bash
    cp .env.example .env
    ```
 Edit the .env file with your Supabase credentials and OpenAI API key:
    ```
    SUPABASE_URL="YOUR_SUPABASE_PROJECT_URL"
    SUPABASE_SERVICE_KEY="YOUR_SUPABASE_SERVICE_ROLE_KEY"
    OPENAI_API_KEY="YOUR_OPENAI_API_KEY"
    ```
4. Frontend Setup (Next.js)
 Navigate to the frontend directory:
    ```bash
    cd frontend
    ```
 Install Node.js dependencies:
    ```bash
    npm install
    ```
 Create a .env.local file in the frontend directory based on .env.local.example:
    ```bash
    cp .env.local.example .env.local
    ```
 Edit the .env.local file with your Supabase public credentials and FastAPI backend URL:
    ```
    NEXT_PUBLIC_SUPABASE_URL="YOUR_SUPABASE_PROJECT_URL"
    NEXT_PUBLIC_SUPABASE_ANON_KEY="YOUR_SUPABASE_ANON_KEY"
    NEXT_PUBLIC_FASTAPI_URL="http://localhost:8000"
    ```
    (The Supabase Anon Key can be found in your Supabase Project Settings > API, similar to the Service Role Key).
Running the Application
Ensure your local Supabase instance is running before starting the backend and frontend.

1. Start Supabase (if not already running)
From the project root directory:
supabase start
2. Start the Backend (FastAPI)
From the backend directory:
poetry run uvicorn main:app --reload --port 8000
This will start the FastAPI server, typically accessible at <http://localhost:8000>.
3. Start the Frontend (Next.js)
From the frontend directory:
npm run dev
This will start the Next.js development server, typically accessible at <http://localhost:3000>.
Open your web browser and navigate to <http://localhost:3000> to access the FinLit application.
Power BI Semantic Loop (Optional)
For the Semantic Loop workflow:
 Open Power BI Desktop.
 Go to Get Data -> PostgreSQL database.
 Enter localhost for Server and 54322 for Port (for local Supabase). Database name is postgres.
 Choose DirectQuery if you want near-real-time updates, or Import for faster dashboard performance.
 Import the users, portfolios, trades, market_events, webinars, and chatbot_interactions tables.
 In the Model view, define relationships between your tables (e.g., users to portfolios via user_id).
 Create DAX measures for key metrics like "Total Profit/Loss", "Portfolio Net Growth %", etc.
