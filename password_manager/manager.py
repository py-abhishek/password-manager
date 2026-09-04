import json
import logging
from utils.input_utils import InputUtils
import uuid
from password_manager.encrypt import Encryption
from password_manager.server_handling.database import Database
import requests


class ReadJson:
    def __init__(self):
        pass
    
    # Read Json file
    def readData(self):
        try:
            with open(self.file_path, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            # Create new file
            with open(self.file_path, "w") as f:
                json.dump([], f)
                return []
        
    # Write Json file
    def writeData(self, data):
        try:
            with open(self.file_path, "w") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            print(f"Error while saving password: {e}")


class PasswordManager(ReadJson):
    def __init__(self, file_path):
        super().__init__()
        self.file_path = file_path
        self.inputUtils = InputUtils
        self.encryption = Encryption()
        self.database = Database()
        self.url = "http://127.0.0.1:8000/"

    # Add Password
    def addPassword(self, platform, username, password):
        data = {"platform": platform, "username": username, "password": password}
        response = requests.post(self.url+"add-password",json=data)
        return response.json()

    # Search Password
    def searchPassword(self, usr_input):
        url = f"{self.url}search-password/{usr_input}"
        response = requests.get(url)
        return response.json()
        
    # Update Password
    def updatePassword(self, usr_input):
        result = self.searchPassword(usr_input)
        if result:
            for i, item in enumerate(result):
                print(f"{i+1}. Id: {item[0]} Platform: {item[1]} | Username: {item[2]} | Password: {self.encryption.decryptPass(item[3])}")

            usr_choice = self.inputUtils.askInt("Enter Id you want to Update:")
            
            platform = self.inputUtils.askString(f"New Platform name: ")
            username = self.inputUtils.askString(f"New username: ")
            password = self.inputUtils.askString(f"New password: ")
            enc_pass = self.encryption.encryptPass(password)
            data = {'platform': platform, 'username': username, 'password': enc_pass}

            url = self.url+f"update-password/{usr_choice}"
            response = requests.put(url,json=data)
            return response.json()

        else:
            print("No Result Found")

    def update_pass_by_id(self, id, platform, username, password):
        enc_pass = self.encryption.encryptPass(password)

        data = {'platform': platform, 'username': username, 'password': enc_pass}

        url = self.url+f"update-password/{id}"
        response = requests.put(url,json=data)
        return response.json()
        
    # Delete Password
    def deletePassword(self, usr_input):
        result = self.searchPassword(usr_input)
        if result:
            for i, item in enumerate(result):
                print(f"{i+1}. Id: {item[0]} Platform: {item[1]} | Username: {item[2]} | Password: {self.encryption.decryptPass(item[3])}")

            usr_choice = self.inputUtils.askInt("Enter Id to delete: ")
            url = self.url+f"delete-password/{usr_choice}"
            response = requests.delete(url)
            return response.json()

        else:
            print("No Result Found")

    def Delete_pass_by_id(self, id):
        url = self.url+f"delete-password/{id}"
        response = requests.delete(url)
        return response.json()

    # View All passwords
    def getAll(self):
        response = requests.get(self.url+"get-all")
        return response.json()
                


