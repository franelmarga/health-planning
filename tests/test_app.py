# -*- coding: utf-8 -*-

import pytest
import requests
import os

# This tests aims to check if the db connection is successful by checking the length of the list of users
def test_get_all_users():
    url = 'http://127.0.0.1:5000/users' 
    response = requests.get(url)
    
    assert response.status_code == 200 
    
    data = response.json()  #bson response to a list
    
    assert isinstance(data, list)  
    
    assert len(data) >= 1 #checks if the list is empty


