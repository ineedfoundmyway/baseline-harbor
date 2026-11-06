import hashlib
from pathlib import Path
import tempfile
import unittest
from main import snapshot, compare, demo

class IntegrityTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
    def test_empty(self):
        self.assertEqual(snapshot(self.root),{})
    def test_sha256(self):
        (self.root/'a').write_bytes(b'abc')
        self.assertEqual(snapshot(self.root),{'a':hashlib.sha256(b'abc').hexdigest()})
    def test_nested(self):
        (self.root/'sub').mkdir()
        (self.root/'sub'/'a').write_text('a')
        self.assertIn('sub/a',snapshot(self.root))
    def test_symlink_ignored(self):
        (self.root/'a').write_text('a')
        (self.root/'link').symlink_to(self.root/'a')
        self.assertNotIn('link',snapshot(self.root))
    def test_changes(self):
        self.assertEqual(demo(),{'added':['new.txt'],'removed':['obsolete.txt'],'modified':['config.ini']})
    def test_external_directory_symlink_ignored(self):
        with tempfile.TemporaryDirectory() as external:
            (Path(external)/'secret').write_text('outside')
            (self.root/'external').symlink_to(external, target_is_directory=True)
            self.assertEqual(snapshot(self.root), {})
    def test_unchanged(self):
        self.assertEqual(compare({'a':'same'},{'a':'same'}),{'added':[],'removed':[],'modified':[]})
    def test_missing_directory(self):
        with self.assertRaises(FileNotFoundError): snapshot(self.root/'missing')
    def test_large_file(self):
        data=b'x'*150000
        (self.root/'large').write_bytes(data)
        self.assertEqual(snapshot(self.root)['large'],hashlib.sha256(data).hexdigest())
