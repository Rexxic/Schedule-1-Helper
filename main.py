from model import DrugSet
from pyvis.network import Network
import re

def print_help():
    """
    Display available commands.
    """
    help_text = """
Available commands:
    help
        - Show this help message.
    add_drug
        - Add a drug.
          Usage: add_drug "drug name" [value] ["base drug name" "ingredient"]
          (If the name or base contains spaces, enclose it in quotes.)
    get_drug
        - Get drug details.
          Usage: get_drug "drug name"
    save
        - Save current data to file.
    toggle_ingredients
        - Toggle the rendering of ingredients
    render
        - Placeholder command for future rendering functionality.
    exit
        - Exit the program.
    """
    print(help_text)

def main():
    """
    Main function to run the command line interface.
    Loads existing data, processes user commands, and saves data when requested.
    """
    drug_set = DrugSet.load_from_file()
    print("DrugSet CLI loaded. Type 'help' for available commands.")
    
    while True:
        try:
            command_input = input(">>> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not command_input:
            continue

        # Parse all command line args with respect for quoted strings composited from mutliple words.
        try:
            parts = [str(s).replace('"', '') for s in re.findall(r'"[^"]*"|[\S]+', command_input)]
        except ValueError as e:
            print(f"Error parsing command: {e}")
            continue

        if not parts:
            continue

        command = str(parts[0]).lower()

        if command == "help":
            print_help()
        
        elif command == "add_drug":
            if len(parts) < 2:
                print("Usage: add_drug \"drug name\" [value] [\"base drug name\" \"ingredient\"]")
                continue

            name = parts[1]
            value = 0
            base = ""
            ingredient = ""

            if len(parts) >= 3:
                try:
                    value = int(parts[2])
                except ValueError:
                    print("Value must be an integer.")
                    continue
            if len(parts) == 5:
                base = parts[3]
                ingredient = parts[4]
            elif len(parts) not in (2, 3):
                print("Usage: add_drug \"drug name\" [value] [\"base drug name\" \"ingredient\"]")
                continue

            drug_set.add_drug(name, value, base, ingredient)
            print(f"Drug '{name}' added/updated.")
        
        elif command == "get_drug":
            if len(parts) != 2:
                print("Usage: get_drug \"drug name\"")
                continue
            name = parts[1]
            drug = drug_set.get_drug(name)
            if drug:
                print(drug.model_dump())
            else:
                print(f"Drug '{name}' not found.")
        
        elif command == "save":
            drug_set.save_to_file()
        
        elif command == "render":
            net = Network(height="1080", directed=True, select_menu=True)
            for name, drug in drug_set.drugs.items():
                net.add_node(name, title=f"{drug.value}$", value=drug.value, color='#ff3399' if drug.is_base() else '#669900')
                if drug_set.render_ingredients:
                    for ingredient in drug.creates_with:
                        net.add_node(ingredient, color='#0066ff')
            for name, drug in drug_set.drugs.items():
                for ingredient, product in drug.creates_with.items():
                    ingredient_value = drug_set.get_ingredient(ingredient)
                    net.add_edge(name, product, title=f"{ingredient}: {ingredient_value}$")
                    if drug_set.render_ingredients:
                        net.add_edge(ingredient, product)
            net.toggle_physics(True)
            net.show('nodes.html', notebook=False)
        
        elif command == "toggle_ingredients":
            drug_set.render_ingredients = not drug_set.render_ingredients
            print(f"render_ingredients: {drug_set.render_ingredients}")

        elif command == "exit":
            print("Exiting.")
            break
        
        else:
            print("Unknown command. Type 'help' for available commands.")

if __name__ == "__main__":
    main()