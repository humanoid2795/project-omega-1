import regex
import unittest


class RegexTest(unittest.TestCase):

    def test_basic_regex(self):
        self.assertEqual(regex.check(r'abcde', 'abcde'), True)
        self.assertEqual(regex.check(r'abcde', 'abcdf'), False)
        self.assertEqual(regex.check(r'ab.de', 'abcde'), True)
        self.assertEqual(regex.check(r'ab.de', 'ab1de'), True)
        self.assertEqual(regex.check(r'^abcde', 'abcde'), True)
        self.assertEqual(regex.check(r'^abcde', 'fabcde'), False)
        self.assertEqual(regex.check(r'abcde$', 'abcde'), True)
        self.assertEqual(regex.check(r'abcde$', 'abcdef'), False)
        self.assertEqual(regex.check(r'abc\dde', 'abc1de'), True)
        self.assertEqual(regex.check(r'abc\dde', 'abcfde'), False)
        self.assertEqual(regex.check(r'abc\Dde', 'abc1de'), False)
        self.assertEqual(regex.check(r'abc\Dde', 'abcfde'), True)
        self.assertEqual(regex.check(r'abc\sde', 'abc de'), True)
        self.assertEqual(regex.check(r'abc\sde', 'abc1de'), False)
        self.assertEqual(regex.check(r'abc\Sde', 'abc de'), False)
        self.assertEqual(regex.check(r'abc\Sde', 'abc1de'), True)
        self.assertEqual(regex.check(r'\w\w\w\w', 'aA0_'), True)
        self.assertEqual(regex.check(r'\w\w\w\w', 'aA0.'), False)
        self.assertEqual(regex.check(r'abc\Wde', 'abc de'), True)
        self.assertEqual(regex.check(r'abc\Wde', 'abc0de'), False)

    def test_repetition_quantifier(self):
        self.assertEqual(regex.check(r'abc*d', 'abd'), True)
        self.assertEqual(regex.check(r'abc*d', 'abcd'), True)
        self.assertEqual(regex.check(r'abc*d', 'abccd'), True)
        self.assertEqual(regex.check(r'abc+d', 'abd'), False)
        self.assertEqual(regex.check(r'abc+d', 'abcd'), True)
        self.assertEqual(regex.check(r'abc+d', 'abccd'), True)
        self.assertEqual(regex.check(r'abc?d', 'abd'), True)
        self.assertEqual(regex.check(r'abc?d', 'abcd'), True)
        self.assertEqual(regex.check(r'abc?d', 'abccd'), False)
        self.assertEqual(regex.check(r'abc{2}d', 'abcd'), False)
        self.assertEqual(regex.check(r'abc{2}d', 'abccd'), True)
        self.assertEqual(regex.check(r'abc{2}d', 'abcccd'), False)
        self.assertEqual(regex.check(r'abc{2,3}d', 'abcd'), False)
        self.assertEqual(regex.check(r'abc{2,3}d', 'abccd'), True)
        self.assertEqual(regex.check(r'abc{2,3}d', 'abcccd'), True)
        self.assertEqual(regex.check(r'abc{2,3}d', 'abccccd'), False)
        self.assertEqual(regex.check(r'abc{2,}d', 'abcd'), False)
        self.assertEqual(regex.check(r'abc{2,}d', 'abccd'), True)
        self.assertEqual(regex.check(r'abc{2,}d', 'abcccd'), True)
        self.assertEqual(regex.check(r'abc{2,}d', 'abccccd'), True)

    def test_character_class(self):
        self.assertEqual(regex.check(r'a[bc_]d', 'abd'), True)
        self.assertEqual(regex.check(r'a[bc_]d', 'aad'), False)
        self.assertEqual(regex.check(r'a[\wbc]d', 'ad'), False)
        self.assertEqual(regex.check(r'a[\wbc]d', 'a.d'), False)
        self.assertEqual(regex.check(r'a[\wbc]d', 'abd'), True)
        self.assertEqual(regex.check(r'a[\wbc]d', 'a0d'), True)
        self.assertEqual(regex.check(r'a[\wbc]d', 'a d'), False)
        self.assertEqual(regex.check(r'a[^abc]d', 'abd'), False)
        self.assertEqual(regex.check(r'a[^abc]d', 'acd'), False)
        self.assertEqual(regex.check(r'a[^abc]d', 'add'), True)
        self.assertEqual(regex.check(r'[a-z]', 'A'), False)
        self.assertEqual(regex.check(r'[a-z]', 'd'), True)
        self.assertEqual(regex.check(r'[a-z-]', 'd'), True)
        self.assertEqual(regex.check(r'[a-z-]', '-'), True)
        self.assertEqual(regex.check(r'[-a-z]', '-'), True)
        self.assertEqual(regex.check(r'[-a-z]', '-'), True)
        self.assertEqual(regex.check(r'[^a-z]', 'c'), False)
        self.assertEqual(regex.check(r'[^a-z]', '0'), True)
        self.assertEqual(regex.check(r'a[\d.]+b', 'ab'), False)
        self.assertEqual(regex.check(r'a[\d.]+b', 'a0b'), True)
        self.assertEqual(regex.check(r'a[\d.]*b', 'a01b'), True)
        self.assertEqual(regex.check(r'a[\d.]*b', 'a0123456..b'), True)

    def test_groups(self):
        self.assertEqual(regex.check(r'(abc)', 'abc'), True)
        self.assertEqual(regex.check(r'(abc)', 'abd'), False)
        self.assertEqual(regex.check(r'(abc)*', ''), True)
        self.assertEqual(regex.check(r'(abc)*', 'abc'), True)
        self.assertEqual(regex.check(r'(abc)+', ''), False)
        self.assertEqual(regex.check(r'(abc)+', 'abc'), True)
        self.assertEqual(regex.check(r'(abc)?', ''), True)
        self.assertEqual(regex.check(r'(abc)?', 'abc'), True)
        self.assertEqual(regex.check(r'(a[bc]d)', 'ad'), False)
        self.assertEqual(regex.check(r'(a[bc]d)', 'acd'), True)
        self.assertEqual(regex.check(r'(a(bc)?d)', 'abcd'), True)
        self.assertEqual(regex.check(r'(a(bc)?d)', 'ad'), True)
        self.assertEqual(regex.check(r'(a(bc)?d)', 'abcbcd'), False)
        self.assertEqual(regex.check(r'(a+b)+', 'abaab'), True)
        self.assertEqual(regex.check(r'(a*b)+', 'baaaaaab'), True)
        self.assertEqual(regex.check(r'(a(b+c)+)+', 'ab'), False)
        self.assertEqual(regex.check(r'(a(b+c)+)+', 'abc'), True)
        self.assertEqual(regex.check(r'(a(b+c)+)+', 'abbcbc'), True)
        self.assertEqual(regex.check(r'(a{2,4}){2}b+', 'aaaaaab'), True)
        self.assertEqual(regex.check(r'(a{2,4}?){2}?b+', 'aaaaaab'), True)

    def test_or(self):
        self.assertEqual(regex.check(r'a|b', 'a'), True)
        self.assertEqual(regex.check(r'a|b', 'b'), True)
        self.assertEqual(regex.check(r'a|b', 'c'), False)
        self.assertEqual(regex.check(r'a|b|c', 'c'), True)
        self.assertEqual(regex.check(r'(cat|dog|fish)', 'cat'), True)
        self.assertEqual(regex.check(r'(cat|dog|fish)', 'dog'), True)
        self.assertEqual(regex.check(r'(cat|dog|fish)', 'fish'), True)
        self.assertEqual(regex.check(r'(cat|dog|fish)', 'ant'), False)
        self.assertEqual(regex.check(r'cat|dog|fish', 'cat'), True)
        self.assertEqual(regex.check(r'cat|dog|fish', 'dog'), True)
        self.assertEqual(regex.check(r'cat|dog|fish', 'fish'), True)
        self.assertEqual(regex.check(r'cat|dog|fish', 'ant'), False)
        self.assertEqual(regex.check(r'(cat)|(dog)|(fish)', 'cat'), True)
        self.assertEqual(regex.check(r'(cat)|(dog)|(fish)', 'dog'), True)
        self.assertEqual(regex.check(r'(cat)|(dog)|(fish)', 'fish'), True)
        self.assertEqual(regex.check(r'(cat)|(dog)|(fish)', 'ant'), False)
        self.assertEqual(regex.check(r'(cat|frog)(dog|ant)', 'frogdog'), True)


if __name__ == '__main__':
    unittest.main()
