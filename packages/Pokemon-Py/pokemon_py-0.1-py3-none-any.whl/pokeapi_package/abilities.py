import requests
url = "https://pokeapi.co/api/v2/ability"


class Ability:
    def __init__(self):
        # dict that caches data
        """Initialize the Move class"""
        self._ability_cache = {}

    def get(self, name_or_id) -> dict:
        """
        Retrieve data for a specific Move.

        Args:
        name_or_id (str or int): Name or ID of the Move.

        Returns:
            dict or None: A dictionary containing the Move data,
            or None if the request fails.
        """
        if name_or_id in self._ability_cache:
            return self._ability_cache[name_or_id]

        response = requests.get(f"{url}/{name_or_id}")
        if response.status_code == 200:
            data = response.json()
            self._ability_cache[name_or_id] = data
            return data
        else:
            return None

    def get_ability(self, name_or_id) -> dict:
        """
        Retrieve data for a specific Move.

        Args:
        name_or_id (str or int): Name or ID of the Move.

        Returns:
            dict or None: A dictionary containing the ability data,
            or None if the request fails.
        """
        ability_data = self.get(name_or_id)
        if ability_data:
            ability = {
                'name': ability_data['name'],
                'effect': ability_data['effect_entries'][1]['effect'],
            }
            return ability
        else:
            return None

    def get_pokemon_can_have_ability(self, name_or_id) -> list:
        """
        Retrieve which Pokemon can have this specific ability

        Args:
        name_or_id (str or int): Name or ID of the Move.

        Returns:
            list or None: A list containing the names of Pokemon,
            or None if the request fails.
        """
        ability_data = self.get(name_or_id)
        pkmn_names = []
        if ability_data:
            for i in ability_data['pokemon']:
                pkmn_names.append(i['pokemon']['name'])
            return pkmn_names
        else:
            return None
