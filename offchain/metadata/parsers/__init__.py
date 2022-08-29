from offchain.base.types import StringEnum

from .base_parser import BaseParser
from .collection.collection_parser import CollectionParser
from .collection.ens import ENSParser
from .collection.foundation import FoundationParser
from .collection.superrare import SuperRareParser
from .collection.punks import PunksParser
from .schema.opensea import OpenseaParser
from .schema.unknown import UnknownParser
from .schema.schema_parser import SchemaParser
