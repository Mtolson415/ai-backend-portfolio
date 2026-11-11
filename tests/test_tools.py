from concurrent.futures import ThreadPoolExecutor
import json
import os
from pathlib import Path
import tempfile
import threading
import unittest
from unittest.mock import patch
from urllib import request, error

from ai_backend.core import Principal, Workspace, Knowledge, Denied, ToolError, Conflict, TooLarge
from ai_backend.server import create_server, token_principals

ALPHA='synthetic-test-alpha-'+'a'*40
BETA='synthetic-test-beta-'+'b'*40

class Fixture(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.root=Path(self.temp.name)
        for project in ('alpha','beta'):
            (self.root/project/'outputs').mkdir(parents=True)
            (self.root/project/'notes.txt').write_text(project+' synthetic notes',encoding='utf-8')
        self.alpha=Principal('alpha-user',frozenset({'alpha'}),frozenset({'files.read','files.write_output','knowledge.search'}))
        self.beta=Principal('beta-reader',frozenset({'beta'}),frozenset({'files.read','knowledge.search'}))
        self.workspace=Workspace(self.root)
        docs=json.loads((Path(__file__).parents[1]/'examples/knowledge.json').read_text(encoding='utf-8'))
        self.knowledge=Knowledge(docs)

    def tearDown(self):
        self.temp.cleanup()

class TestWorkspace(Fixture):
    def test_allowed_read(self):
        self.assertEqual(self.workspace.read(self.alpha,'alpha','notes.txt')['text'],'alpha synthetic notes')

    def test_cross_project_read_denied(self):
        with self.assertRaises(Denied): self.workspace.read(self.alpha,'beta','notes.txt')

    def test_traversal_and_absolute_paths_denied(self):
        for path in ('../beta/notes.txt','/etc/passwd','outputs/../../notes.txt','C:\\notes.txt','notes.txt\x00','outputs//file','./notes.txt'):
            with self.subTest(path=path), self.assertRaises(Denied): self.workspace.read(self.alpha,'alpha',path)

    def test_leaf_symlink_denied(self):
        (self.root/'alpha/link').symlink_to(self.root/'beta/notes.txt')
        with self.assertRaises(Denied): self.workspace.read(self.alpha,'alpha','link')

    def test_parent_symlink_denied(self):
        (self.root/'alpha/linkdir').symlink_to(self.root/'beta',target_is_directory=True)
        with self.assertRaises(Denied): self.workspace.read(self.alpha,'alpha','linkdir/notes.txt')

    def test_output_parent_symlink_denied(self):
        (self.root/'alpha/outputs/linkdir').symlink_to(self.root/'beta/outputs',target_is_directory=True)
        with self.assertRaises(Denied): self.workspace.write_output(self.alpha,'alpha','outputs/linkdir/file.txt','x')
        self.assertFalse((self.root/'beta/outputs/file.txt').exists())

    def test_nonregular_file_denied_without_blocking(self):
        os.mkfifo(self.root/'alpha/pipe')
        with self.assertRaises(Denied): self.workspace.read(self.alpha,'alpha','pipe')

    def test_file_size_limit(self):
        (self.root/'alpha/large').write_bytes(b'x'*65537)
        with self.assertRaises(TooLarge): self.workspace.read(self.alpha,'alpha','large')

    def test_write_output_and_read_back(self):
        result=self.workspace.write_output(self.alpha,'alpha','outputs/report.txt','synthetic report')
        self.assertEqual(result['bytes'],16)
        self.assertEqual(self.workspace.read(self.alpha,'alpha','outputs/report.txt')['text'],'synthetic report')

    def test_source_write_denied(self):
        with self.assertRaises(Denied): self.workspace.write_output(self.alpha,'alpha','notes.txt','changed')

    def test_reader_write_denied(self):
        with self.assertRaises(Denied): self.workspace.write_output(self.beta,'beta','outputs/report.txt','x')

    def test_output_does_not_overwrite_existing_or_follow_symlink(self):
        (self.root/'alpha/outputs/link').symlink_to(self.root/'beta/notes.txt')
        with self.assertRaises(Conflict): self.workspace.write_output(self.alpha,'alpha','outputs/link','changed')
        self.assertEqual((self.root/'beta/notes.txt').read_text(),'beta synthetic notes')
        self.assertEqual(sorted(x.name for x in (self.root/'alpha/outputs').iterdir()),['link'])

    def test_atomic_create_under_concurrent_writers(self):
        def write(i):
            try:
                self.workspace.write_output(self.alpha,'alpha','outputs/one.txt',str(i))
                return 'created'
            except Conflict: return 'conflict'
        with ThreadPoolExecutor(max_workers=8) as pool: results=list(pool.map(write,range(8)))
        self.assertEqual(results.count('created'),1)
        self.assertEqual(results.count('conflict'),7)
        self.assertEqual(len(list((self.root/'alpha/outputs').iterdir())),1)

    def test_output_size_limit(self):
        with self.assertRaises(TooLarge): self.workspace.write_output(self.alpha,'alpha','outputs/large','x'*65537)

class TestKnowledge(Fixture):
    def test_cited_retrieval_filters_before_scoring(self):
        result=self.knowledge.search(self.alpha,'alpha','recovery')
        self.assertTrue(result['matches'])
        self.assertTrue(all(x['source'].startswith('synthetic://alpha/') for x in result['matches']))
        self.assertNotIn('SYNTHETIC-BETA-CANARY',json.dumps(result))

    def test_explicit_cross_project_search_denied(self):
        with self.assertRaises(Denied): self.knowledge.search(self.alpha,'beta','recovery')

    def test_unknown_question_returns_empty_not_fabricated_answer(self):
        self.assertEqual(self.knowledge.search(self.alpha,'alpha','unfindablezzz')['matches'],[])

    def test_invalid_queries_rejected(self):
        for query in ('','   ','!!!',None,'x'*501):
            with self.subTest(query=str(query)[:10]), self.assertRaises(ToolError): self.knowledge.search(self.alpha,'alpha',query)

class TestHTTP(Fixture):
    def setUp(self):
        super().setUp()
        self.audit=[]
        self.server=create_server(('127.0.0.1',0),self.workspace,self.knowledge,[(ALPHA,self.alpha),(BETA,self.beta)],self.audit.append)
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True)
        self.thread.start()
        self.base='http://127.0.0.1:'+str(self.server.server_port)

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        super().tearDown()

    def post(self,path,body,token=ALPHA,extra=None):
        data=body if isinstance(body,bytes) else json.dumps(body).encode()
        headers={'Content-Type':'application/json'}
        if token is not None: headers['Authorization']='Bearer '+token
        headers.update(extra or {})
        req=request.Request(self.base+path,data=data,headers=headers,method='POST')
        try:
            with request.urlopen(req,timeout=3) as response: return response.status,json.load(response)
        except error.HTTPError as response: return response.code,json.load(response)

    def test_health(self):
        with request.urlopen(self.base+'/health') as response: self.assertEqual(response.status,200)

    def test_authentication_required(self):
        for token in (None,'wrong-token'):
            self.assertEqual(self.post('/v1/files/read',{'project':'alpha','path':'notes.txt'},token)[0],401)

    def test_authenticated_request_and_citation(self):
        status,result=self.post('/v1/knowledge/search',{'project':'alpha','query':'recovery'})
        self.assertEqual(status,200)
        self.assertTrue(result['request_id'])
        self.assertTrue(result['matches'][0]['source'].startswith('synthetic://alpha/'))

    def test_caller_headers_cannot_override_token_identity(self):
        status,result=self.post('/v1/files/read',{'project':'beta','path':'notes.txt'},extra={'X-User':'beta-reader','X-Project':'beta'})
        self.assertEqual(status,403)
        self.assertNotIn('beta synthetic notes',json.dumps(result))

    def test_malformed_json(self):
        self.assertEqual(self.post('/v1/files/read',b'{broken')[0],400)

    def test_oversized_body(self):
        self.assertEqual(self.post('/v1/files/read',b'x'*8193)[0],413)

    def test_audit_excludes_token_query_and_content(self):
        self.post('/v1/knowledge/search',{'project':'alpha','query':'recovery'})
        serialized=json.dumps(self.audit)
        self.assertNotIn(ALPHA,serialized)
        self.assertNotIn('recovery',serialized)
        self.assertNotIn('synthetic database',serialized)
        self.assertEqual(self.audit[0]['principal'],'alpha-user')

    def test_unknown_route(self):
        self.assertEqual(self.post('/v1/execute-shell',{})[0],404)

class TestStartup(unittest.TestCase):
    def test_missing_and_duplicate_tokens_rejected(self):
        for env in ({},{'AI_ALPHA_TOKEN':ALPHA,'AI_BETA_TOKEN':ALPHA}):
            with self.subTest(env=bool(env)),patch.dict(os.environ,env,clear=True),self.assertRaises(ValueError): token_principals()

if __name__=='__main__': unittest.main()
