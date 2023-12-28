# Installation
1. Run the following console command at the root of the repository:
`pip install -r requirements.txt`
2. Go to the project root:
`cd app`
3. Execute any of these console commands to perform a specific action:
     - `python manage.py runserver` -- Run Django project (to see it, go to page 127.0.0.1:8000 in the browser);
     - `python manage.py test` -- Run tests;
     - `python manage.py seed --number number_of_entries` -- Seed the database with a `number_of_entries` of random entries;
  
## What you can do on the website
- See the hierarchical view of employees;
- See detail information about the employee;
- See table-based view about employees, where you can sort or search for entries by any field;
- Register and login on a website;
- **Only for authenticated users:** Create, Update, Delete entries about employees
- **Only for authenticated users:** Change employee bosses directly in the hierarchical view using the Drag'n'Drop feature

## Additional features:
- Sorting, searching, and changing page on table-based view performs without reloading the page;
- Hierarchical view initially loads only first two levels of hierarchy. After this you can toggle any next level by clicking the button on a right side of the record;
- If you delete an record, all his employees will become employees of his boss.
