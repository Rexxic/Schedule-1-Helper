from pydantic import BaseModel
import json
import os

DATA_FILE = "drug_set.json"

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
        """Return True if the drug has no mixtures that yield other than itself."""
        if self.mixed_with:
            item_set = self.mixed_with.values()
            return len(item_set) == 1 and self.name in item_set
        return True

class DrugSet(BaseModel):
    """
    Holds a collection of drugs.
    
    Attributes:
        drugs (dict[str, Drug]): A dictionary mapping drug names to Drug objects.
    """
    drugs: dict[str, Drug] = {}
    ingredients: dict[str, int] = {}
    
    def add_drug(self, name: str, value: int = 0, base: str = "", ingredient: str = ""):
        """
        Add a drug to the set. If the drug exists, updates its value and mixture details.
        
        Parameters:
            name (str): Name of the drug.
            value (int): The drug's value.
            base (str): The base drug with which it is mixed (optional).
            ingredient (str): The ingredient used for mixing (optional).
        """
        if name in self.drugs:
            if value:
                self.drugs[name].value = value
            if base and ingredient:
                self.drugs[name].mixed_with[ingredient] = base
        else:
            self.drugs[name] = Drug(name=name, value=value)
            if base and ingredient:
                self.drugs[name].mixed_with[ingredient] = base

        if base and ingredient:
            if base in self.drugs:
                self.drugs[base].creates_with[ingredient] = name
            else:
                self.drugs[base] = Drug(name=base)
                self.drugs[base].creates_with[ingredient] = name

    def get_drug(self, name: str):
        """
        Retrieve a drug from the set.
        
        Parameters:
            name (str): The name of the drug.
            
        Returns:
            Drug or None: The Drug object if found, else None.
        """
        return self.drugs.get(name)
    
    def set_ingredient(self, name: str, value: int = 0):
        """
        Adds/Updates an ingridient.

        Parameters:
            name (str): The name of the ingridient.
            value (int): The value of the ingridient.
        """
        self.ingridients[name] = value
        
    def get_ingredient(self, name: str):
        """
        Retrieves the value of an ingridient, zero if unknown.

        Parameters:
            name (str): The name of the ingridient.
        """
        return self.ingridients[name] if name in self.ingridients else 0

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