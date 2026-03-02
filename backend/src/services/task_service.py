from fastapi import HTTPException
from src.db.supabase_client import supabase

def create_task(client, user_id, data):
    try:
        task_response = client.table("tasks").insert({
            "user_id": user_id,
            "title": data.title,
            "description": data.description,
        }).execute()

        if not task_response.data:
            raise HTTPException(status_code=400, detail="Task creation failed")

        return task_response.data
    
    except Exception as e:
        print("EXCEPTION:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
    

def get_tasks(client, user_id: str):
    response = (
        client.table("tasks")
        .select("*")
        .eq("user_id", user_id)
        .execute()
    )

    return response.data


def update_task(client, user_id: str, task_id: str, data):
    try:
        response = (
            client.table("tasks")
            .update(data.dict(exclude_unset=True))
            .eq("id", task_id)
            .eq("user_id", user_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=404, detail="Task not found")

        return response.data
    
    except Exception as e:
        print("EXCEPTION:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
    

def delete_task(client, user_id: str, task_id: str):
    try:
        response = (
            client.table("tasks")
            .delete()
            .eq("id", task_id)
            .eq("user_id", user_id)
            .execute()
        )

        if not response.data:
            raise HTTPException(status_code=404, detail="Task not found")

        return {
            "message": "Task deleted successfully",
            "task": response.data
        }
    
    except Exception as e:
        print("EXCEPTION:", str(e))
        raise HTTPException(status_code=500, detail=str(e))