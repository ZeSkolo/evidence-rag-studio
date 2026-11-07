import unittest, os, json
from unittest.mock import patch, MagicMock
from core import run

class Tests(unittest.TestCase):

    def base(self):
        return {'question': 'snapshots', 'documents': [{'id': 'a', 'text': 'Snapshots retain immutable blocks.'}]}

    def test_evidence(self):
        r = run(self.base())
        self.assertFalse(r['abstained'])
        self.assertIn('[a:1]', r['answer'])

    def test_abstain(self):
        p = self.base()
        p['question'] = 'bananas'
        self.assertTrue(run(p)['abstained'])

    def test_duplicate_ids(self):
        p = self.base()
        p['documents'] *= 2
        with self.assertRaises(ValueError):
            run(p)

    def test_unknown_mode(self):
        p = self.base()
        p['mode'] = 'pretend'
        with self.assertRaises(ValueError):
            run(p)

    def test_live_adapter(self):
        p = self.base()
        p['mode'] = 'live'
        res = MagicMock()
        res.__enter__.return_value.read.return_value = json.dumps({'choices': [{'message': {'content': 'Answer [a:1]'}}]}).encode()
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'TEST_ONLY', 'OPENAI_MODEL': 'test-model'}), patch('urllib.request.urlopen', return_value=res):
            self.assertEqual(run(p)['answer'], 'Answer [a:1]')

    def test_provider_request_target(self):
        from core import generate
        res = MagicMock()
        res.__enter__.return_value.read.return_value = json.dumps({'choices': [{'message': {'content': 'ok'}}]}).encode()
        with patch.dict(os.environ, {'OPENAI_API_KEY': 'TEST_ONLY', 'OPENAI_MODEL': 'test-model'}), patch('urllib.request.urlopen', return_value=res) as call:
            generate('question', [])
            request = call.call_args.args[0]
            self.assertEqual(request.full_url, 'https://api.openai.com/v1/chat/completions')
            self.assertEqual(request.get_header('Authorization'), 'Bearer TEST_ONLY')
