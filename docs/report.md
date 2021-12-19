PRG1048-2.2  A short paragraph explaining the purpose of your app, and how it will be used including a list of pages and their functionality. 

## Livin’ Macrame

The Livin’ Macrame web app serves as a gallery of macrame projects with their components, and also a tool for calculating useful information relating to the creation and marketing of new macrame projects.

Users can browse existing projects, create and upload their own with accompanying images, and most importantly use the in-built functions to plan and calculate many attributes of new projects. 

### Pages:

Home
- Introduction

Projects gallery
- Create new project
    - Enter project information using forms
- List of projects and their images

Project details
- Display calculated information about the project
- Choose patterns - the components of a project
- Upload image
  
Patterns gallery
- Create new pattern
    - Enter pattern information using forms
- List of patterns and their images

Pattern details
- Display calculated information about the pattern
    - Choose knot - a component of a pattern
- Upload image

Knots gallery
- Create new knot
    - Enter knot information using forms

Knot details
- Display calculated information about the knot
    - Choose cord - a component of a knot
- Upload image

Cords gallery
- Create new cord
  - Enter cord information using forms

Cord details
- Display information about the cord
- Upload image

User Index
- List signed up users and their email addresses

Account
- Display and update account information
- Display information about the user’s created projects

Log in
- Login form. Only visible when logged out

Sign up
- Sign up form. Only visible when logged out


ERD: ![ERD](/docs/livin_macrame_ERD.png)

PRG1048-2.3 A list of any fields which will need to be validated when data is input by the user in order to prevent integrity errors.

### User:
Name
- Validate name is provided

Email
- Validate email address is correct format

Password
- Validate password is at least 6 characters long
 
 
CMP1042-7.1 (R2) A short paragraph on security concerns. (You will protect user privacy [an authorisation system? careful design? something else?] and how the SQLAlchemy ORM will protect against SQL injection attacks.)

The application protects user privacy by ensuring their passwords are not stored in plain text format. Instead they are first salted and hashed using the werkzeug.security module’s generate_password_hash() function. This uses a complex cryptographic algorithm to turn a short password into a long string of characters, deterring all but the most persistent of potential attackers from breaking it.
Users are also prevented from deleting or editing any stored information that they did not create themselves. This is achieved by attaching a creator id value to each record upon creation, and validating users again upon login using their browser cookie’s session information with flask’s flask_login LoginManager module. Anyone attempting to modify a record without the correct authorisation is denied and redirected to log in.
Any time user input is used directly in a database query, there is a potential for SQL injection attacks to compromise the database. SQLAlchemy is used as a layer of security between the inputs taken from users and the database itself. Instead of writing SQL queries directly into the database, the user supplies information to the app through routes. The input is first validated through the schema and model before being inserted into safely crafted SQL queries which are written by SQLAlchemy and are therefore sanitised by nature.
 
CMP1042-7.2 (R3) A short paragraph discussing professional, ethical and legal obligations
Example of professional obligations: (delivering the project on time, being explicit about ongoing maintenance of the system).
Example of ethical obligations: ensuring that the application conforms with ethical codes of conduct approved by industry.
Example of legal obligations: is the app subject to any legal regulation? If none, consider any privacy implications of your application.

Professional standards dictate timely delivery of projects as a core principle. By using management resources such as Trello I am able to divide a project up into discrete tasks and assign them priority and time appropriately. 

