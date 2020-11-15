class Mail:
    _from       = None
    _to         = None
    _subject    = None
    _body       = None

    def setFrom(self, _from):
        self._from = _from

    def setTo(self, to):
        self._to = to

    def setSubject(self, subject):
        self._subject = subject

    def setBody(self, body):
        self._body = body

    def getFrom(self):
        return self._from

    def getTo(self):
        return self._to

    def getSubject(self):
        return self._subject

    def getBody(self):
        return self._body
