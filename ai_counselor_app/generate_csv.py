import requests
import pandas as pd
import random
import time

# ✅ Other Countries (Exclude US)
countries = [
    "Canada", "United Kingdom", "Germany", "Australia",
    "France", "Netherlands", "Sweden", "Norway", "Denmark",
    "Finland", "Ireland", "Switzerland", "Italy", "Spain",
    "Singapore", "Japan", "South Korea", "New Zealand", "China",
    "India"
]

# ✅ US Search Keywords (Chunked)
us_keywords = [
    "University", "College", "Institute",
    "California", "Texas", "New York",
    "Massachusetts", "Illinois", "Florida"
]

# ✅ Tuition ranges
tuition_ranges = {
    "United States": (35000, 70000),
    "Canada": (20000, 45000),
    "United Kingdom": (25000, 55000),
    "Germany": (1000, 15000),
    "Australia": (25000, 55000),
    "India": (2000, 12000)
}

scholarship_levels = ["Very High", "High", "Medium", "Low"]

programs_pool = [
    "MS Computer Science", "Artificial Intelligence", "Data Science",
    "MBA", "Cybersecurity", "Robotics",
    "Business Analytics", "Software Engineering"
]

city_samples = {
    "United States": ["New York", "Boston", "California", "Chicago", "Texas"],
    "Canada": ["Toronto", "Vancouver"],
    "United Kingdom": ["London", "Manchester"],
    "Germany": ["Berlin", "Munich"],
    "Australia": ["Sydney", "Melbourne"],
    "India": ["Delhi", "Mumbai", "Bangalore"]
}

# ✅ Helpers
def generate_city(country):
    return random.choice(city_samples.get(country, ["Main City"]))

def generate_programs():
    return ", ".join(random.sample(programs_pool, k=3))

def generate_ranking():
    return random.randint(1, 500)

# ✅ Safe Fetch
def safe_fetch(params, retries=3):
    url = "http://universities.hipolabs.com/search"

    for attempt in range(retries):
        try:
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                return response.json()
        except:
            time.sleep(2)

    return []

# ✅ Main Dataset
all_unis = []

print("🌍 Fetching Non-US Universities...")

for country in countries:
    data = safe_fetch({"country": country})

    for uni in data[:100]:
        min_fee, max_fee = tuition_ranges.get(country, (8000, 30000))

        all_unis.append({
            "name": uni["name"],
            "country": country,
            "city": generate_city(country),
            "ranking": generate_ranking(),
            "programs": generate_programs(),
            "tuition": random.randint(min_fee, max_fee),
            "scholarship": random.choice(scholarship_levels),
            "website": uni["web_pages"][0] if uni["web_pages"] else ""
        })

    print(f"✅ Added universities for {country}")

# ✅ Fetch US Separately
print("\n🇺🇸 Fetching US Universities Separately...")

us_added = 0
us_seen = set()

for keyword in us_keywords:
    print(f"🔍 Searching US keyword: {keyword}")

    data = safe_fetch({"country": "United States", "name": keyword})

    for uni in data[:150]:

        if uni["name"] in us_seen:
            continue

        us_seen.add(uni["name"])

        min_fee, max_fee = tuition_ranges["United States"]

        all_unis.append({
            "name": uni["name"],
            "country": "United States",
            "city": generate_city("United States"),
            "ranking": generate_ranking(),
            "programs": generate_programs(),
            "tuition": random.randint(min_fee, max_fee),
            "scholarship": random.choice(scholarship_levels),
            "website": uni["web_pages"][0] if uni["web_pages"] else ""
        })

        us_added += 1

    time.sleep(1)

print(f"\n✅ Total US Universities Added: {us_added}")

# ✅ Save CSV
df = pd.DataFrame(all_unis)
df.to_csv("universities2.csv", index=False)

print("\n✅ universities2.csv generated successfully!")
print("Total Universities:", len(df))
