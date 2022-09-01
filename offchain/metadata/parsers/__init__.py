from offchain.base.types import StringEnum

from .base_parser import BaseParser
from .collection.collection_parser import CollectionParser
from .collection.ens import ENSParser
from .collection.foundation import FoundationParser
from .collection.superrare import SuperRareParser
from .collection.punks import PunksParser
from .collection.hashmasks import HashmasksParser
from .collection.autoglyphs import AutoglyphsParser
from .collection.loot import LootParser
from .collection.nouns import NounsParser
from .collection.chainrunners import ChainRunnersParser
from .schema.opensea import OpenseaParser
from .catchall.default_catchall import DefaultCatchallParser
from .schema.schema_parser import SchemaParser
