from __future__ import annotations

from dataclasses import dataclass

from .tables import Category, Typing

try:
    from ampharos_images import IMAGES_AVAILABLE, get_image  # type: ignore
except ImportError:
    IMAGES_AVAILABLE = False


@dataclass
class _BasePokemonObject:
    _term: str


@dataclass
class Ability(_BasePokemonObject):
    """Represents an ability.

    Attributes:
        name (str): The ability's name
        description (str): A description of the ability
        introduced (int): The generation the ability was introduced
    """

    name: str
    description: str
    introduced: int


@dataclass
class Item(_BasePokemonObject):
    """Represents an item.

    Attributes:
        name (str): The item's name
        description (str): A description of the item
    """

    name: str
    description: str


@dataclass
class Move(_BasePokemonObject):
    """Represents a move.

    Attributes:
        type (types.Typing): The move's typing
        name (str): The move's name
        description (str): A description of the move
        pp (int): The move's PP
        power (int): The move's power (`None` if status move or varies)
        accuracy (int): The move's accuracy (`None` if move cannot miss)
        category (types.Category): The moves category
    """

    type: Typing
    name: str
    description: str
    pp: int
    power: int
    accuracy: int
    category: Category


@dataclass
class PokemonName(_BasePokemonObject):
    """Represents a Pokemon's name.

    Attributes:
        english (str): The name in English
        japanese (str): The name in Romanji
        kana (str): The name in Kana
    """

    english: str
    japanese: str | None
    kana: str | None


@dataclass
class PokemonBaseStats(_BasePokemonObject):
    """Represents a Pokemon's base stats.

    Attributes:
        hp (int)
        attack (int)
        defense (int)
        special_attack (int)
        special_defense (int)
        speed (int)
        total (int)
    """

    hp: int
    attack: int
    defense: int
    special_attack: int
    special_defense: int
    speed: int

    @property
    def total(self):
        return sum(
            [
                self.hp,
                self.attack,
                self.defense,
                self.special_attack,
                self.special_defense,
                self.speed,
            ]
        )


@dataclass
class PokemonTypings(_BasePokemonObject):
    """Represents a Pokemon's Typing.

    Attributes:
        primary (types.Typing)
        secondary (types.Typing)
    """

    primary: Typing
    secondary: Typing


@dataclass
class PokemonPokedexEntries(_BasePokemonObject):
    """Represents a Pokemon's Pokedex Entries.

    Attributes:
        sun (str): Pokedex entry in Pokemon Sun.
        moon (str): Pokedex entry in Pokemon Moon.
    """

    sun: str
    moon: str


@dataclass
class PokemonAbilities(_BasePokemonObject):
    """Represents a Pokemon's Abilities.

    Attributes:
        primary (types.Ability)
        secondary (types.Ability)
        hidden (types.Ability)
    """

    primary: Ability
    secondary: Ability
    hidden: Ability


@dataclass()
class Pokemon(_BasePokemonObject):
    """Represents a Pokemon.

    Attributes:
        name (types.PokemonName): The Pokemon's Name
        pokedex_number (int): The Pokemon's Pokedex Number
        classification (str): The Pokemon's classification
        typing (types.PokemonTypings): The Pokemon's Typing
        pokedex_entries (types.PokemonPokedexEntries): The Pokemon's Pokedex Entries
        evolutions (List[types.Pokemon]): A list of Pokemon this Pokemon can evolve into
        base_stats (types.PokemonBaseStats): The Pokemon's Base Stats
        abilities: (types.PokemonAbilities): The Pokemon's Abilities

    """

    pokedex_number: int
    classification: str
    name: PokemonName
    pokedex_entries: PokemonPokedexEntries | None
    evolutions: list[Pokemon]
    base_stats: PokemonBaseStats | None
    typing: PokemonTypings | None
    abilities: PokemonAbilities | None

    @property
    def image(self) -> bytes | None:
        if not IMAGES_AVAILABLE:
            raise ImportError("ampharos_images is not installed")
        return get_image(self)
