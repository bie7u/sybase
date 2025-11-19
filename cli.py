#!/usr/bin/env python3
"""
Command-line interface for PostgreSQL to Sybase SQL translator.

Usage:
    python cli.py "SELECT * FROM users WHERE active = TRUE LIMIT 10"
    python cli.py --file input.sql
    echo "SELECT NOW()" | python cli.py
"""

import sys
import argparse
from pg2sybase import translate_postgresql_to_sybase


def main():
    parser = argparse.ArgumentParser(
        description="Translate PostgreSQL SQL to Sybase SQL dialect",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s "SELECT * FROM users WHERE active = TRUE LIMIT 10"
  %(prog)s -f input.sql -o output.sql
  echo "SELECT NOW()" | %(prog)s
  cat queries.sql | %(prog)s > sybase_queries.sql
        """
    )
    
    parser.add_argument(
        'query',
        nargs='?',
        help='PostgreSQL query to translate (if not reading from stdin or file)'
    )
    
    parser.add_argument(
        '-f', '--file',
        help='Read query from file'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Write output to file (default: stdout)'
    )
    
    args = parser.parse_args()
    
    # Determine input source
    if args.file:
        with open(args.file, 'r') as f:
            query = f.read()
    elif args.query:
        query = args.query
    elif not sys.stdin.isatty():
        query = sys.stdin.read()
    else:
        parser.print_help()
        sys.exit(1)
    
    # Translate
    result = translate_postgresql_to_sybase(query)
    
    # Output
    if args.output:
        with open(args.output, 'w') as f:
            f.write(result)
            f.write('\n')
        print(f"Translated query written to {args.output}")
    else:
        print(result)


if __name__ == '__main__':
    main()
