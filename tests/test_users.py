import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app, get_db
from app.models import Base
# if pytest is not working
# change directory : cd "C:\Users\johns\OneDrive - Atlantic TU\CICD3\Labs\Lab2\Y4_Lab2"
# run python -m pytest

TEST_DB_URL = "sqlite+pysqlite:///:memory:"
engine = create_engine(TEST_DB_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine, expire_on_commit=False)
Base.metadata.create_all(bind=engine)

@pytest.fixture
def client():
    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        # hand the client to the test
        yield c
        # --- teardown happens when the 'with' block exits ---

def test_create_user(client):
    r = client.post("/api/users", 
                    json = {
                        "student_id": "S1234567",
                        "name": "Anthony",
                        "email": "anto@atu.ie",
                        "age": 24
                    })
    assert r.status_code == 201

                    