import json
import os

class RecommendationEngine:
    def __init__(self, data_file="users.json"):
        self.data_file = data_file
        self.items = self.load_items()
        self.current_user = None
        self.user_db = self.load_user_db()

    def load_items(self):
        return {
            "Python Masterclass": ["programming", "python", "ai"],
            "Data Science Bootcamp": ["ai", "data", "math"],
            "Yoga for Beginners": ["fitness", "health", "wellness"],
            "HIIT Training": ["fitness", "sports", "health"],
            "Financial Literacy 101": ["finance", "business", "math"],
            "Digital Marketing 360": ["business", "marketing", "social"]
        }

    def load_user_db(self):
        if not os.path.exists(self.data_file):
            return {}
        try:
            with open(self.data_file, "r") as f:
                return json.load(f)
        except:
            return {}

    def save_user_db(self):
        with open(self.data_file, "w") as f:
            json.dump(self.user_db, f, indent=4)

    def login(self, username):
        if username not in self.user_db:
            print(f"Welcome {username}! New profile created.")
            self.user_db[username] = {"interests": [], "history": []}

        self.current_user = username
        self.save_user_db()

    def update_interests(self):
        print("\nAvailable: programming, python, ai, fitness, health, business, math, finance")
        data = input("Enter interests (comma separated): ")

        interests = [i.strip().lower() for i in data.split(",") if i.strip()]
        self.user_db[self.current_user]["interests"] = interests

        self.save_user_db()
        print("Profile updated successfully!")

    def generate_recommendations(self):
        user_interests = set(self.user_db[self.current_user]["interests"])

        if not user_interests:
            return "No interests found. Please update profile first!"

        results = []

        for item, tags in self.items.items():
            score = len(user_interests & set(tags))

            if score > 0:
                results.append({
                    "item": item,
                    "score": score
                })

        results.sort(key=lambda x: x["score"], reverse=True)

        if results:
            self.user_db[self.current_user]["history"].append(results[0]["item"])
            self.save_user_db()

        return results

    def display_profile(self):
        profile = self.user_db[self.current_user]

        print(f"\n--- PROFILE: {self.current_user} ---")
        print("Interests:", ", ".join(profile["interests"]))
        print("Recent:", profile["history"][-3:])


def main():
    engine = RecommendationEngine()

    print("=== SMART RECOMMENDATION SYSTEM ===")

    username = input("Enter username: ").strip()
    if not username:
        print("Invalid username")
        return

    engine.login(username)

    while True:
        print("\n[1] Update Interests")
        print("[2] Get Recommendations")
        print("[3] View Profile")
        print("[4] Exit")

        choice = input("Choose option: ")

        if choice == "1":
            engine.update_interests()

        elif choice == "2":
            results = engine.generate_recommendations()

            if isinstance(results, list):
                print("\n🔥 Top Recommendations:\n")
                for r in results:
                    print(f"✔ {r['item']} ({r['score']} matches)")
            else:
                print(results)

        elif choice == "3":
            engine.display_profile()

        elif choice == "4":
            print("Goodbye 👋")
            break

        else:
            print("Invalid option")


if __name__ == "__main__":
    main()