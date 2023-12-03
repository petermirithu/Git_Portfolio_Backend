# Git Portfolio Backend
Welcome to the Git Portfolio Backend Server! This Django application serves as the backend for your Git portfolio frontend, providing endpoints to retrieve and manage data related to your ones portfolio.

It is basically a platform that facilitates one to create their Portfilio.

The project is live at:- https://git-portfolio-backend.vercel.app

## Getting Started

### Prerequisites

Before you start, make sure you have Python and Django installed on your machine.

- Python: [Download here](https://www.python.org/downloads/)
- Django: Install using the following command:
    ```
    pip install django
    ```
    
### Installation  
- Clone the repository to your local machine, run the command:-
    ```
    git clone https://github.com/petermirithu/Git_Portfolio_Backend.git
    ```
- Navigate to the project directory using the command:-
    ```
    cd Git_Portfolio_Backend
    ```
- Create and activate a virtual environment:
    ```
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```
- Then install dependencies using the command:-
    ```
    pip install -r requirements.txt
    ```
- You will need to create a <b>.env</b> file with following keys:-
    ```
    MONGO_DB_URI= <Your mongo db URI here>

    MONGO_DB_NAME = <Your mongo db name here >

    JWT_SECRET= <A valid JWT secret key>

    JWT_ALGORITHM= <jwt type of algorithm>

    ENCODE_ALGORITHM= <type of encoding algorithm>

    EMAIL_HOST_USER= <your Gmail email to send mails>

    EMAIL_HOST_PASSWORD= <your app generated password here>
    ```
### Development 
- To start the development server, run the following command:
    ```
    python manage.py runserver
    ```
- This will start the development server, and you can view your app at http://127.0.0.1:8000 in your browser.

