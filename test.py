import unittest

import utils

import MailPrototype

from Models import Mail

class TestUtils(unittest.TestCase):

    def test_hash(self):
        self.assertEqual(utils.hash("test-Hash-function"), utils.hash("test-Hash-function"),
        "The result of the hash function is different on same plaintext.")

class TestMail(unittest.TestCase):

    def test_mail_class(self):
        _mail = Mail()
        _mail.setFrom("test@test.com")
        _mail.setTo("tester@test.com")
        _mail.setSubject("TEST")
        _mail.setBody("This is just a test.")

        self.assertEqual(_mail.getFrom(), "test@test.com",
        "Mail._from should be \'test@test.com\'")
        self.assertEqual(_mail.getTo(), "tester@test.com",
        "Mail._to should be \'tester@test.com\'")
        self.assertEqual(_mail.getSubject(), "TEST",
        "Mail._subject should be \'TEST\'")
        self.assertEqual(_mail.getBody(), "This is just a test.",
        "Mail._body should be \'This is just a test.\'")

class TestMailPrototype(unittest.TestCase):

    def test_mailprototype(self):
        _mail = Mail()
        _mail.setFrom("test@test.com")
        _mail.setTo("tester@test.com")
        _mail.setSubject("TEST")
        _mail.setBody("This is just a test.")

        draft_mail = MailPrototype.Draft(_mail)
        forward_mail = MailPrototype.Forward(_mail)
        sent_mail = MailPrototype.Sent(_mail)

        self.assertEqual(draft_mail.clone().getType(),
        "Draft", "Should be of type \'Draft\'.")
        self.assertEqual(forward_mail.clone().getType(),
        "Forward", "Should be of type \'Forward\'.")
        self.assertEqual(sent_mail.clone().getType(),
        "Sent", "Should be of type \'Sent\'.")

if __name__ == '__main__':
    unittest.main()
