def singleton(cls):
    """
    Prosty dekorator implementujący wzorzec Singleton.
    Dodaje metodę statyczną get_instance() do klasy.
    """
    instances = {}

    def get_instance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    # Dodajemy metodę get_instance do klasy
    setattr(cls, 'get_instance', staticmethod(get_instance))

    return cls