from tdlc.tencentcloud.common import credential
from tdlc.tencentcloud.common.profile import http_profile, client_profile
from tdlc.tencentcloud.dlc.v20210125 import models
from tdlc.utils import log, configurations
from tdlc.engines import qclient
import base64

LOG = log.getLogger('QCloud')


def toSession(dto: models.NotebookSessionInfo) -> dict:
    session = {
        'name': dto.Name,
        'engine': dto.DataEngineName,
        'sessionId': dto.SessionId,
        'sparkAppId':dto.SparkAppId,
        'kind': dto.Kind,
        'status': dto.State,
        'log': [],
        'appInfo': {
            'sparkUiUrl': dto.SparkUiUrl,
        }
    }
    return session


def toStatement(dto: models.NotebookSessionStatementInfo) -> dict:

    statement_id = 0
    try:
        statement_id = int(dto.StatementId)
    except Exception as e:
        LOG.error(e)

    statement = {
        'statementId': statement_id,
        'status': dto.State,
        'completed': dto.Completed,
        'progress': dto.Progress,
        'started': dto.Started,
        'output': {}
    }


    data = {}

    if dto.OutPut.Data:
        for pair in dto.OutPut.Data:
            data[pair.Key] = pair.Value
        
    error_message = ''
    if dto.OutPut.ErrorMessage:
        error_message = ''.join(dto.OutPut.ErrorMessage)

    statement['output'] = {
        'data': data,
        'executionCount':dto.OutPut.ExecutionCount,
        'status': dto.OutPut.Status,
        'error': {
            'name': dto.OutPut.ErrorName,
            'value': dto.OutPut.ErrorValue,
            'message': error_message,
        }
    }

    return statement


class QCloudInteractiveApi(object):

    def __init__(self, region, secretId, secretKey, token=None, endpoint=None) -> None:

        self._region = region
        self._secret_id = secretId
        self._secret_key = secretKey
        self._token = token
        self._endpoint = endpoint

        cred = credential.Credential(secretId, secretKey, token=token)
        profile = client_profile.ClientProfile()
        if endpoint:
            profile.httpProfile = http_profile.HttpProfile(endpoint=endpoint)

        self._client = qclient.QClient(cred, region, profile)


    def get_engines(self):
        pass
    
    def get_sessions(self, engine, states=[]) -> list:

        request = models.DescribeNotebookSessionsRequest()
        request.DataEngineName = engine
        if states:
            request.State = states
        response = self._client.DescribeNotebookSessions(request)
        sessions = []
        for each in response.Sessions:
            sessions.append(toSession(each))
        return sessions


    def get_session(self, session_id):

        request = models.DescribeNotebookSessionRequest()
        request.SessionId = session_id

        response = self._client.DescribeNotebookSession(request)

        return toSession(response.Session)

    def create_session(self, 
                    engine, 
                    name, 
                    kind, 
                    driver_size,
                    executor_size,
                    executor_num,
                    files=[],
                    jars=[],
                    pyfiles=[],
                    archives=[],
                    timeout=3600,
                    arguments={},
                    image=None):

        request = models.CreateNotebookSessionRequest()
        request.Name = name
        request.DataEngineName = engine
        request.Kind = kind
        request.DriverSize = driver_size
        request.ExecutorSize = executor_size
        request.ExecutorNumbers = executor_num
        request.ProgramDependentFiles = files
        request.ProgramDependentJars = jars
        request.ProgramDependentPython = pyfiles
        request.ProgramArchives = archives
        request.ProxyUser = configurations.PROXY_USER.get()
        request.TimeoutInSecond = timeout
        request.Arguments = []
        request.SparkImage = image

        for k, v in arguments.items():
            o = models.KVPair()
            o.Key, o.Value = k, str(v)
            request.Arguments.append(o)

        response = self._client.CreateNotebookSession(request)

        return {
            "sessionId": response.SessionId,
            "sparkAppId": response.SparkAppId,
            "status": response.State,
        }

    def delete_session(self, session_id):

        request = models.DeleteNotebookSessionRequest()
        request.SessionId = session_id

        _ = self._client.DeleteNotebookSession(request)
        return None


    def submit_statement(self, session_id, kind, statement):

        request = models.CreateNotebookSessionStatementRequest()
        request.SessionId = session_id
        request.Kind = kind
        if not statement:
            statement = ""
        request.Code = base64.b64encode(statement.encode('utf8')).decode('utf8')

        response = self._client.CreateNotebookSessionStatement(request)

        return toStatement(response.NotebookSessionStatement)


    def get_statement(self, session_id, statement_id):

        request = models.DescribeNotebookSessionStatementRequest()
        request.SessionId = session_id
        request.StatementId = str(statement_id)

        response = self._client.DescribeNotebookSessionStatement(request)

        return toStatement(response.NotebookSessionStatement)


    def cancel_statement(self, session_id, statement_id):

        request = models.CancelNotebookSessionStatementRequest()
        request.SessionId = session_id
        request.StatementId = str(statement_id)

        _ = self._client.CancelNotebookSessionStatement(request)
        return None


    def get_logs(self,session_id):
        request = models.DescribeNotebookSessionLogRequest()
        request.SessionId = session_id
        response = self._client.DescribeNotebookSessionLog(request)
        return response.Logs

