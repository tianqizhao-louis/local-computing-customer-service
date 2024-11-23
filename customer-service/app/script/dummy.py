import requests
import random
import string
import uuid

# URLs of your API endpoints for customers, breeders, and pets
customer_url = "http://localhost:8001/api/v1/customers/"
breeder_url = "http://localhost:8080/api/v1/breeders/"
pet_url = "http://localhost:8082/api/v1/pets"
waitlist_url_template = "http://localhost:8001/api/v1/customers/{customer_id}/waitlist"

# Function to generate random dummy customer data
def generate_dummy_customer():
    # Generate random name
    name = ''.join(random.choices(string.ascii_uppercase + string.ascii_lowercase, k=10))
    
    # Generate a random email
    email = f"{name.lower()}@example.com"

    return {
        "name": name,
        "email": email
    }

# Function to get a random breeder and pet from the APIs
def get_random_breeder_and_pet():
    # Get breeders
    breeder_response = requests.get(breeder_url)
    if breeder_response.status_code != 200:
        raise Exception(f"Failed to fetch breeders: {breeder_response.status_code}")
    breeders = breeder_response.json().get("data", [])
    if not breeders:
        raise Exception("No breeders found")
    breeder = random.choice(breeders)

    # Get pets
    pet_response = requests.get(pet_url)
    if pet_response.status_code != 200:
        raise Exception(f"Failed to fetch pets: {pet_response.status_code}")
    pets = pet_response.json().get("data", [])
    if not pets:
        raise Exception("No pets found")
    pet = random.choice(pets)

    return breeder, pet

# Function to add a pet to the customer's waitlist
def add_pet_to_waitlist(customer_id, pet_id, breeder_id):
    waitlist_url = waitlist_url_template.format(customer_id=customer_id)
    payload = {
        "pet_id": pet_id,
        "breeder_id": breeder_id
    }
    response = requests.post(waitlist_url, json=payload)

    if response.status_code == 201:
        print(f"Successfully added pet {pet_id} to waitlist for customer {customer_id}")
    else:
        print(f"Failed to add pet {pet_id} to waitlist for customer {customer_id} - Status Code: {response.status_code}")
        try:
            print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error while reading response text: {e}")

# Loop to add 20 dummy customers and add a pet to their waitlist
for _ in range(20):
    dummy_customer = generate_dummy_customer()

    # Sending the POST request to create a customer
    response = requests.post(customer_url, json=dummy_customer)

    # Checking if the request was successful
    if response.status_code == 201:
        customer_data = response.json()
        customer_id = customer_data['id']
        print(f"Successfully added customer: {dummy_customer['name']}")

        try:
            # Get a random breeder and pet
            print("Fetching a random breeder and pet...")
            breeder, pet = get_random_breeder_and_pet()
            breeder_id = breeder["id"]
            pet_id = pet["id"]
            print(f"Fetched breeder ID: {breeder_id}, pet ID: {pet_id}")

            # Adding a pet to the waitlist for the created customer
            add_pet_to_waitlist(customer_id, pet_id, breeder_id)
        except Exception as e:
            print(f"Error adding pet to waitlist: {e}")
    else:
        print(f"Failed to add customer: {dummy_customer['name']} - Status Code: {response.status_code}")
        try:
            # Log the response text for more details on the failure
            print(f"Response: {response.text}")
        except Exception as e:
            print(f"Error while reading response text: {e}")
