import unittest
from tools import scan_vulnerabilities

class TestTools(unittest.TestCase):
    def test_clean_code(self):
        code = "def add(a, b):\n    return a + b"
        findings = scan_vulnerabilities(code)
        self.assertEqual(len(findings), 0)

    def test_hardcoded_secret(self):
        code = "API_KEY = '12345abcdef'"
        findings = scan_vulnerabilities(code)
        self.assertEqual(len(findings), 1)
        self.assertEqual(findings[0]['category'], "Hardcoded Secret")

    def test_sql_injection(self):
        code = "query = f'SELECT * FROM users WHERE id = {user_id}'"
        findings = scan_vulnerabilities(code)
        self.assertTrue(any(f['category'] == 'SQL Injection Risk' for f in findings))

    def test_insecure_subprocess(self):
        code = "subprocess.run('ls -l', shell=True)"
        findings = scan_vulnerabilities(code)
        self.assertTrue(any(f['category'] == 'Insecure Subprocess' for f in findings))

    def test_insecure_deserialization(self):
        code = "data = pickle.loads(user_payload)"
        findings = scan_vulnerabilities(code)
        self.assertTrue(any(f['category'] == 'Insecure Deserialization' for f in findings))

    def test_weak_hashing(self):
        code = "h = hashlib.md5(b'password')"
        findings = scan_vulnerabilities(code)
        self.assertTrue(any(f['category'] == 'Weak Hashing' for f in findings))

if __name__ == '__main__':
    unittest.main()
