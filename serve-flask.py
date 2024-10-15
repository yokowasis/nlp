import backend
from dotenv import load_dotenv
import os
load_dotenv()

backend.app.run(host='localhost', port=int(os.getenv('PORT') or "3000"))
