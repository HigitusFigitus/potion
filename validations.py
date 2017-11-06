from app import Potion
import re


def validate_potion_name(potion_name):
  if potion_name == "":
    raise InvalidPotionError("potion_name can't be empty")
  elif potion_name[0] in ("_", "-"):
    raise InvalidPotionError(
      "potion_name cannot start with an underscore or dash")
  elif len(potion_name) not in range(4, 65):
    raise InvalidPotionError(
      "potion_name must be between 4 and 64 characters long")
  elif re.match("^[A-Za-z0-9_\-]*$", potion_name) == None:
    raise InvalidPotionError(
      "potion_name can only contain alphanumeric ascii characters, " +
      "underscores, and dashes")
  elif Potion.query.filter_by(potion_name=potion_name).first() is not None:
    raise InvalidPotionError("potion_name must be unique")


def validate_potion_type(potion_type):
  if potion_type == "":
    raise InvalidPotionError("potion_type can't be empty")
  elif potion_type not in ("passive", "active"):
    raise InvalidPotionError(
      "potion_type must either be 'passive' or 'active', both lowercase")


def validate_potion_class(potion_type, potion_class):
  if potion_class == "":
    raise InvalidPotionError("potion_class can't be empty")
  elif potion_type == "passive":
    if potion_class not in ("life", "mana"):
      raise InvalidPotionError(
        "potion_class must either be 'life' or 'mana', both lowercase")
  elif potion_type == "active":
    if potion_class not in ("fire", "poison"):
      raise InvalidPotionError(
        "potion_class must either be 'fire' or 'poison', both lowercase")


def validate_potion(potion_name, potion_type, potion_class):
  validate_potion_name(potion_name)
  validate_potion_type(potion_type)
  validate_potion_class(potion_type, potion_class)


class InvalidPotionError(Exception):
  pass
