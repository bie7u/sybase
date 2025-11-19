#!/bin/bash
set -e

echo "==============================================="
echo "FINAL VERIFICATION OF POSTGRESQL TO SYBASE SQL TRANSLATOR"
echo "==============================================="
echo ""

echo "1. Running unit tests..."
python -m unittest test_translator.py -q
echo "✓ All unit tests passed"
echo ""

echo "2. Testing CLI interface..."
result=$(python cli.py "SELECT * FROM users WHERE active = TRUE LIMIT 10")
if [[ $result == *"TOP 10"* ]] && [[ $result == *"= 1"* ]]; then
    echo "✓ CLI interface works"
else
    echo "✗ CLI interface failed"
    exit 1
fi
echo ""

echo "3. Testing Python import..."
python -c "from pg2sybase import translate_postgresql_to_sybase; assert 'TOP 5' in translate_postgresql_to_sybase('SELECT * FROM t LIMIT 5')"
echo "✓ Python package import works"
echo ""

echo "4. Testing package installation..."
pip show postgresql-sybase-translator > /dev/null 2>&1
echo "✓ Package is installed"
echo ""

echo "5. Checking file structure..."
for file in README.md QUICKSTART.md SUMMARY.md cli.py demo.py examples.py test_translator.py pg2sybase/translator.py; do
    if [ -f "$file" ]; then
        echo "  ✓ $file exists"
    else
        echo "  ✗ $file missing"
        exit 1
    fi
done
echo ""

echo "6. Running integration test..."
python << 'PYEOF'
from pg2sybase import translate_postgresql_to_sybase
test_cases = [
    ("SELECT * FROM users WHERE active = TRUE LIMIT 10", "TOP 10", "= 1"),
    ("SELECT first_name || ' ' || last_name FROM users", "+", None),
    ("CREATE TABLE t (id SERIAL)", "NUMERIC(10,0) IDENTITY", None),
]
for query, expected1, expected2 in test_cases:
    result = translate_postgresql_to_sybase(query)
    assert expected1 in result, f"Expected '{expected1}' in result"
    if expected2:
        assert expected2 in result, f"Expected '{expected2}' in result"
print("All integration tests passed")
PYEOF
echo "✓ Integration tests passed"
echo ""

echo "==============================================="
echo "ALL VERIFICATIONS PASSED ✓"
echo "==============================================="
echo ""
echo "The PostgreSQL to Sybase SQL Translator is ready for use!"
echo ""
echo "Quick commands:"
echo "  - Run demo:     python demo.py"
echo "  - Run examples: python examples.py"
echo "  - Run tests:    python -m unittest test_translator.py -v"
echo "  - Use CLI:      python cli.py \"YOUR QUERY\""
echo ""
