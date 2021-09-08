# YET (Your English Tests)
Final project for _CS50’s Web Programming with Python and JavaScript_.
This web app simulates _Listening_, and _Reading and Use of English_ parts of the Cambridge English Qualifications exams.
## Distinctiveness and Complexity
The app is designed to be used by two different types of user: teachers and students. Its complexity relies on the many models and relationships between them (compared to the rest of the course's projects). As required, the project was built using Django on the back-end, and Javascript on the front-end.
### Teachers' features:
- **Create new test**: choosing one of the two categories, typing a task (or uploading an image), uploading (if needed) audio files, typing the correct(s) answer(s) for each question.
- **Tests page**: view all created tests.
- **Individual test page**: see the content of the test and:
  - _Edit test_: change title, task text, image, or audio, modify or add more correct answers for each question.
  - _Assign test_: ability to assign a test for a student to solve.
  - _Remove assignment_.
  - _See results_: View the tests results for the students who have completed the assignment. See the score percentage of the test, individual answers for each question, assign a custom score to incorrect answers (in case of spelling mistakes, for example).
### Students' features:
- **Tests page**: view the list of all (assigned and finished) tests.
- **Assigned test**:
  - _See the content_: View the task text and/or image, and - in the case of Listening test - listen to the audio files, for each part of the test.
  - _Answer question_: posibility to write or select an aswer for each question.
  - _Continue later_: every time the student clicks to see the next or previous parts of an assigned test; the answers are saved in the database. This allows the student to continue answering the exam later (he/she can even log out and log in again to continue).
  - _Finish_: when the student considers that the test is ready to be graded, he/she can click the Finish button. It will take the user to the results page.
- **Finished test**: when clicking on any finishined test of the list, or after finishing a test, the user will be taken to the results page of that test. It will display the score percentage for the whole test, and a table showing the answer given to each question as well as the correct(s) answer(s), and the score for that answer (the score percentage and individual scores could change if the teacher decides to assign a custom score to a given answer, or if he/she decides to change the correct(s) answer(s) for a particular question). This page also shows the test contents (text/images/audios).
# Folders and files
- `capstone`
  - `/capstone` Django project folder
  - `/media/tests` Folder to store apps images and audio files
  - `/tests` App folder
    - `/fixtures/categories.yaml` Initial data for the Category model
    - `/static` Static files folder
      - `/css` Folder containing css files
      - `/images` Folder containing images files used in the app
      - `/js` Folder containing JavaScript files used in the app
        - `/add_edit_test.js` Handles creating forms for add or edit a test as well as saving the data in the database.
        - `/bootstrap.js`Bootstrap JS file
        - `/jquery-3.4.1.min.js` JQuery JS file
        - `teacher_results.js` Handles showing individual results of each student for a given test and assigning custom scores to incorrect answers.
    - `/templates/tests` Templates files for the app
      - `/404.html` Template for 404 (not found) pages
      - `/index.html` Template for the index page showing the list of all tests (teacher), or assigned and finished tests (student).
      - `/layout.html` Template layout containing the head and navbar (common to all pages)
      - `/login.html` Template for login page
      - `/new_test.html` Template for the new test page (teacher)
      - `/register.html` Template for register page
      - `/teacher_results.html` Template for the results page (teacher).
      - `/test_form_layout.html` Template for generating HTML forms for adding or editing a test.
      - `/test.html` Template for displaying test content page; answer forms if test is not finished, or results otherwise (student); admin section (teacher) for editing, assigning, unassigning, etc. the test.
    - `/templatetags/load_answer.py` Custom Django filters
    - `/admin.py` Registered models for admin
    - `/models.py` Model classes for the app
    - `/urls.py` URL paths for the app
    - `/views.py` View methods for the app
  - `/manage.py`Django project file
  - `/requirements.txt` Required Python packages to run the app
  - `/README.md` This file 
# How to run the app
1. In your terminal, `cd` to the `capstone` main directory.
2. Run `python manage.py makemigrations` to make migrations.
3. Run `python manage.py migrate` to apply migrations to your database.
4. Run `python manage.py loaddata tests/fixtures/categories.yaml` to provide initial data for the Category model.
5. Run `python manage.py createsuperuser` to create an admin user.
6. Run `python manage.py runserver`
7. In your browser go to `http://127.0.0.1:8000/register/` and register an account (that will be flagged as teacher), then `logout`.
8. In your browser go to `http://127.0.0.1:8000/admin/` and login with the admin user created in step 4. Go to the `Users` admin page and mark _admin user_ and the _user created in step 5_ as teacher (by checking the `Is teacher` checkbox).
9. In your browser go to `http://127.0.0.1:8000/` (you will be redirected to the login page). You can login as teacher and start creating tests, or you can go the register page and register for a new (student) account.
