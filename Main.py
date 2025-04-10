from Ikon import brand_score

def main():
    print("Welcome to Ikon!")
    
    brand_name = input("Enter the brand name: ").strip()
    tags_input = input("Enter tags for the brand (comma-separated): ").strip()
    tags = [tag.strip() for tag in tags_input.split(",") if tag.strip()]
    
    while True:
        ease = float(input("On a scale of 0 to 1, how easy is it to say the brand name? (e.g., 0 if impossible): ").strip())
        if 0 <= ease <= 1:
            break
        else:
            print("Please enter a number between 0 and 1.")
    
    is_luxury_input = input("Is this a luxury product? (yes/no): ").strip().lower()
    is_luxury = is_luxury_input in ["yes", "y"]
    
    score = brand_score(brand_name, tags, ease, is_luxury)
    
    print(f"\nThe score for the brand '{brand_name}' with tags {tags} is: {score}")

if __name__ == "__main__":
    main()