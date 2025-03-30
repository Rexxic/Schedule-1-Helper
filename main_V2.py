import json
import os
import re
from pydantic import BaseModel
from pyvis.network import Network

DATA_FILE = "drugs.json"

class Drug(BaseModel):
    """
    Represents a drug with a name, value, and relationships with other drugs.
    
    Attributes:
        name (str): The name of the drug.
        value (int): An integer value associated with the drug.
        mixed_with (dict[str, str]): A mapping where key is an ingredient and value is the base drug it is mixed with.
        creates_with (dict[str, str]): A mapping where key is an ingredient and value is the drug created.
    """
    name: str
    value: int = 0
    mixed_with: dict[str, str] = {}
    creates_with: dict[str, str] = {}
    
    def is_base(self):
        """Return True if the drug has no mixtures."""
        return not self.mixed_with

class DrugSet(BaseModel):
    """
    Holds a collection of drugs.
    
    Attributes:
        drug_set (dict[str, Drug]): A dictionary mapping drug names to Drug objects.
    """
    drug_set: dict[str, Drug] = {}
    
    def add_drug(self, name: str, value: int = 0, base: str = "", ingredient: str = ""):
        """
        Add a drug to the set. If the drug exists, updates its value and mixture details.
        
        Parameters:
            name (str): Name of the drug.
            value (int): The drug's value.
            base (str): The base drug with which it is mixed (optional).
            ingredient (str): The ingredient used for mixing (optional).
        """
        if name in self.drug_set:
            if value:
                self.drug_set[name].value = value
            if base and ingredient:
                self.drug_set[name].mixed_with[ingredient] = base
        else:
            self.drug_set[name] = Drug(name=name, value=value)
            if base and ingredient:
                self.drug_set[name].mixed_with[ingredient] = base

        if base and ingredient:
            if base in self.drug_set:
                self.drug_set[base].creates_with[ingredient] = name
            else:
                self.drug_set[base] = Drug(name=base)
                self.drug_set[base].creates_with[ingredient] = name

    def get_drug(self, name: str):
        """
        Retrieve a drug from the set.
        
        Parameters:
            name (str): The name of the drug.
            
        Returns:
            Drug or None: The Drug object if found, else None.
        """
        return self.drug_set.get(name)

    def save_to_file(self, filename: str = DATA_FILE):
        """
        Save the current drug set to a JSON file.
        
        Parameters:
            filename (str): Path to the JSON file.
        """
        with open(filename, "w") as f:
            json.dump(self.model_dump(), f, indent=4)
        print(f"Data saved to {filename}.")

    @classmethod
    def load_from_file(cls, filename: str = DATA_FILE):
        """
        Load a DrugSet from a JSON file if it exists.
        
        Parameters:
            filename (str): Path to the JSON file.
            
        Returns:
            DrugSet: The loaded DrugSet or a new one if file doesn't exist.
        """
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
            return cls.model_validate(data)
        return cls()

def print_help():
    """
    Display available commands.
    """
    help_text = """
Available commands:
    help                - Show this help message.
    add_drug            - Add a drug. Usage: add_drug <name> [value] [base] [ingredient]
                          (value is an integer; base and ingredient are optional and should be provided together)
    get_drug            - Get drug details. Usage: get_drug <name>
    save                - Save current data to file.
    render              - Placeholder command for future rendering functionality.
    exit                - Exit the program.
    """
    print(help_text)

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

        # Use shlex.split to handle quoted arguments properly
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
            net = Network()
            for name, drug in drug_set.drug_set.items():
                net.add_node(name,value=drug.value, color='#ff3399' if drug.is_base() else '#669900')
                for ingredient in drug.creates_with:
                    net.add_node(ingredient, color='#0066ff')
            for name, drug in drug_set.drug_set.items():
                for ingredient, product in drug.creates_with.items():
                    net.add_edge(name, product)
                    net.add_edge(ingredient, product)
            net.toggle_physics(True)
            net.show('nodes.html', notebook=False)
        elif command == "exit":
            print("Exiting.")
            break
        
        else:
            print("Unknown command. Type 'help' for available commands.")

if __name__ == "__main__":
    main()