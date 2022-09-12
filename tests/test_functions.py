import json
from telnetlib import SE
from unicodedata import name
from unittest import result
from faker import Faker
from playwright.sync_api import Playwright, APIRequestContext


fake = Faker()

def test_register(client: APIRequestContext, faker):
    """
        Register an account
    """
    first_name = fake.first_name_male()
    last_name = fake.last_name()
    domain_name = fake.domain_name()
    
    body = dict(first_name=first_name,last_name=last_name,email=f"{first_name}{last_name}@{domain_name}.com", password=first_name +last_name)


    # body_1 = dict(first_name=first_name,last_name=last_name,email="{first_name}{last_name}@{domain_name}.com", password='johndoe')
    response = client.post(f'/register', data=body).json()
    # response_1 = client.post(f'/register', data=body_1).json()
    
    assert response
    assert response['_id']

def test_wrong_register_email(client: APIRequestContext, faker):   
    first_name_1 = fake.first_name_male()
    last_name_1 = fake.last_name()
    domain_name_1 = fake.domain_name()
    
    body_1 = dict(first_name=first_name_1,last_name=last_name_1,email=f"{first_name_1}{last_name_1}{domain_name_1}.com", password=first_name_1 +last_name_1)
    
    response_1 = client.post(f"/register", data=body_1).json()
    print(response_1)
    assert response_1.get("message") == 'Email format not vailid'



def test_login(client: APIRequestContext, faker):
    first_name = fake.first_name_male()
    last_name = fake.last_name()
    domain_name = fake.domain_name()
    
    
    
    body = dict(first_name=first_name,last_name=last_name,email=f"{first_name}{last_name}@{domain_name}.com", password=first_name +last_name)

    client.post(f'/register', data=body).json()
    
    login_body = dict(email=f"{first_name}{last_name}@{domain_name}.com", password=first_name +last_name)
    
    login_response = client.post(f'/login', data=login_body).json()
    
    assert "_id" in login_response
    assert "token" in login_response
    
def test_wrong_login(client: APIRequestContext, faker):
    first_name = fake.first_name_male()
    last_name = fake.last_name()
    domain_name = fake.domain_name()
    
    
    
    body = dict(first_name=first_name,last_name=last_name,email=f"{first_name}{last_name}@{domain_name}.com", password=first_name +last_name)

    client.post(f'/register', data=body).json()
    login_body = dict(email=f"{first_name}{last_name}@{domain_name}.com", password="wrong password")
    login_response = client.post(f'/login', data=login_body).json()
    
    assert login_response["message"] == 'Could not validate credentials'
   
    

def test_template_create(client: APIRequestContext,payload, faker):
    
    headers, email, id  = payload
    template_body = {
          "template_name": "My first template",
          "subject": "about templates",
          "body": "This iis the body of my first template"
    }
    post_template = client.post(f'/template', data=template_body, headers = headers).json()
    assert post_template ==  "Successful"
    
def test_incorrect_template_create(client: APIRequestContext,payload, faker):
    headers, email, id  = payload
    template_body = {
          "template_name": "My error template",
         
          "body": "This is the body of my first template"
    }
    post_template = client.post(f'/template', data=template_body, headers = headers).json()
    
    assert post_template['message']['subject'] == 'Input template subject'

def test_template_retrieve(client: APIRequestContext,payload, faker):
    headers, email, id  = payload
    get_templates_request = client.get(f'/template', headers = headers)
    get_templates = get_templates_request.json()
    assert get_templates_request.status == 200
    assert type(get_templates) == list
    
    
def test_template_retrieve_single(client: APIRequestContext,payload, faker):
    headers, email, id  = payload
    get_templates_request = client.get(f'/template', headers = headers)
    get_templates = get_templates_request.json()    
    temp_1_id = get_templates[0]["_id"]
    
    get_template_request = client.get(f'/template/{temp_1_id}', headers = headers)
    json_for_temp = get_template_request.json()
    assert get_template_request.status == 200
    assert "body" in json_for_temp
    
def test_template_update_single(client: APIRequestContext,payload, faker):
    headers, email, id  = payload
    get_templates_request = client.get(f'/template', headers = headers)
    get_templates = get_templates_request.json()    
    temp_1_id = get_templates[0]["_id"]
    
    body = {"body": "Modified "}
    get_template_request = client.put(f'/template/{temp_1_id}', data = body, headers = headers)
    assert get_template_request.status == 204
    

def test_template_update_delete(client: APIRequestContext,payload, faker):
    headers, email, id  = payload
    get_templates_request = client.get(f'/template', headers = headers)
    get_templates = get_templates_request.json()    
    temp_1_id = get_templates[len(get_templates) - 1]["_id"]
    
    get_template_request = client.delete(f'/template/{temp_1_id}', headers = headers)
    assert get_template_request.status == 204
#     global template_id # declare global variable for use in other test case
#     global template_name
#     res = response['results']
#     template_id = res['id']
#     template_name = res['name']
    
#     data = Search(using=db, index=default_index).query(Q('bool', must=[Q('match_phrase', id=template_id)])).execute()[0].to_dict()
#     if not data:
#         assert response['code'] == 500
#         assert response['module'] == "Templates"
#         assert response['message'] == "Something Went Wrong, Pls try Again Later"
#     else:
#         assert response['code'] == 201
#         assert response['code'] != 500
#         assert response['module'] == "Templates"
#         assert response['message'] == "New email template created successfully."
#         assert len(res) > 0
#         assert res['is_delete'] == 0
#         assert res['status'] == 1
#         assert res['company_id'] == company_id
#         assert res['name'] == body['name']
#         assert res['subject'] == body['subject']
#         assert res['tag'] == body['tag']
#         assert res['is_shared'] == body['is_shared']
#         assert res['body'] == body['body']
#         assert res['modified_by'] == user_id
#         assert res['id'].startswith("template")

#         assert body['name'] == data['name']
#         assert body['subject'] == data['subject']
#         assert body['tag'] == data['tag']
#         assert body['is_shared'] == data['is_shared']
#         assert body['body'] == data['body']

# def test_create_duplicate_template(client:APIRequestContext,db,payload,faker):
#     """
#     GIVEN Create a duplicate Template
#     WHEN a new template is created with the '/template' (POST)
#     THEN check whether a duplicate template is not created
#     """
#     headers,company_id,user_id = payload
#     data = Search(using=db, index=default_index).query(Q('bool', must=[Q('match_phrase', name=template_name)])).execute()[0].to_dict()

#     body = dict(name=template_name,subject=faker.words(1)[0],tag=faker.words(1)[0],is_shared= 1 if faker.pybool() else 0,attachments=[],body="<p id=\"isPasted\" style=\"margin-top:10.0pt;margin-right:0cm;margin-bottom:  10.0pt;margin-left:0cm;line-height:120%;\">Hi &nbsp;{{first}},</p><p style=\"margin-top:10.0pt;margin-right:0cm;margin-bottom:  10.0pt;margin-left:0cm;line-height:120%;\">What if you never again have to deal with expensive marketing agencies, unreliable freelancers, and in-house graphic designers?</p><p style=\"margin-top:10.0pt;margin-right:0cm;margin-bottom:  10.0pt;margin-left:0cm;line-height:120%;\">All Time Design is the remote graphic design service platform you’ve been looking for:</p><p style=\"margin-top:10.0pt;margin-right:0cm;margin-bottom:  10.0pt;margin-left:18.0pt;line-height:120%;\">1. &nbsp; &nbsp; &nbsp;Countless graphic designs (at an affordable monthly rate)</p><p style=\"margin-top:10.0pt;margin-right:0cm;margin-bottom:  10.0pt;margin-left:18.0pt;line-height:120%;\">2. &nbsp; &nbsp; &nbsp;14-day trial - cancel anytime (we bet you won’t)</p><p style=\"margin-top:10.0pt;margin-right:0cm;margin-bottom:  10.0pt;margin-left:18.0pt;line-height:120%;\">3. &nbsp; &nbsp; &nbsp;Countless revisions (no exaggeration)</p><p style=\"margin-top:10.0pt;margin-right:0cm;margin-bottom:  10.0pt;margin-left:18.0pt;line-height:120%;\">4. &nbsp; &nbsp; &nbsp;Turnaround time of 24 to 48 hours (express delivery)</p><p style=\"margin-top:10.0pt;margin-right:0cm;margin-bottom:  10.0pt;margin-left:0cm;line-height:120%;\"><a href=\"http://bit.ly/atdshow\">Take a look at what we’ve done for other clients.</a></p><p style=\"margin-top:10.0pt;margin-right:0cm;margin-bottom:  10.0pt;margin-left:0cm;line-height:120%;\">Want to know more? Please call me anytime, or <a href=\"https://calendly.com/alltimedesign/meeting\">schedule a meeting here﻿</a></p>")
#     print(body)
#     response = client.post(f'/template?company_id={company_id}', data=body, headers=headers).json()
#     result = response['results']
#     assert response['code'] == 400
#     assert response['code'] != 500
#     assert response['module'] == "Templates"
#     assert response['message'] == "Validation error"
#     assert body['name'] == data['name']
#     assert len(result) > 0
#     for res in result:
#         assert len(res['key']) > 0
#         if res['key'] == "name":
#             assert res['msg'] == "Template name already exists."

# def test_update_template(client:APIRequestContext,db,payload,faker):
#     """
#     GIVEN Update a Template
#     WHEN a new template is updated with the '/template' (PUT)
#     THEN check whether the template is updated
#     """
#     headers,company_id,user_id = payload
    
#     body = dict(name=template_name,subject=faker.words(1)[0],tag=faker.words(1)[0],status=1,is_shared= 1 if faker.pybool() else 0,attachments=[],body="<p id=\"isPasted\" style=\"margin-top:10.0pt;margin-right:0cm;margin-bottom:  10.0pt;margin-left:0cm;line-height:120%;\">Hi &nbsp;{{first}},</p><p style=\"margin-top:10.0pt;margin-right:0cm;margin-bottom:  10.0pt;margin-left:0cm;line-height:120%;\">What if you never again have to deal with expensive marketing agencies, unreliable freelancers, and in-house graphic designers?</p><p style=\"margin-top:10.0pt;margin-right:0cm;margin-bottom:  10.0pt;margin-left:0cm;line-height:120%;\">All Time Design is the remote graphic design service platform you’ve been looking for:</p><p style=\"margin-top:10.0pt;margin-right:0cm;margin-bottom:  10.0pt;margin-left:18.0pt;line-height:120%;\">1. &nbsp; &nbsp; &nbsp;Countless graphic designs (at an affordable monthly rate)</p><p style=\"margin-top:10.0pt;margin-right:0cm;margin-bottom:  10.0pt;margin-left:18.0pt;line-height:120%;\">2. &nbsp; &nbsp; &nbsp;14-day trial - cancel anytime (we bet you won’t)</p><p style=\"margin-top:10.0pt;margin-right:0cm;margin-bottom:  10.0pt;margin-left:18.0pt;line-height:120%;\">3. &nbsp; &nbsp; &nbsp;Countless revisions (no exaggeration)</p><p style=\"margin-top:10.0pt;margin-right:0cm;margin-bottom:  10.0pt;margin-left:18.0pt;line-height:120%;\">4. &nbsp; &nbsp; &nbsp;Turnaround time of 24 to 48 hours (express delivery)</p><p style=\"margin-top:10.0pt;margin-right:0cm;margin-bottom:  10.0pt;margin-left:0cm;line-height:120%;\"><a href=\"http://bit.ly/atdshow\">Take a look at what we’ve done for other clients.</a></p><p style=\"margin-top:10.0pt;margin-right:0cm;margin-bottom:  10.0pt;margin-left:0cm;line-height:120%;\">Want to know more? Please call me anytime, or <a href=\"https://calendly.com/alltimedesign/meeting\">schedule a meeting here﻿</a></p>")
#     # print(body)
#     response = client.put(f'/template/{template_id}?company_id={company_id}', data=body, headers=headers).json()
#     res = response['results']
#     data = Search(using=db, index=default_index).query(Q('bool', must=[Q('match_phrase', id=res['id'])])).execute()[0].to_dict()
#     # print(response.json)
#     assert response['code'] == 202
#     assert response['code'] != 500
#     assert response['module'] == "Templates"
#     assert response['message'] == "Updated successfully"
#     assert len(res) > 0
#     assert res['is_delete'] == 0
#     assert res['status'] == 1
#     assert res['company_id'] == company_id
#     assert res['name'] == body['name']
#     assert res['subject'] == body['subject']
#     assert res['tag'] == body['tag']
#     assert res['is_shared'] == body['is_shared']
#     assert res['body'] == body['body']
#     assert res['modified_by'] == user_id
#     assert res['id'].startswith("template")

#     assert body['name'] == data['name']
#     assert body['subject'] == data['subject']
#     assert body['tag'] == data['tag']
#     assert body['is_shared'] == data['is_shared']
#     assert body['body'] == data['body']
#     assert body['status'] == data['status']

# def test_template(client:APIRequestContext,db,payload):
#     """
#     GIVEN GET a Template with template_id
#     WHEN the '/template/template_id' is requested (GET)
#     THEN check the response is valid
#     """
#     headers,company_id,user_id = payload
#     data = Search(using=db, index=default_index).query(Q('bool', must=[Q('match_phrase', id=template_id)])).execute()[0].to_dict()
#     print(data)
#     response = client.get(f'template/{template_id}?company_id={company_id}', headers=headers).json() 
#     print(response)
#     result = response['results']
#     assert response['code'] == 200
#     assert response['code'] != 500
#     assert response['module'] == "Templates"
#     assert response['message'] == "Fetched successfully"
#     assert len(result) > 0
#     assert result['is_delete'] == 0
#     assert result['company_id'] == company_id

#     assert result['name'] == data['name']
#     assert result['subject'] == data['subject']
#     assert result['tag'] == data['tag']
#     assert result['is_shared'] == data['is_shared']
#     assert result['body'] == data['body']
#     assert result['status'] == data['status']

# def test_delete_template(client:APIRequestContext,db,payload,faker):
#     """
#     GIVEN Delete a Template
#     WHEN a  template is deleted with the '/template' (DELETE)
#     THEN check whether the template is deleted
#     """
#     headers,company_id,user_id = payload
#     response = client.delete(f'/template/{template_id}?company_id={company_id}', headers=headers).json()
#     data = Search(using=db, index=default_index).query(Q('bool', must=[Q('match_phrase', id=template_id)])).execute()[0].to_dict()
#     # print(response.json)
#     assert response['code'] == 204
#     assert response['code'] != 500
#     assert response['module'] == "Templates"
#     assert response['message'] == "Email template deleted successfully."
#     assert data['is_delete'] == 1

# def test_all_templates(client: APIRequestContext,payload) -> None:
#     """
#     GIVEN GET all Templates
#     WHEN the '/template' is requested (GET)
#     THEN check whether templates are valid
#     """
#     headers,company_id,user_id = payload # token credentials
#     response = client.get(f'/template?company_id={company_id}', headers=headers).json()
#     result = response['results']
#     # Assert the response
#     assert response['module'] == "Templates"
#     assert response['code'] == 200
#     assert response['code'] != 500
#     assert response['message'] == "Fetched successfully"
#     assert len(result) > 0
#     for res in result:
#         assert res['is_delete'] == 0
#         assert res['company_id'] == company_id

# def test_deleted_template(client:APIRequestContext,db,payload):
#     """
#     GIVEN GET a Template with template_id
#     WHEN the '/template/template_id' is requested (GET)
#     THEN check whether the template is already deleted 
#     """
#     headers,company_id,user_id = payload
#     data = Search(using=db, index=default_index).query(Q('bool', must=[Q('match_phrase', id=template_id)])).execute()[0].to_dict()
#     print(data)
#     response = client.get(f'template/{template_id}?company_id={company_id}', headers=headers).json() 
#     print(response)
#     assert response['code'] == 404
#     assert response['code'] != 500
#     assert response['module'] == "Templates"
#     assert response['message'] == "Resource Was Deleted"