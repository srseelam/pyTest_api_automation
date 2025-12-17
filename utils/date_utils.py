from datetime import datetime
def is_valid_date(d,fmt="%Y-%m-%d"):
    try: datetime.strptime(d,fmt); return True
    except: return False
