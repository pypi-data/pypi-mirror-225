def has_either_ids_or_names(id: int = None, name: str = None) -> bool:
    return id is not None or name is not None

def str_to_bool(s) -> bool:
     if isinstance(s, str):
          if s.lower() == 'true':
               return True
          elif s.lower() == 'false':
               return False
          else:
               raise ValueError(f'Failed to convert string value {s} to boolean.')
     elif isinstance(s, bool):
          return s
     else:
          raise TypeError(f'{s} is not a valid bool or string and cannot be converted.')
