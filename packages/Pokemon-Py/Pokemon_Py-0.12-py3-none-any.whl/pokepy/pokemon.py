import requests
url = "https://pokeapi.co/api/v2/pokemon"


class Pokemon:
    """
        A class for interacting with Pokémon data using the PokeAPI.

        This class provides methods to retrieve various aspects of Pokémon data,
        such as moves, abilities, sprites, and more.

        Example usage:
        - p = Pokemon()
        - p.get(2)
        Output: {'name': 'ivysaur', ...}

        - p.get_moves(2)
        Output: [{'move': {'name': 'razor-wind', ...}, ...}, ...]

        p.get_abilities(2)
        Output: [{'ability': {'name': 'overgrow', ...}, ...}, ...]

        """
    def __init__(self):
        # dict that caches data
        """Initialize the Pokemon class"""
        self._pokemon_cache = {}

    def get(self, name_or_id) -> dict:
        """
        Retrieve data for a specific Pokémon.

        Args:
        name_or_id (str or int): Name or ID of the Pokémon.

        Returns:
            dict or None: A dictionary containing the Pokémon data,
            or None if the request fails.
        """
        if type(name_or_id) == str:
            name_or_id = name_or_id.lower()

        if name_or_id in self._pokemon_cache:
            return self._pokemon_cache[name_or_id]

        response = requests.get(f"{url}/{name_or_id}")
        if response.status_code == 200:
            data = response.json()
            self._pokemon_cache[name_or_id] = data
            return data
        else:
            return None

    def get_moves(self, name_or_id) -> list:
        """
        Retrieve the moves of a specific Pokémon.

        Args:
            name_or_id (str or int): Name or ID of the Pokémon.

        Returns:
            list or None: A list of moves for the Pokémon,
            or None if the request fails.
        """
        pokemon_data = self.get(name_or_id)
        moves_list = []
        if pokemon_data:
            for i in pokemon_data['moves']:
                moves_list.append(i['move']['name'])
            return moves_list
        else:
            return None

    def get_abilities(self, name_or_id) -> list:
        """
        Retrieve the abilities of a specific Pokémon.

        Args:
            name_or_id (str or int): Name or ID of the Pokémon.

        Returns:
            list or None: A list of moves for the Pokémon,
            or None if the request fails.
        """
        pokemon_data = self.get(name_or_id)
        abilities_list = []
        if pokemon_data:
            for i in pokemon_data['abilities']:
                abilities_list.append(i['ability']['name'])
            return abilities_list
        else:
            return None

    def get_sprites(self, name_or_id) -> dict:
        """
        Retrieve the sprites of a specific Pokémon.

        Args:
            name_or_id (str or int): Name or ID of the Pokémon.

        Returns:
            dict or None: A list of moves for the Pokémon,
            or None if the request fails.
        """
        pokemon_data = self.get(name_or_id)
        if pokemon_data:
            return pokemon_data['sprites']
        else:
            return None

    def get_stats(self, name_or_id) -> list:
        """
        Retrieve the stats of a specific Pokémon.

        Args:
            name_or_id (str or int): Name or ID of the Pokémon.

        Returns:
            list or None: A list of moves for the Pokémon,
            or None if the request fails.
        """
        pokemon_data = self.get(name_or_id)
        if pokemon_data:
            return pokemon_data['stats']
        else:
            return None

    def get_types(self, name_or_id) -> list:
        """
        Retrieve the types of a specific Pokémon.

        Args:
            name_or_id (str or int): Name or ID of the Pokémon.

        Returns:
            list or None: A list of moves for the Pokémon,
            or None if the request fails.
        """
        pokemon_data = self.get(name_or_id)
        if pokemon_data:
            return pokemon_data['types']
        else:
            return None
