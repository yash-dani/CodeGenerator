from firebase_admin import credentials, firestore, initialize_app, storage
import datetime

class Image():
    def __init__(self):
        self.cred = credentials.Certificate('key.json')
        self.app = initialize_app(self.cred, {
            "storageBucket" : "se101-team404.appspot.com"
        })
        self.image_path = ""
        self.image_title = ""
        self.bucket = storage.bucket()
        self.blob = ""
    
    def upload(self, image_path, image_title):
        self.blob = self.bucket.blob(image_title)
        self.blob.upload_from_filename(image_path)
    
    def download(self, image_title):
        self.blob = self.bucket.blob(image_title)
        return(self.blob.generate_signed_url(datetime.timedelta(seconds = 300), method = 'GET'))