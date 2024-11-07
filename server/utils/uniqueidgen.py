import uuid
from datetime import datetime

def generate_unique_id():
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    
    unique_str = str(uuid.uuid4().hex[:4]) 
    
    unique_id = f'{timestamp}-{unique_str}'
    
    return unique_id
