from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import Database
import logging

# Pydantic model
class PasswordData(BaseModel):
    platform: str
    username: str
    password: str

class PasswordManagerAPI:
    def __init__(self):
        self.app = FastAPI(title="Password Manager API")
        self.db = Database()
        self.register_routes()
    
    def register_routes(self):
        @self.app.get("/")
        def read_root():
            return {"message": "Password Manager API is running!"}
        
        @self.app.post("/add-password")
        def add_password(data: PasswordData):
            logging.info("API add pass method")
            print("add password")
            if self.db.addPassword(data.platform, data.username, data.password):
                return {"success": True, "message": "Password added successfully"}
            raise HTTPException(status_code=500, detail="Failed to add password!")
        
        @self.app.get("/search-password/{search_term}")
        def search_password(search_term: str):
            result = self.db.searchPassword(search_term)
            if result:
                return result
            raise HTTPException(status_code=404, detail="No passwords found!")
        
        @self.app.get("/get-all")
        def get_all():
            return self.db.getAll()
        
        @self.app.put("/update-password/{id}")
        def update_password(id: int, data: PasswordData):
            if self.db.updatePassword(id, data.platform, data.username, data.password):
                return {"success": True, "message": "Password updated successfully"}
            raise HTTPException(status_code=500, detail="Error while updating password!")
        
        @self.app.delete("/delete-password/{id}")
        def delete_password(id: int):
            if self.db.deletePassword(id):
                return {"success": True, "message": "Password deleted successfully"}
            raise HTTPException(status_code=500, detail="Error while deleting password!")
        
# Creating Instance
api_instance = PasswordManagerAPI()
app = api_instance.app