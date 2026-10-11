from fastapi import Depends,HTTPException,status

def get_token():
    return {"hash" : "xxx-1" }



def get_current_user(token=Depends(get_token)):
    if token:
        return {
            "id": 1,
            "role": "admin"
        }


def require_admin(user=Depends(get_current_user)):
    if user['role'] == "admin":
        return True
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Only Admin Can access")