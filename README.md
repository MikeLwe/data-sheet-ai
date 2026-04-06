# Data Sheet AI
Database generation with natural language using an LLM

Design
- Only have the schema_manager access the database and nothing else
- This is to centralize all the sqlite functions that edit the database to keep track of any errors that occur and makes it easier to prevent the llm or the query service from affecting the database

- Added cli_interface rather than just having a main file run once based on an input
- I wanted to have the ability to run multiple queries without restarting the application and be able to upload multiple CSVs in one go.

- Implemented a Soft Delete option for when there is a table with the same title as what the user requested, saving the "deleted" tables into another database with a backup_key database to remember the multiple types of tables. (Table title notation is f"{title}_{key_value}")
- This protects against accidental deletes and keeps a proper records of all the tables, along with avoiding errors with duplicate names.

- Used pandas to read the CSV in the csv_loader.
- This is because the pandas DataFrame is great for readability, similar to json, when it reads a csv file.

- Did not implement appending columns to an existing table and only allowing rows to be appended.
- If the user wants to append columns for all the rows that exist in the table, I think it is better to archive the old data and replace the table rather than appending a column for efficiency. This also reduces the complexity of the code.

- Use input function and confirmation with infinite while loop to allow user to decide what to do
- For user interface to be better in case a typo occurs or the user misunderstands the prompt, I allow the user to decide again if the want to continue performing that task.



Plan:
- One folder contains all the CSV files
- Query Service and SQL Validator Separate Files
- SQL Files

Thigns to Consider/Look At:
- Consider classes, queues, multiple systems
- Design choice: Why use Pandas?
- Multiple Databases or all in one database?
- Multiple Databases: security, load times shorter | managing multiple databases is hard
- Single Database: can join databases together | one database crashes/secrutiy risk
- Hybrid: try going for this (ask user to make new database or not)

Problems to Fix:
- [x] Open and close connections
- [x] Implement retrieval functions in schema_manager
- [x] Review structure of code with AI
- [ ] Error message/Options to deal with similar columns names/tables
- [ ] If doing multiple databases, implement/update functions as appropriate

Website Links Used:
1. https://stackoverflow.com/questions/1601151/how-do-i-check-in-sqlite-whether-a-table-exists#:~:text=Comments,-Add%20a%20comment&text=If%20the%20resulting%20table%20is,can%20also%20be%20a%20view.
2. https://www.reddit.com/r/learnpython/comments/1s77o5c/how_to_create_cli_with_python/#:~:text=For%20a%20first%20CLI:%20start,about%20what%20becomes%20a%20command.&text=If%20you%20want%20the%20least,already%20in%20the%20standard%20library.