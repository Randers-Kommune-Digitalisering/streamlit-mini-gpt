from models import File
from utils.db_connection import get_db_client

db_client = get_db_client()


def create_file(assistant_id, azure_file_id, name, type_, size, timestamp):
    session = db_client.get_session()
    try:
        new_file = File(
            assistant_id=assistant_id,
            azure_file_id=azure_file_id,
            name=name,
            type=type_,
            size=size,
            timestamp=timestamp
        )
        session.add(new_file)
        session.commit()
        return {"message": "File created successfully", "file_id": new_file.file_id}
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def get_files_by_assistant(assistant_id):
    session = db_client.get_session()
    try:
        files = session.query(File).filter_by(assistant_id=assistant_id).all()
        files_data = [
            {
                'file_id': file.file_id,
                'assistant_id': file.assistant_id,
                'azure_file_id': file.azure_file_id,  # Ensure this is included
                'name': file.name,
                'type': file.type,
                'size': file.size,
                'timestamp': file.timestamp.isoformat() if file.timestamp else None
            } for file in files
        ]
        return files_data
    except Exception as e:
        raise e
    finally:
        session.close()


def update_file(file_id, **kwargs):
    session = db_client.get_session()
    try:
        file = session.query(File).filter_by(file_id=file_id).first()
        if not file:
            raise ValueError("File not found")
        for field in ['assistant_id', 'name', 'type', 'size', 'timestamp']:
            if field in kwargs:
                setattr(file, field, kwargs[field])
        session.commit()
        return {"message": "File updated successfully"}
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def delete_file(azure_file_id):
    session = db_client.get_session()
    try:
        file = session.query(File).filter_by(azure_file_id=azure_file_id).first()
        if not file:
            raise ValueError("File not found")
        session.delete(file)
        session.commit()
        return {"message": "File deleted successfully"}
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()
