import asyncio
import aiohttp
from bs4 import BeautifulSoup
from datetime import datetime
from dataclasses import dataclass
from .extra import crop, headers

@dataclass
class Journal():
  
  def __repr__(self) -> str:
    return f"{self.subject}[{self.mark}]"
  
  date : datetime
  subject : str 
  mark : str

class Marks():
  
  def __init__(self, __cookies : dict) -> None:
    self.__cookies = __cookies
  
  @staticmethod
  def __group_journals(journals : list[Journal]) -> list[Journal]:
    grouped_journals = {}
    for journal in journals:
        key = (journal.date, journal.subject)
        if key in grouped_journals:
            grouped_journals[key].mark += f", {journal.mark}"
        else:
            grouped_journals[key] = Journal(date=journal.date, mark=str(journal.mark), subject=journal.subject)
            
    # Преобразуем словарь обратно в список объектов Journal
    grouped_journals_list = list(grouped_journals.values())
    
    return grouped_journals_list
  
  def __marks(self) -> list[Journal]:

    async def pagination(session : aiohttp.ClientSession) -> int:
      response = await session.get('https://cabinet.ruobr.ru//student/progress/',cookies = self.__cookies,headers=headers)
      soup = BeautifulSoup(await response.text(), 'lxml')
      href_list = soup.find('ul',class_='pagination noprint').find_all('a')[-1]
      number = crop(str(href_list),'?page=', '"')
      return int(number)
    
    async def catch_page(url: str ,session : aiohttp.ClientSession):
      async with session.get(url=url,headers=headers,cookies = self.__cookies) as response:
        return await response.text()
        
    async def pages(timeout: float):
      tasks = []
      async with aiohttp.ClientSession() as session:
        pagination_num = await pagination(session)
        
        for num in range(pagination_num,0,-1):
          url = f"https://cabinet.ruobr.ru//student/progress/?page={num}"
          tasks.append(asyncio.create_task(catch_page(url,session))) 
          await asyncio.sleep(timeout)
          
        return await asyncio.gather(*tasks)
    
    async def sorter() -> list[Journal]:
      all_marks = []
      for page in await pages(0.0065):
        soup = BeautifulSoup(page, 'html.parser')
        data = list(map(str, soup.find_all('tr')))
        for t in data:
          cleantext = BeautifulSoup(t, 'html.parser').text.split('\n')[3:6]
          header = ['Дата', 'Дисциплина', 'Отметка']
          if cleantext != header:
            cleantext[2] = {'отлично': 5,'хорошо': 4,'удовлетворительно': 3,'неудовлетворительно': 2}[cleantext[2]]
            cleantext[0] = datetime.strptime(cleantext[0], '%d.%m.%Y')
            cleantext : Journal = Journal(date = cleantext[0], subject= cleantext[1],  mark = cleantext[2])
            all_marks.append(cleantext)
      
      
      all_marks.sort(key=lambda x: x.date)
      grouped_journals_list = self.__group_journals(all_marks)
      return grouped_journals_list
    
    async def main():
      return await sorter()
    
    return asyncio.run(main())

  def get_last_results(self) -> list[Journal]:
    import requests
    all_marks = []
    url = 'https://cabinet.ruobr.ru//student/progress/'
    response = requests.get(url,cookies=self.__cookies,headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    data = list(map(str, soup.find_all('tr')))
    for t in data:
      cleantext = BeautifulSoup(t, 'html.parser').text.split('\n')[3:6]
      header = ['Дата', 'Дисциплина', 'Отметка']
      if cleantext != header:
        cleantext[2] = {'отлично': 5,'хорошо': 4,'удовлетворительно': 3,'неудовлетворительно': 2}[cleantext[2]]
        cleantext[0] = datetime.strptime(cleantext[0], '%d.%m.%Y')
        cleantext : Journal = Journal(date = cleantext[0], subject= cleantext[1],  mark = cleantext[2])
        all_marks.append(cleantext)
            
    all_marks.sort(key=lambda x: x.date)
    grouped_journals_list = self.__group_journals(all_marks)
    return grouped_journals_list
    
  def get_all(self) -> list[Journal]:
    return self.__marks()

  