# skinVault
Web application showcasing CS:GO skins and their market prices, powered by a cleaned and merged PostgreSQL database.


CSGO Skins Database

This project, developed as part of a Database Systems (BDD) course, aims to design and build a web application that leverages a relational database in a real-world context.

The application displays Counter-Strike: Global Offensive (CS:GO) skins along with their current market prices, inspired by the reference website csgodatabase.com.

Main Features : 
- Structured display of CS:GO skins and their prices.
- Easy browsing of skin details.
- Simple user preference management.
- Database
- Database system: PostgreSQL

Data sources :
- Kaggle dataset
- External Git repository
- Data was cleaned, analyzed, and merged to create a unified and consistent database.
- Follows relational modeling best practices taught in the course.

Educational Objectives
- Apply relational database modeling.
- Create and manage tables and relationships in PostgreSQL.
- Utilize data in a real web application.

Project Structure : 

-- backend/ : server logic and PostgreSQL connection

-- frontend/ : web interface for skin display

-- database/ : SQL scripts to create and initialize tables


						-------------------====How to use ⚠️====------------------------------- 
1. The first step is to modify config/settings.py by adding your database information.

2. Run db/tables.sql to create the tables in your database.

3. Run scripts/import_bdd to complete the data in the database.

4. Run the manage.sh script, then the launch.sh script.










