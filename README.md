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
- [] Review structure of code with AI
- [] Error message/Options to deal with similar columns names/tables