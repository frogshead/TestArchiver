import json
from urllib.request import Request, urlopen

class DefaultListener():
    def __init__(self):
        self.suites = []
        self.tests = []

    def suite_result(self, suite):
        self.suites.append(suite)
        # print(suite.full_name)
        # print(suite.status)

    def test_result(self, test):
        self.tests.append(test)
        # print(test.full_name)
        # print(test.status)

    def end_run(self):
        pass




class ChangeEngineListener(DefaultListener):
    CHANGE_ENGINE_URL = "http://localhost:8888"

    def __init__(self):
        super(ChangeEngineListener, self).__init__()

    def end_run(self):
        top_suite = self.suites[-1]
        changes = top_suite.metadata['changes'] if 'changes' in top_suite.metadata else None
        changes = changes.split('\n') if changes else []
        #print(changes)
        self.report_changes(self.tests, changes)

    def report_changes(self, tests, changes):
        data = {"tests": [{'name': test.full_name, 'status': test.status} for test in tests],
                "changes": changes}
        url = "{change_engine_url}/result/".format(change_engine_url=CHANGE_ENGINE_URL)
        request = Request(url)
        request.add_header('Content-Type', 'application/json;')
        body = json.dumps(data)
        response = urlopen(request, body.encode("utf-8"))
        if response.getcode() != 200:
            print("ERROR: ChangeEngine update failed. Return code: {}".format(response.getcode()))
            print(response.read())
