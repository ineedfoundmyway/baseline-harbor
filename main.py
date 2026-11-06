import argparse
import hashlib
import json
from pathlib import Path
import tempfile

def snapshot(directory):
    root = Path(directory).resolve(strict=True)
    if not root.is_dir():
        raise ValueError('expected a directory')
    result = {}
    for file in sorted(root.rglob('*')):
        if file.is_symlink() or any((root / parent).is_symlink() for parent in file.relative_to(root).parents if parent != Path('.')):
            continue
        if file.is_file():
            resolved = file.resolve(strict=True)
            if not resolved.is_relative_to(root):
                continue
            digest = hashlib.sha256()
            with file.open('rb') as stream:
                for chunk in iter(lambda: stream.read(65536), b''):
                    digest.update(chunk)
            result[str(file.relative_to(root))] = digest.hexdigest()
    return result

def compare(before, after):
    return {'added': sorted(after.keys()-before.keys()), 'removed': sorted(before.keys()-after.keys()), 'modified': sorted(key for key in before.keys() & after.keys() if before[key] != after[key])}

def demo():
    with tempfile.TemporaryDirectory() as directory:
        root = Path(directory)
        (root/'config.ini').write_text('mode=protected\n')
        (root/'obsolete.txt').write_text('old')
        before = snapshot(root)
        (root/'config.ini').write_text('mode=changed\n')
        (root/'obsolete.txt').unlink()
        (root/'new.txt').write_text('new')
        return compare(before, snapshot(root))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('demo')
    sub.add_parser('snapshot').add_argument('directory', type=Path)
    diff = sub.add_parser('compare')
    diff.add_argument('baseline', type=Path)
    diff.add_argument('directory', type=Path)
    args = parser.parse_args()
    try:
        if args.command == 'demo': result = demo()
        elif args.command == 'snapshot': result = snapshot(args.directory)
        else: result = compare(json.loads(args.baseline.read_text()), snapshot(args.directory))
        print(json.dumps(result, indent=2))
    except (OSError, ValueError, AttributeError, TypeError) as error:
        parser.exit(2, f'Invalid input: {error}\n')
