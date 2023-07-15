from modules.models.download.library_resource import LibraryResource


class GameCore():
    id: str
    root: str
    type: str
    main_class: str
    inherits_form: str
    java_version: int
    library_resources: list[LibraryResource]

