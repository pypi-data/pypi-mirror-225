from .marks import Marks
from .cookie import RuobrCookies
from .schedule import Schedule
from .excel import ExcelTable
from .exceptions import IncorrectDateError

class RuobrParser():
  
  def __init__(self,cookie : RuobrCookies) -> None:
    self.__cookies = cookie.cookies()
    
  def marks(self) -> Marks:
    return Marks(self.__cookies)

  def schedule(self):
    return Schedule(self.__cookies)
  
  def excel(self,year : int | str ) -> ExcelTable:
    if 3 < len(str(year)) == 4 and str(year).isdigit():
      return ExcelTable(self.marks(),int(year))
    else: 
      raise IncorrectDateError("Incorrect date format. Please enter a valid year in the format YYYY")