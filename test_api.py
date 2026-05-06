import requests
import json

# Test health endpoint
print("Testing health...")
r = requests.get("http://localhost:5000/api/health")
print(f"Health: {r.json()}")

# Test register endpoint
print("\nTesting register...")
data = {
    "name": "John",
    "age": 25,
    "height": 170,
    "weight": 70,
    "goal": "lose",
    "diet_type": "both",
    "period": "month"
}
r = requests.post("http://localhost:5000/api/register", json=data)
print(f"Register: {r.json()}")

# Test get data endpoint
print("\nTesting get data...")
r = requests.get("http://localhost:5000/api/data/John")
print(f"Data: {r.json()}")