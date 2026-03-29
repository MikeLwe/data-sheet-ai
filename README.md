# Data Sheet AI
Database generation with natural language using an LLM

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
- [ ] Review structure of code with AI
- [ ] Error message/Options to deal with similar columns names/tables
- [ ] If doing multiple databases, implement/update functions as appropriate

Website Links Used:
1. https://stackoverflow.com/questions/1601151/how-do-i-check-in-sqlite-whether-a-table-exists#:~:text=Comments,-Add%20a%20comment&text=If%20the%20resulting%20table%20is,can%20also%20be%20a%20view.