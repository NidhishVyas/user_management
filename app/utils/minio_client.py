# minio_client.py

from minio import Minio
from minio.error import S3Error


def create_minio_client():
    try:
        # Initialize the Minio client with your Minio server details
        client = Minio(
            "localhost:9000",  # Or the appropriate IP/hostname
            access_key="minioadmin",  # Replace with your actual Minio admin user
            secret_key="minioadmin",  # Replace with your actual Minio admin password
            secure=False,  # Set to True if you are using HTTPS
        )
        return client
    except S3Error as e:
        print(f"Error initializing Minio client: {e}")
        raise


if __name__ == "__main__":
    # Simple test to ensure the client is working
    client = create_minio_client()
    print(f"Minio client created: {client}")
