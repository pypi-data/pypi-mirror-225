import time
import os
import jira


class JIRAClient:
    def __init__(self, cookie=None):
        self.server = 'https://its.cern.ch/jira'

        # TODO: Make these files more configurable. It's not good to specify them in the source code.
        os.environ['JIRA_SSO_COOKIE'] = '/tmp/PnR_TnI-sso-cookie'
        cookie = os.environ.get('JIRA_SSO_COOKIE', cookie)

        os.environ['TNIUSER_PASS'] = '/home/workflow-restapi/tniuser_pass.txt'
        os.environ['TNIUSER_UNAME'] = '/home/workflow-restapi/tniuser_uname.txt'

        # Try to log in with existing cookie, if any
        self.client = self.logIn(cookie)

        # if you cannot log in w/ existing cookie, then create one
        if not self.client:
            uname = os.popen("cat $TNIUSER_UNAME").read()
            password = os.popen("cat $TNIUSER_PASS").read()
            command = "echo {} | kinit {}@CERN.CH".format(str(password)[:-1], str(uname)[:-1])
            out = os.popen(command).read()
            print(out)
            out = os.popen("cern-get-sso-cookie -u https://its.cern.ch/jira/loginCern.jsp -o {} --krb".format(
                '$JIRA_SSO_COOKIE')).read()
            print(out)

            self.client = self.logIn(cookie)

        if not self.client:
            raise Exception("No JIRA Connection!")

    def logIn(self, cookie):
        cookies = {}
        try:
            for line in open(cookie, 'r').read().split('\n'):
                tokens = line.split()
                if len(tokens) < 7:
                    continue
                if tokens[5] in ['JSESSIONID', 'atlassian.xsrf.token']:
                    cookies[tokens[5]] = tokens[6]
            client = jira.JIRA('https://its.cern.ch/jira', options={'cookies': cookies})
            return client
        except Exception as e:
            print("Failed to log in to JIRA: ", str(e))

    def getTicketCreationTime(self, ticket):
        return ticket.fields.created

    def find(self, specifications):
        query = 'project=CMSCOMPPR'
        summary = specifications.get('prepID', specifications.get('summary', None))
        if summary:
            query += ' AND summary~"%s"' % summary

        if specifications.get('status', None):
            status = specifications['status']
            if status.startswith('!'):
                query += ' AND status != %s' % (status[1:])
            else:
                query += ' AND status = %s' % status

        if specifications.get('label', None):
            label = specifications['label']
            query += ' AND labels = %s' % label

        if specifications.get('text', None):
            string = specifications['text']
            query += ' AND text ~ "%s"' % string

        return self._find(query)

    def _find(self, query):
        return self.client.search_issues(query, maxResults=-1)