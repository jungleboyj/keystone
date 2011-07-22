# vim: tabstop=4 shiftwidth=4 softtabstop=4
# Copyright (c) 2010-2011 OpenStack, LLC.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or
# implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import httplib2
import json
from lxml import etree
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.abspath(__file__),
                                '..', '..', '..', '..', '..', 'keystone')))
import unittest

import test_common as utils
from test_common import URL_V2

from keystone.logic.types import fault

class EndpointTemplatesTest(unittest.TestCase):
    def setUp(self):
        self.tenant = utils.get_tenant()
        self.password = utils.get_password()
        self.email = utils.get_email()
        self.user = utils.get_user()
        self.userdisabled = utils.get_userdisabled()
        self.auth_token = utils.get_auth_token()
        self.exp_auth_token = utils.get_exp_auth_token()
        self.disabled_token = utils.get_disabled_token()
        self.missing_token = utils.get_none_token()
        self.invalid_token = utils.get_non_existing_token()
        utils.create_tenant(self.tenant, str(self.auth_token))
        utils.create_user(self.tenant, self.user, self.auth_token)
        self.token = utils.get_token(self.user, 'secrete', self.tenant,
                                     'token')

    def tearDown(self):
        utils.delete_user(self.user, self.auth_token)
        utils.delete_tenant(self.tenant, self.auth_token)
        utils.delete_all_endpoint(self.tenant, self.auth_token)

class GetEndpointTemplatesTest(EndpointTemplatesTest):
    def test_get_endpoint_templates(self):
        header = httplib2.Http(".cache")
        url = '%sendpointTemplates' % (utils.URL_V2)
        #test for Content-Type = application/json
        resp, content = header.request(url, "GET", body='{}',
                                  headers={"Content-Type": "application/json",
                                         "X-Auth-Token": self.auth_token})
        if int(resp['status']) == 500:
            self.fail('Identity Fault')
        elif int(resp['status']) == 503:
            self.fail('Service Not Available')
        self.assertEqual(200, int(resp['status']))
        
        #verify content
        obj = json.loads(content)
        if not "endpointTemplates" in obj:
            raise self.fail("Expecting endpointTemplates")

    def test_get_endpoint_templates_using_expired_auth_token(self):
        header = httplib2.Http(".cache")
        url = '%sendpointTemplates' % (utils.URL_V2)
        #test for Content-Type = application/json
        resp, _content = header.request(url, "GET", body='{}',
                                  headers={"Content-Type": "application/json",
                                         "X-Auth-Token": self.exp_auth_token})
        if int(resp['status']) == 500:
            self.fail('Identity Fault')
        elif int(resp['status']) == 503:
            self.fail('Service Not Available')
        self.assertEqual(403 , int(resp['status']))            

    def test_get_endpoint_templates_using_disabled_auth_token(self):
        header = httplib2.Http(".cache")
        url = '%sendpointTemplates' % (utils.URL_V2)
        #test for Content-Type = application/json
        resp, _content = header.request(url, "GET", body='{}',
                                  headers={"Content-Type": "application/json",
                                         "X-Auth-Token": self.disabled_token})
        if int(resp['status']) == 500:
            self.fail('Identity Fault')
        elif int(resp['status']) == 503:
            self.fail('Service Not Available')
        self.assertEqual(403 , int(resp['status']))

    def test_get_endpoint_templates_using_missing_auth_token(self):
        header = httplib2.Http(".cache")
        url = '%sendpointTemplates' % (utils.URL_V2)
        #test for Content-Type = application/json
        resp, _content = header.request(url, "GET", body='{}',
                                  headers={"Content-Type": "application/json",
                                         "X-Auth-Token": self.missing_token})
        if int(resp['status']) == 500:
            self.fail('Identity Fault')
        elif int(resp['status']) == 503:
            self.fail('Service Not Available')
        self.assertEqual(401 , int(resp['status']))

    def test_get_endpoint_templates_using_invalid_auth_token(self):
        header = httplib2.Http(".cache")
        url = '%sendpointTemplates' % (utils.URL_V2)
        #test for Content-Type = application/json
        resp, _content = header.request(url, "GET", body='{}',
                                  headers={"Content-Type": "application/json",
                                         "X-Auth-Token": self.invalid_token})
        if int(resp['status']) == 500:
            self.fail('Identity Fault')
        elif int(resp['status']) == 503:
            self.fail('Service Not Available')
        self.assertEqual(404 , int(resp['status']))

    def test_get_endpoint_templates_xml(self):
        header = httplib2.Http(".cache")
        url = '%sendpointTemplates' % (utils.URL_V2)
        #test for Content-Type = application/json
        resp, content = header.request(url, "GET", body='{}',
                                  headers={"Content-Type": "application/xml",
                                         "X-Auth-Token": self.auth_token,
                                         "ACCEPT": "application/xml"})
        if int(resp['status']) == 500:
            self.fail('Identity Fault')
        elif int(resp['status']) == 503:
            self.fail('Service Not Available')
        self.assertEqual(200, int(resp['status']))
        
        #verify content
        dom = etree.Element("root")
        dom.append(etree.fromstring(content))
        endpoint_templates = dom.find(
            "{http://docs.openstack.org/identity/api/v2.0}endpointTemplates")
        if endpoint_templates == None:
            self.fail("Expecting endpointTemplates")

    def test_get_endpoint_templates_xml_expired_auth_token(self):
        header = httplib2.Http(".cache")
        url = '%sendpointTemplates' % (utils.URL_V2)
        #test for Content-Type = application/json
        resp, _content = header.request(url, "GET", body='{}',
                                  headers={"Content-Type": "application/xml",
                                         "X-Auth-Token": self.exp_auth_token,
                                         "ACCEPT": "application/xml"})
        if int(resp['status']) == 500:
            self.fail('Identity Fault')
        elif int(resp['status']) == 503:
            self.fail('Service Not Available')
        self.assertEqual(403, int(resp['status']))
        
    def test_get_endpoint_templates_xml_disabled_auth_token(self):
        header = httplib2.Http(".cache")
        url = '%sendpointTemplates' % (utils.URL_V2)
        #test for Content-Type = application/json
        resp, _content = header.request(url, "GET", body='{}',
                                  headers={"Content-Type": "application/xml",
                                         "X-Auth-Token": self.disabled_token,
                                         "ACCEPT": "application/xml"})
        if int(resp['status']) == 500:
            self.fail('Identity Fault')
        elif int(resp['status']) == 503:
            self.fail('Service Not Available')
        self.assertEqual(403, int(resp['status']))

    def test_get_endpoint_templates_xml_missing_auth_token(self):
        header = httplib2.Http(".cache")
        url = '%sendpointTemplates' % (utils.URL_V2)
        #test for Content-Type = application/json
        resp, _content = header.request(url, "GET", body='{}',
                                  headers={"Content-Type": "application/xml",
                                         "X-Auth-Token": self.missing_token,
                                         "ACCEPT": "application/xml"})
        if int(resp['status']) == 500:
            self.fail('Identity Fault')
        elif int(resp['status']) == 503:
            self.fail('Service Not Available')
        self.assertEqual(401, int(resp['status']))

    def test_get_endpoint_templates_xml_invalid_auth_token(self):
        header = httplib2.Http(".cache")
        url = '%sendpointTemplates' % (utils.URL_V2)
        #test for Content-Type = application/json
        resp, _content = header.request(url, "GET", body='{}',
                                  headers={"Content-Type": "application/xml",
                                         "X-Auth-Token": self.invalid_token,
                                         "ACCEPT": "application/xml"})
        if int(resp['status']) == 500:
            self.fail('Identity Fault')
        elif int(resp['status']) == 503:
            self.fail('Service Not Available')
        self.assertEqual(404, int(resp['status']))
                         
class GetEndpointTemplateTest(EndpointTemplatesTest):
    def test_get_endpoint(self):
        header = httplib2.Http(".cache")
        url = '%sendpointTemplates/%s' % (utils.URL_V2, '1')
        #test for Content-Type = application/json
        resp, content = header.request(url, "GET", body='{}',
                                  headers={"Content-Type": "application/json",
                                         "X-Auth-Token": self.auth_token})
        if int(resp['status']) == 500:
            self.fail('Identity Fault')
        elif int(resp['status']) == 503:
            self.fail('Service Not Available')
        self.assertEqual(200, int(resp['status']))
        
        #verify content
        obj = json.loads(content)
        if not "endpointTemplate" in obj:
            raise self.fail("Expecting endpointTemplate")

    def test_get_endpoint_using_expired_auth_token(self):
        header = httplib2.Http(".cache")
        url = '%sendpointTemplates/%s' % (utils.URL_V2, '1')
        #test for Content-Type = application/json
        resp, _content = header.request(url, "GET", body='{}',
                                  headers={"Content-Type": "application/json",
                                         "X-Auth-Token": self.exp_auth_token})
        if int(resp['status']) == 500:
            self.fail('Identity Fault')
        elif int(resp['status']) == 503:
            self.fail('Service Not Available')
        self.assertEqual(403, int(resp['status']))

    def test_get_endpoint_using_disabled_auth_token(self):
        header = httplib2.Http(".cache")
        url = '%sendpointTemplates/%s' % (utils.URL_V2, '1')
        #test for Content-Type = application/json
        resp, _content = header.request(url, "GET", body='{}',
                                  headers={"Content-Type": "application/json",
                                         "X-Auth-Token": self.disabled_token})
        if int(resp['status']) == 500:
            self.fail('Identity Fault')
        elif int(resp['status']) == 503:
            self.fail('Service Not Available')
        self.assertEqual(403, int(resp['status']))

    def test_get_endpoint_using_missing_auth_token(self):
        header = httplib2.Http(".cache")
        url = '%sendpointTemplates/%s' % (utils.URL_V2, '1')
        #test for Content-Type = application/json
        resp, _content = header.request(url, "GET", body='{}',
                                  headers={"Content-Type": "application/json",
                                         "X-Auth-Token": self.missing_token})
        if int(resp['status']) == 500:
            self.fail('Identity Fault')
        elif int(resp['status']) == 503:
            self.fail('Service Not Available')
        self.assertEqual(401, int(resp['status']))


    def test_get_endpoint_using_invalid_auth_token(self):
        header = httplib2.Http(".cache")
        url = '%sendpointTemplates/%s' % (utils.URL_V2, '1')
        #test for Content-Type = application/json
        resp, _content = header.request(url, "GET", body='{}',
                                  headers={"Content-Type": "application/json",
                                         "X-Auth-Token": self.invalid_token})
        if int(resp['status']) == 500:
            self.fail('Identity Fault')
        elif int(resp['status']) == 503:
            self.fail('Service Not Available')
        self.assertEqual(404, int(resp['status']))

    def test_get_endpoint_xml(self):
        header = httplib2.Http(".cache")
        url = '%sendpointTemplates/%s' % (utils.URL_V2, '1')
        #test for Content-Type = application/json
        resp, content = header.request(url, "GET", body='{}',
                                  headers={"Content-Type": "application/xml",
                                         "X-Auth-Token": self.auth_token,
                                         "ACCEPT": "application/xml"})
        if int(resp['status']) == 500:
            self.fail('Identity Fault')
        elif int(resp['status']) == 503:
            self.fail('Service Not Available')
        self.assertEqual(200, int(resp['status']))
        
        #verify content
        dom = etree.Element("root")
        dom.append(etree.fromstring(content))
        endpoint = dom.find("{http://docs.openstack.org/identity/api/v2.0}" \
            "endpointTemplate")
        if endpoint == None:
            self.fail("Expecting endpointTemplate")

class CreateEndpointRefsTest(EndpointTemplatesTest):
    def test_endpoint_create_json_using_expired_token(self):
        _header = httplib2.Http(".cache")
        resp, _content = utils.create_endpoint(self.tenant, "1",
            str(self.exp_auth_token))
        resp_val = int(resp['status'])
        self.assertEqual(403, resp_val)

    def test_endpoint_create_json_using_disabled_token(self):
        _header = httplib2.Http(".cache")
        resp, _content = utils.create_endpoint(self.tenant, "1",
            str(self.disabled_token))
        resp_val = int(resp['status'])
        self.assertEqual(403, resp_val)

    def test_endpoint_create_json_using_missing_token(self):
        _header = httplib2.Http(".cache")
        resp, _content = utils.create_endpoint(self.tenant, "1",
            str(self.missing_token))
        resp_val = int(resp['status'])
        self.assertEqual(401, resp_val)

    def test_endpoint_create_json_using_invalid_token(self):
        _header = httplib2.Http(".cache")
        resp, _content = utils.create_endpoint(self.tenant, "1",
            str(self.invalid_token))
        resp_val = int(resp['status'])
        self.assertEqual(404, resp_val)
    
    def test_endpoint_create_xml(self):
        header = httplib2.Http(".cache")
        
        resp, _content = utils.create_endpoint_xml(self.tenant, "1",
            str(self.auth_token))
        resp_val = int(resp['status'])
        self.assertEqual(201, resp_val)
        url = '%stenants/%s/endpoints/%s' % (URL_V2, self.tenant, '1')
        resp, _content = header.request(url, "DELETE", body='', headers={
            "Content-Type": "application/json",
            "X-Auth-Token": str(self.auth_token)})
        resp_val = int(resp['status'])
        self.assertEqual(204, resp_val)

    def test_endpoint_create_xml_using_expired_token(self):
        header = httplib2.Http(".cache")
        
        resp, _content = utils.create_endpoint_xml(self.tenant, "1",
            str(self.auth_token))
        resp_val = int(resp['status'])
        self.assertEqual(201, resp_val)
        url = '%stenants/%s/endpoints/%s' % (URL_V2, self.tenant, '1')
        resp, _content = header.request(url, "DELETE", body='', headers={
            "Content-Type": "application/json",
            "X-Auth-Token": str(self.exp_auth_token)})
        resp_val = int(resp['status'])
        self.assertEqual(403, resp_val)
        
    def test_endpoint_create_xml_using_disabled_token(self):
        header = httplib2.Http(".cache")
        
        resp, _content = utils.create_endpoint_xml(self.tenant, "1",
            str(self.auth_token))
        resp_val = int(resp['status'])
        self.assertEqual(201, resp_val)
        url = '%stenants/%s/endpoints/%s' % (URL_V2, self.tenant, '1')
        resp, _content = header.request(url, "DELETE", body='', headers={
            "Content-Type": "application/json",
            "X-Auth-Token": str(self.disabled_token)})
        resp_val = int(resp['status'])
        self.assertEqual(403, resp_val)

    def test_endpoint_create_xml_using_missing_token(self):
        header = httplib2.Http(".cache")
        
        resp, _content = utils.create_endpoint_xml(self.tenant, "1",
            str(self.auth_token))
        resp_val = int(resp['status'])
        self.assertEqual(201, resp_val)
        url = '%stenants/%s/endpoints/%s' % (URL_V2, self.tenant, '1')
        resp, _content = header.request(url, "DELETE", body='', headers={
            "Content-Type": "application/json",
            "X-Auth-Token": str(self.missing_token)})
        resp_val = int(resp['status'])
        self.assertEqual(401, resp_val)

    def test_endpoint_create_xml_using_invalid_token(self):
        header = httplib2.Http(".cache")
        
        resp, _content = utils.create_endpoint_xml(self.tenant, "1",
            str(self.auth_token))
        resp_val = int(resp['status'])
        self.assertEqual(201, resp_val)
        url = '%stenants/%s/endpoints/%s' % (URL_V2, self.tenant, '1')
        resp, _content = header.request(url, "DELETE", body='', headers={
            "Content-Type": "application/json",
            "X-Auth-Token": str(self.invalid_token)})
        resp_val = int(resp['status'])
        self.assertEqual(404, resp_val)

class GetEndPointTest(EndpointTemplatesTest):    
    def test_get_endpoint_xml(self):
        header = httplib2.Http(".cache")
        url = '%stenants/%s/endpoints' % (URL_V2, self.tenant)
        #test for Content-Type = application/xml
        resp, _content = header.request(url, "GET", body='{}', headers={
            "Content-Type": "application/xml",
            "X-Auth-Token": str(self.auth_token),
            "ACCEPT": "application/xml"})
        if int(resp['status']) == 500:
            self.fail('Identity Fault')
        elif int(resp['status']) == 503:
            self.fail('Service Not Available')
        self.assertEqual(200, int(resp['status']))
        
    def test_get_endpoint_xml_using_expired_auth_token(self):
        header = httplib2.Http(".cache")
        url = '%stenants/%s/endpoints' % (URL_V2, self.tenant)
        #test for Content-Type = application/xml
        resp, _content = header.request(url, "GET", body='{}', headers={
            "Content-Type": "application/xml",
            "X-Auth-Token": str(self.exp_auth_token),
            "ACCEPT": "application/xml"})
        if int(resp['status']) == 500:
            self.fail('Identity Fault')
        elif int(resp['status']) == 503:
            self.fail('Service Not Available')
        self.assertEqual(403, int(resp['status']))

    def test_get_endpoint_xml_using_disabled_auth_token(self):
        header = httplib2.Http(".cache")
        url = '%stenants/%s/endpoints' % (URL_V2, self.tenant)
        #test for Content-Type = application/xml
        resp, _content = header.request(url, "GET", body='{}', headers={
            "Content-Type": "application/xml",
            "X-Auth-Token": str(self.disabled_token),
            "ACCEPT": "application/xml"})
        if int(resp['status']) == 500:
            self.fail('Identity Fault')
        elif int(resp['status']) == 503:
            self.fail('Service Not Available')
        self.assertEqual(403, int(resp['status']))

    def test_get_endpoint_xml_using_missing_auth_token(self):
        header = httplib2.Http(".cache")
        url = '%stenants/%s/endpoints' % (URL_V2, self.tenant)
        #test for Content-Type = application/xml
        resp, _content = header.request(url, "GET", body='{}', headers={
            "Content-Type": "application/xml",
            "X-Auth-Token": str(self.missing_token),
            "ACCEPT": "application/xml"})
        if int(resp['status']) == 500:
            self.fail('Identity Fault')
        elif int(resp['status']) == 503:
            self.fail('Service Not Available')
        self.assertEqual(401, int(resp['status']))

    def test_get_endpoint_xml_using_invalid_auth_token(self):
        header = httplib2.Http(".cache")
        url = '%stenants/%s/endpoints' % (URL_V2, self.tenant)
        #test for Content-Type = application/xml
        resp, _content = header.request(url, "GET", body='{}', headers={
            "Content-Type": "application/xml",
            "X-Auth-Token": str(self.invalid_token),
            "ACCEPT": "application/xml"})
        if int(resp['status']) == 500:
            self.fail('Identity Fault')
        elif int(resp['status']) == 503:
            self.fail('Service Not Available')
        self.assertEqual(404, int(resp['status']))
        
    def test_get_endpoint_json(self):
        header = httplib2.Http(".cache")
        url = '%stenants/%s/endpoints' % (URL_V2, self.tenant)
        #test for Content-Type = application/json
        resp, content = header.request(url, "GET", body='{}', headers={
            "Content-Type": "application/json",
            "X-Auth-Token": str(self.auth_token),
            "ACCEPT": "application/json"})
        if int(resp['status']) == 500:
            self.fail('Identity Fault')
        elif int(resp['status']) == 503:
            self.fail('Service Not Available')
        self.assertEqual(200, int(resp['status']))
        obj = json.loads(content)
        if not "endpoints" in obj:
            raise self.fail("Expecting endpoints")

    def test_get_endpoint_json_using_expired_auth_token(self):
        header = httplib2.Http(".cache")
        url = '%stenants/%s/endpoints' % (URL_V2, self.tenant)
        #test for Content-Type = application/json
        resp, content = header.request(url, "GET", body='{}',
            headers={"Content-Type": "application/json",
                "X-Auth-Token": str(self.exp_auth_token),
                "ACCEPT": "application/json"})
        if int(resp['status']) == 500:
            self.fail('Identity Fault')
        elif int(resp['status']) == 503:
            self.fail('Service Not Available')
        self.assertEqual(403, int(resp['status']))
        _obj = json.loads(content)

    def test_get_endpoint_json_using_disabled_auth_token(self):
        header = httplib2.Http(".cache")
        url = '%stenants/%s/endpoints' % (URL_V2, self.tenant)
        #test for Content-Type = application/json
        resp, content = header.request(url, "GET", body='{}', headers={
            "Content-Type": "application/json",
            "X-Auth-Token": str(self.disabled_token),
            "ACCEPT": "application/json"})
        if int(resp['status']) == 500:
            self.fail('Identity Fault')
        elif int(resp['status']) == 503:
            self.fail('Service Not Available')
        self.assertEqual(403, int(resp['status']))
        _obj = json.loads(content)

    def test_get_endpoint_json_using_missing_auth_token(self):
        header = httplib2.Http(".cache")
        url = '%stenants/%s/endpoints' % (URL_V2, self.tenant)
        #test for Content-Type = application/json
        resp, content = header.request(url, "GET", body='{}', headers={
            "Content-Type": "application/json",
            "X-Auth-Token": str(self.missing_token),
            "ACCEPT": "application/json"})
        if int(resp['status']) == 500:
            self.fail('Identity Fault')
        elif int(resp['status']) == 503:
            self.fail('Service Not Available')
        self.assertEqual(401, int(resp['status']))
        _obj = json.loads(content)

    def test_get_endpoint_json_using_invalid_auth_token(self):
        header = httplib2.Http(".cache")
        url = '%stenants/%s/endpoints' % (URL_V2, self.tenant)
        #test for Content-Type = application/json
        resp, content = header.request(url, "GET", body='{}', headers={
            "Content-Type": "application/json",
            "X-Auth-Token": str(self.invalid_token),
            "ACCEPT": "application/json"})
        if int(resp['status']) == 500:
            self.fail('Identity Fault')
        elif int(resp['status']) == 503:
            self.fail('Service Not Available')
        self.assertEqual(404, int(resp['status']))
        _obj = json.loads(content)

class DeleteEndpointsTest(EndpointTemplatesTest):            
    def test_delete_endpoint(self):
        header = httplib2.Http(".cache")
        resp, content = utils.create_endpoint(self.tenant, "1",
            str(self.auth_token))
        resp_val = int(resp['status'])
        self.assertEqual(201, resp_val)
        obj = json.loads(content)
        if not "endpoint" in obj:
            raise fault.BadRequestFault("Expecting endpoint")
        endpoint = obj["endpoint"]
        if not "id" in endpoint:
            endpoint_id = None
        else:
            endpoint_id = endpoint["id"]
        if endpoint_id is None:
            raise fault.BadRequestFault("Expecting endpointID")
        url = '%stenants/%s/endpoints/%s' % (URL_V2, self.tenant, endpoint_id)
        resp, content = header.request(url, "DELETE", body='', headers={
            "Content-Type": "application/json",
            "X-Auth-Token": str(self.auth_token)})
        resp_val = int(resp['status'])
        self.assertEqual(204, resp_val)

    def test_delete_endpoint_using_expired_auth_token(self):
        header = httplib2.Http(".cache")
        resp, content = utils.create_endpoint(self.tenant, "1",
            str(self.auth_token))
        resp_val = int(resp['status'])
        self.assertEqual(201, resp_val)
        obj = json.loads(content)
        if not "endpoint" in obj:
            raise fault.BadRequestFault("Expecting endpoint")
        endpoint = obj["endpoint"]
        if not "id" in endpoint:
            endpoint_id = None
        else:
            endpoint_id = endpoint["id"]
        if endpoint_id is None:
            raise fault.BadRequestFault("Expecting endpoint id")
        url = '%stenants/%s/endpoints/%s' % (URL_V2, self.tenant, endpoint_id)
        resp, content = header.request(url, "DELETE", body='', headers={
            "Content-Type": "application/json",
            "X-Auth-Token": str(self.exp_auth_token)})
        resp_val = int(resp['status'])
        self.assertEqual(403, resp_val)

    def test_delete_endpoint_using_disabled_auth_token(self):
        header = httplib2.Http(".cache")
        resp, content = utils.create_endpoint(self.tenant, "1",
            str(self.auth_token))
        resp_val = int(resp['status'])
        self.assertEqual(201, resp_val)
        obj = json.loads(content)
        if not "endpoint" in obj:
            raise fault.BadRequestFault("Expecting endpoint")
        endpoint = obj["endpoint"]
        if not "id" in endpoint:
            endpoint_id = None
        else:
            endpoint_id = endpoint["id"]
        if endpoint_id is None:
            raise fault.BadRequestFault("Expecting endpoint id")
        url = '%stenants/%s/endpoints/%s' % (URL_V2, self.tenant, endpoint_id)
        resp, content = header.request(url, "DELETE", body='', headers={
            "Content-Type": "application/json",
            "X-Auth-Token": str(self.disabled_token)})
        resp_val = int(resp['status'])
        self.assertEqual(403, resp_val)
 
    def test_delete_endpoint_using_missing_auth_token(self):
        header = httplib2.Http(".cache")
        resp, content = utils.create_endpoint(self.tenant, "1",
            str(self.auth_token))
        resp_val = int(resp['status'])
        self.assertEqual(201, resp_val)
        obj = json.loads(content)
        if not "endpoint" in obj:
            raise fault.BadRequestFault("Expecting endpoint")
        endpoint = obj["endpoint"]
        if not "id" in endpoint:
            endpoint_id = None
        else:
            endpoint_id = endpoint["id"]
        if endpoint_id is None:
            raise fault.BadRequestFault("Expecting endpointID")
        url = '%stenants/%s/endpoints/%s' % (URL_V2, self.tenant, endpoint_id)
        resp, content = header.request(url, "DELETE", body='', headers={
            "Content-Type": "application/json",
            "X-Auth-Token": str(self.missing_token)})
        resp_val = int(resp['status'])
        self.assertEqual(401, resp_val)

    def test_delete_endpoint_using_invalid_auth_token(self):
        header = httplib2.Http(".cache")
        resp, content = utils.create_endpoint(self.tenant, "1",
            str(self.auth_token))
        resp_val = int(resp['status'])
        self.assertEqual(201, resp_val)
        obj = json.loads(content)
        if not "endpoint" in obj:
            raise fault.BadRequestFault("Expecting endpoint")
        endpoint = obj["endpoint"]
        if not "id" in endpoint:
            endpoint_id = None
        else:
            endpoint_id = endpoint["id"]
        if endpoint_id is None:
            raise fault.BadRequestFault("Expecting endpoint ID")
        url = '%stenants/%s/endpoints/%s' % (URL_V2, self.tenant, endpoint_id)
        resp, content = header.request(url, "DELETE", body='', headers={
            "Content-Type": "application/json",
            "X-Auth-Token": str(self.invalid_token)})
        resp_val = int(resp['status'])
        self.assertEqual(404, resp_val)

if __name__ == '__main__':
    unittest.main()
