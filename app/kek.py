import json
import random
import string

def random_string(length=12):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def generate_large_json(num_users=100):
    data = {
        "users": []
    }

    for user_id in range(1, num_users + 1):
        user = {
            "id": user_id,
            "username": f"user_{random_string(8)}",
            "email": f"{random_string(6)}@example.com",
            "profile": {
                "first_name": random_string(6),
                "last_name": random_string(8),
                "bio": random_string(100),
                "interests": [random_string(10) for _ in range(10)],
                "location": {
                    "city": random_string(8),
                    "country": random_string(6)
                }
            },
            "stats": {
                "followers": random.randint(0, 10000),
                "following": random.randint(0, 10000),
                "posts": random.randint(0, 500)
            }
        }
        data["users"].append(user)

    return data

# Save to file if needed
large_json = generate_large_json(100)
with open("large_data.json", "w") as f:
    json.dump(large_json, f, indent=2)

print("Large JSON generated and saved.")
