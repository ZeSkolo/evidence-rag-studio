import argparse, json, sys
from pathlib import Path
from core import run

def main():
    p = argparse.ArgumentParser(description='Run the project demo or a JSON input file.')
    p.add_argument('command', choices=['demo', 'run'])
    p.add_argument('input', nargs='?')
    a = p.parse_args()
    source = Path(__file__).with_name('example.json') if a.command == 'demo' else Path(a.input or '')
    try:
        if not source.is_file() or source.stat().st_size > 1000000:
            raise ValueError('Provide a JSON file below 1 MB.')
        result = run(json.loads(source.read_text()))
        print(json.dumps(result, indent=2, allow_nan=False))
    except (ValueError, KeyError, TypeError, OSError) as e:
        print(json.dumps({'error': str(e)}), file=sys.stderr)
        return 2
    return 0
if __name__ == '__main__':
    raise SystemExit(main())
