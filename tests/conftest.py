import pytest
from main import app
import os
import requests
from faker import Faker
import random
from playwright.sync_api import Playwright, APIRequestContext
from typing import Generator

@pytest.fixture(scope='session', autouse=True)
def faker_session_locale():
    return ['it_IT', 'en_US']

@pytest.fixture(scope='session', autouse=True)
def faker_seed():
    return random.randint(0,100)

@pytest.fixture(scope="session")
def client(
    playwright: Playwright,payload
) -> Generator[APIRequestContext, None, None]:
    headers,company_id,user_id = payload
    request_context = playwright.request.new_context(
        base_url=f"https://slooviassessment.herokuapp.com", extra_http_headers=headers
    )
    yield request_context
    request_context.dispose()

@pytest.fixture(scope='session', autouse=True)
def payload(): 
    response = requests.post("https://slooviassessment.herokuapp.com/login",json={"email":"sam@gmail.com","password":"12345"}).json()
    res = response
    headers = {'Authorization': f'Bearer {res["token"]}'}
    email= res['email']
    id = res['_id']
    return headers, email, id

