# ✨ Django Portfolio Project ✨

Welcome to my personal portfolio project, built with the powerful Django framework! This application is designed to showcase my skills, projects, blog posts, and certifications in a clean, modern, and interactive way. It's a dynamic platform that allows me to highlight my work and share my journey as a developer.

## 🚀 Features

*   **Dynamic Profile**: A dedicated section to introduce myself, my expertise, and my professional background.
*   **Showcase Projects**: Detailed pages for each project, complete with descriptions, technologies used, and links.
*   **Engaging Blog**: A fully functional blog to share insights, tutorials, and updates on my development experiences.
*   **Certifications Display**: Highlight earned certifications to validate skills and knowledge.
*   **Responsive Design**: Optimized for various devices, ensuring a seamless experience on desktop, tablet, and mobile.
*   **Admin Panel**: Robust Django admin interface for easy content management.

## 🛠️ Technologies Used

*   **Backend**: Python, Django
*   **Database**: SQLite (default, easily configurable for PostgreSQL/MySQL)
*   **Frontend**: HTML5, CSS3, JavaScript
*   **Styling**: Custom CSS (and potentially a CSS framework if integrated)
*   **Version Control**: Git

## ⚙️ Local Installation Guide

Follow these steps to get a copy of this project up and running on your local machine for development and testing purposes.

### Prerequisites

Before you begin, ensure you have the following installed:

*   **Python 3.8+**: Download from [python.org](https://www.python.org/downloads/)
*   **pip**: Python package installer (usually comes with Python)
*   **Git**: Download from [git-scm.com](https://git-scm.com/downloads/)

### Step-by-Step Setup

1.  **Clone the Repository**

    Open your terminal (Git Bash recommended for Windows) and clone the project to your desired directory:

    ```bash
    git clone <YOUR_REPOSITORY_URL>
    cd portfolio
    ```

    *(Replace `<YOUR_REPOSITORY_URL>` with the actual URL of your GitHub repository.)*

2.  **Create a Virtual Environment**

    It's highly recommended to use a virtual environment to manage project dependencies. Navigate to the root of your project (where `manage.py` is located) and create one:

    ```bash
    python -m venv myenv
    ```

3.  **Activate the Virtual Environment**

    *   **Windows (Command Prompt/PowerShell):**
        ```bash
        .\myenv\Scripts\activate
        ```
    *   **Windows (Git Bash):**
        ```bash
        source myenv/Scripts/activate
        ```
    *   **macOS/Linux:**
        ```bash
        source myenv/bin/activate
        ```

4.  **Install Dependencies**

    With your virtual environment activated, install all required packages using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

5.  **Apply Migrations**

    Django uses migrations to define your database schema. Apply the initial migrations:

    ```bash
    python manage.py migrate
    ```

6.  **Create a Superuser (for Admin Panel access)**

    You'll need a superuser account to access the Django admin panel:

    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create your username, email, and password.

7.  **Collect Static Files**

    This command gathers all static files (CSS, JavaScript, images) into a single directory, which is important for deployment and often for development as well:

    ```bash
    python manage.py collectstatic
    ```
    Type `yes` when prompted.

8.  **Run the Development Server**

    Finally, start the Django development server:

    ```bash
    python manage.py runserver
    ```

    You can now access the project in your web browser at `http://127.0.0.1:8000/`.
    To access the admin panel, go to `http://127.0.0.1:8000/admin/` and log in with the superuser credentials you created.

## ✅ Testing the Project

To ensure everything is working correctly, you can run Django's built-in tests:

```bash
python manage.py test