#used source 2
import argparse
import shlex
import logging
import query_service
import csv_loader

logger = logging.getLogger(__name__)

def query_handler(args):
    query = " ".join(args.query)
    print("Reading your query...")
    query_service.main(query)
    pass

def csv_handler(args):
    print("Uploading CSV to database...\n")
    csv_loader.main(args.filepath) #consider spaces in file path?
    return

#chatgpt to help with structure for learning argparse and how cli interfaces works
def main():
    #create a parser
    parser = argparse.ArgumentParser(description = "A simple CLI example using argparse")

    #create the subparsers/commands and making the subparser required
    subparsers = parser.add_subparsers(dest="command", required=True)

    #query subcommand
    parser_query = subparsers.add_parser("query")
    parser_query.add_argument("query", nargs="+") #joins string args together
    parser_query.set_defaults(func=query_handler)

    #upload subcommand
    parser_upload = subparsers.add_parser("upload")
    parser_upload.add_argument("filepath", type=str)
    parser_upload.set_defaults(func=csv_handler)

    print("Interactive CLI for DataSheet AI running. Type 'exit' to quit.")
    print("Available commands: query, upload")

    #Complete assistance with ChatGPT:
    while True:
        try:
            #adds the classic > in the terminal
            user_input = input("> ").strip()
            #method of closing the CLI Interface
            if user_input.lower() in ("exit", "quit"):
                print("Closing the Interactive CLI...")
                break

            # Split input like shell arguments
            #ex: query datatables/test1.csv => ['query', 'datatables/test1.csv']
            #good for flexibility
            args_list = shlex.split(user_input)
            if not args_list:
                continue

            # Parse arguments for subcommands
            args = parser.parse_args(args_list)
            #check if command exists by using the argument (first word of input)
            if hasattr(args, "func"):
                args.func(args)
            else:
                print("Unknown command. Available: query, upload")

        except Exception as e:
            print(f"Error: {e}")

if __name__ == '__main__':
    main()