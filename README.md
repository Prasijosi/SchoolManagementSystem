# SchoolManagementSystem

**To run the project locally, please follow these instructions:**
1. **Clone the project** to your local machine.
2. **Create a virtual environment** by running the following command:
   ```
   python -m venv venv
   ```
3. **Install the required dependencies** by executing:
   ```
   pip install -r requirements.txt
   ```
4. **Migrate the database** after installing the necessary packages:
   ```
   python manage.py migrate
   ```
5. **Start the server** to run the application:
   ```
   python manage.py runserver
   ```_
**Please note that the project does not include a `.env` file, so the email functionality for the "Contact Us" section will not work until the appropriate email configurations are set up.**
_

School Management System is a web application built with Python ,Django framework , Bulma and Sqlite DB. It focuses on managing student-teacher records and handling attendance and fee details. The system is divided into three main categories: Student, Teacher, and Admin Panel.

**Student Panel:**  
Students can register and, after approval from the admin, access their profile, attendance records, and public notices. 

**Teacher Panel:**  
Teachers can register and, once approved, manage attendance for students, publish announcements, and view student lists. They can take attendance for classes and mark it for specific dates.

**Admin Panel:**  
The admin has full control over the system, managing both student and teacher accounts. They can approve or decline registration requests, monitor student attendance, manage fees, and publish notices. The admin also oversees the system’s flow and handles all records.

The system features a user-friendly dashboard with a clean design, utilizing Bootstrap for UI elements and Vanilla CSS. Key functionalities include managing students, teachers, attendance, fees, and notices.
