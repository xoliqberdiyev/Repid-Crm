import os, sys
import logging
from datetime import date

from tests.conftest import create_test_auth_headers_for_user
from database.models import UserType


class TestProject:
    async def create_test_user(self,create_user_in_database, create_position_from_database):
        position = await create_position_from_database("Backend")

        user_data = {
            "username": "test",
            "last_name": "test",
            "first_name": "test",
            "phone_number": "+345345345345",
            "salary": 100000,
            "position_id": position,
            "password": "testjkjk",
            "is_active": True,
            "user_type": UserType.admin,
            "date_of_birth": date(2024, 1, 1),
            "date_of_jobstarted": date(2024, 1, 1),
            "created_time": date(2024, 1, 1),
        }
        user_id = await create_user_in_database(**user_data)
        return (user_data,user_id)

    async def test_create_project(self,client,create_user_in_database, create_position_from_database):

        user_data = await self.create_test_user(create_user_in_database,create_position_from_database)

        data_project = {
            "name":"Goodle",
            "start_date":date(2004,1,1),
            "end_date":date(2005,1,1),
            "price":"100000",
            "progemmer_list":[str(user_data[1])]
        }

        resp = client.post('/employee/project',data=data_project,
                           headers = create_test_auth_headers_for_user(user_data[0]['username'])
                           )
        
        data_json = resp.json()
        assert resp.status_code == 200    
        assert data_json['name'] == data_project['name']
        assert data_json["start_date"] == '2004-01-01T00:00:00'
        assert data_json['end_date'] == '2005-01-01T00:00:00'
        assert data_json['price'] == data_project['price']

    async def test_list_project(self,client,create_user_in_database, create_position_from_database,create_project_in_database):
        user_data = await self.create_test_user(create_user_in_database,create_position_from_database)

        project_data = {
            "name":"Goodle",
            "start_date":date(2004,1,1),
            "end_date":date(2005,1,1),
            "price":"100000",
            "progemmer_list":[str(user_data[1])]
        }

        data_project = await create_project_in_database(name=project_data["name"],
                                                        start_date=project_data["start_date"],
                                                        end_date=project_data["end_date"],
                                                        price=project_data["price"],
                                                        progemmer_list=project_data["progemmer_list"])

        resp = client.get('employee/projects', headers=create_test_auth_headers_for_user(user_data[0]['username']))

        assert resp.status_code==200
        data_json = resp.json()
        assert data_json['items'][0]['name'] == project_data['name']
        assert data_json['items'][0]['start_date'] == '2004-01-01T00:00:00'
        assert data_json['items'][0]['end_date'] == '2005-01-01T00:00:00'
        assert data_json['items'][0]['price'] == project_data['price']

    async def test_update_project(self, client,create_user_in_database, create_position_from_database,create_project_in_database):
        user_data = await self.create_test_user(create_user_in_database,create_position_from_database)

        project_data = {
            "name":"Google",
            "start_date":date(2004,1,1),
            "end_date":date(2005,1,1),
            "price":"100000",
            "progemmer_list":[str(user_data[1])]
        }

        data_project = await create_project_in_database(name=project_data["name"],
                                                        start_date=project_data["start_date"],
                                                        end_date=project_data["end_date"],
                                                        price=project_data["price"],
                                                        progemmer_list=project_data["progemmer_list"])

        resp = client.patch('employee/project', headers=create_test_auth_headers_for_user(user_data[0]['username']),
                                            params ={'project_id':data_project.id},
                                            data = {'name':'Katta bola',
                                                    "start_date":'2025-01-02',
                                                    'end_date':'2025-01-04',
                                                    'price':'10000',
                                                    'progemmer_list':[user_data[1]]})

        assert resp.status_code == 200
        data_json = resp.json()

        assert data_json['name'] == 'Katta bola'
        assert data_json['start_date'] == '2025-01-02T00:00:00'
        assert data_json['end_date'] == '2025-01-04T00:00:00'
        assert data_json['price'] == '10000'

    async def test_delete_project(self,client,create_user_in_database, create_position_from_database,create_project_in_database):
        user_data = await self.create_test_user(create_user_in_database,create_position_from_database)

        project_data = {
            "name":"Google",
            "start_date":date(2004,1,1),
            "end_date":date(2005,1,1),
            "price":"100000",
            "progemmer_list":[str(user_data[1])]
        }

        data_project = await create_project_in_database(name=project_data["name"],
                                                        start_date=project_data["start_date"],
                                                        end_date=project_data["end_date"],
                                                        price=project_data["price"],
                                                        progemmer_list=project_data["progemmer_list"])
        
        resp = client.delete('employee/project', headers=create_test_auth_headers_for_user(user_data[0]['username']),
                                            params ={'project_id':data_project.id})

        assert resp.status_code == 200 
        data_json = resp.json()

        assert data_json['message'] == 'Project deleted successfully'
        assert data_json['success'] == True
        
    async def test_update_status_project(self,client,create_user_in_database, create_position_from_database,create_project_in_database):
        user_data = await self.create_test_user(create_user_in_database,create_position_from_database)

        project_data = {
            "name":"Google",
            "start_date":date(2004,1,1),
            "end_date":date(2005,1,1),
            "price":"100000",
            "progemmer_list":[str(user_data[1])]
        }

        data_project = await create_project_in_database(name=project_data["name"],
                                                        start_date=project_data["start_date"],
                                                        end_date=project_data["end_date"],
                                                        price=project_data["price"],
                                                        progemmer_list=project_data["progemmer_list"])
        
        resp = client.patch('employee/project-status', headers=create_test_auth_headers_for_user(user_data[0]['username']),
                                            params ={'project_id':data_project.id,
                                                     'status':'done'})
        assert resp.status_code == 200
        data_json = resp.json()
        assert data_json['success'] == True
        assert data_json['message'] == "Status created successfully"
        assert data_json['status'] == 'done'
