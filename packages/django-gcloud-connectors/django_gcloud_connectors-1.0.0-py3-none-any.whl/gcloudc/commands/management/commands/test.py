from . import (
    CloudDatastoreRunner,
    locate_command,
)

BaseCommand = locate_command("test")


class Command(CloudDatastoreRunner, BaseCommand):
    pass
