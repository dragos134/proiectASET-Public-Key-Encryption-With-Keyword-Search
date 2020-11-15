import unittest

import MailPrototype

from Models import Mail

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

if __name__ == '__main__':
    unittest.main()
