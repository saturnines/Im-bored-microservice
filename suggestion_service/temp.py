import sys

from crud_services import create_entry, delete_entry, random_entry


def main_menu():
    print("\nWelcome to the Random things to do!")
    print("This simple app allows you to interact with the suggestions database.")
    print("You can create, delete, and retrieve random suggestions.")
    while True:
        print("\nChoose an option:")
        print("1: Create a new suggestion")
        print("2: Delete a suggestion")
        print("3: Get a random suggestion")
        print("4: Quit")

        choice = input("Enter choice: ")
        if choice == '1':
            create_suggestion()
        elif choice == '2':
            delete_suggestion()
        elif choice == '3':
            get_random_suggestion()
        elif choice == '4':
            sys.exit("Exiting the program...")
        else:
            print("Invalid choice. Please choose a valid option.")

def create_suggestion():
    category = input("Enter category: ")
    title = input("Enter title: ")
    description = input("Enter description (optional): ")
    try:
        create_entry(category, title, description)
        print("Suggestion created successfully.")
    except Exception as e:
        print(f"Error creating suggestion: {e}")

def delete_suggestion():
    category = input("Enter category of the suggestion to delete: ")
    title = input("Enter title of the suggestion to delete: ")
    description = input("Enter description of the suggestion to delete: ")
    try:
        delete_entry(category, title, description)
        print("Suggestion deleted successfully.")
    except Exception as e:
        print(f"Error deleting suggestion: {e}")

def get_random_suggestion():
    try:
        result = random_entry()
        if result:
            print("Random Suggestion Found:")
            print(f"Category: {result[0]}, Title: {result[1]}, Description: {result[2]}")
        else:
            print("No suggestions available.")
    except Exception as e:
        print(f"Error fetching random suggestion: {e}")

if __name__ == "__main__":
    main_menu()


#db intergration
# get random suggestions
#add random stuff

#heu 2 is at the start
#4 let people gather as much info as they want