import requests
url = "https://pokeapi.co/api/v2/move"


class Move:
    def __init__(self):
        # dict that caches data
        """Initialize the Move class"""
        self._move_cache = {}

    def get(self, name_or_id) -> dict:
        """
        Retrieve data for a specific Move.

        Args:
        name_or_id (str or int): Name or ID of the Move.

        Returns:
            dict or None: A dictionary containing the Move data,
            or None if the request fails.
        """
        if name_or_id in self._move_cache:
            return self._move_cache[name_or_id]

        response = requests.get(f"{url}/{name_or_id}")
        if response.status_code == 200:
            data = response.json()
            self._move_cache[name_or_id] = data
            return data
        else:
            return None

    def get_battle_info(self, name_or_id) -> dict:
        """
        Retrieve relevant battle data for a specific Move.

        Args:
        name_or_id (str or int): Name or ID of the Move.

        Returns:
            dict or None: A dictionary containing the battle Move data,
            or None if the request fails.
        """
        move_data = self.get(name_or_id)
        if move_data:
            try:
                effect_entry = move_data['effect_entries'][0]['short_effect']
            except IndexError:
                effect_entry = None

            battle_info = {
                'name': move_data['name'],
                'accuracy': move_data['accuracy'],
                'power': move_data['power'],
                'pp': move_data['pp'],
                'priority': move_data['priority'],
                'type': move_data['type']['name'],
                'damage_class': move_data['damage_class']['name'],
                'effect_chance': move_data['effect_chance'],
                'effect_entry': effect_entry
            }
            return battle_info
        else:
            return None

    def get_learned_by_pokemon(self, name_or_id) -> list:
        move_data = self.get(name_or_id)
        if move_data:
            name_list = []
            learned_by_pokemon = move_data['learned_by_pokemon']
            for pkmn in learned_by_pokemon:
                name_list.append(pkmn['name'])
        else:
            return None
        return name_list
