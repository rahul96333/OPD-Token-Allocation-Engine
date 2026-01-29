import requests
import time

# The address where your server is running
BASE_URL = "http://127.0.0.1:8000"

def run_simulation():
    print("🚀 Starting OPD Day Simulation...\n")

    # 1. Fill up Dr. Sharma's slot with regular patients
    patients = [
        {"doc": "Dr. Sharma", "name": "Patient A", "type": "walkin"},
        {"doc": "Dr. Sharma", "name": "Patient B", "type": "online"},
        {"doc": "Dr. Sharma", "name": "Patient C", "type": "followup"},
    ]

    for p in patients:
        res = requests.post(f"{BASE_URL}/book-token", 
                            params={"doctor_name": p["doc"], "patient_name": p["name"], "source": p["type"]})
        print(f"Booked {p['name']}: {res.json()['status']}")

    # 2. Trigger an EMERGENCY (Real-world variability)
    print("\n🚨 ALERT: Emergency Arrival for Dr. Sharma!")
    emergency = {"doc": "Dr. Sharma", "name": "EMERGENCY_RAHUL", "type": "emergency"}
    res = requests.post(f"{BASE_URL}/book-token", 
                        params={"doctor_name": emergency["doc"], "patient_name": emergency["name"], "source": emergency["type"]})
    print(f"Result: {res.json()['message']}")

    # 3. Book patients for other doctors to show multi-doctor support
    requests.post(f"{BASE_URL}/book-token", params={"doctor_name": "Dr. Reddy", "patient_name": "Patient X", "source": "paid"})
    requests.post(f"{BASE_URL}/book-token", params={"doctor_name": "Dr. Kapoor", "patient_name": "Patient Y", "source": "walkin"})

    print("\n✅ Simulation Complete. Check your browser at http://127.0.0.1:8000/view-status to see the final queues.")

if __name__ == "__main__":
    run_simulation()