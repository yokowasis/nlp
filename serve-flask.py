import backend
from dotenv import load_dotenv
import os
load_dotenv()

backend.app.run(host='0.0.0.0', port=int(os.getenv('PORT') or "3000"))
