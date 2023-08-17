from Parser.books_parser import BooksParser
from Parser.kingstone_parser import KingstoneParser
from Parser.sanmin_parser import SanminParser
from Parser.eslite_parser import EsliteParser
#from Parser.pchome_parser import PchomeParser
from Parser.momo_parser import MomoParser
from Parser.caves_parser import CavesParser
from Parser.tcsb_parser import TcsbParser

from Parser.yahoo_parser import YahooParser
from Parser.udn_parser import UdnParser

from Parser.taaze_parser import TaazeParser
from Parser.rakuten_parser import RakutenParser
from Parser.tenlong_parser import TenlongParser
#from Parser.linking_parser import LinkingParser
from Parser.cite_parser import CiteParser

class ParserFactory():
    _parsers = [
        BooksParser(),
        KingstoneParser(),
        SanminParser(),
        EsliteParser(),
        #PchomeParser(),
        MomoParser(),
        CavesParser(),
        TcsbParser(),
        
        YahooParser(),
        UdnParser(),
        
        TaazeParser(),
        RakutenParser(),
        TenlongParser(),
        #LinkingParser(),
        CiteParser(),
        
    ]
    def __init__(self):
        pass
    
    def get_parser(self, url):
        for p in self._parsers:
            if p.is_target_page(url):
                return p
        return None
    
    
    