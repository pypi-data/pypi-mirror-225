import requests
from datetime import datetime
from .extra import headers
from .exceptions import IncorrectDateError

class Schedule:

  def __init__(self, __cookies : dict)-> None:
    self.__cookies = __cookies
    
  def get_schedule(self, __date : str) -> list:
       
    correct_date = datetime.strptime(__date, "%d.%m.%Y").strftime('%Y-%m-%d')
    
    params = {'start': correct_date,'end': correct_date}
    response = requests.get('https://cabinet.ruobr.ru/student/get_schedule/g0/',
                            cookies=self.__cookies,
                            headers=headers,
                            params=params)
    response = response.json()
    
    if response:
      return response
    else :
      raise IncorrectDateError(f'Invalid date {__date}')

  def get_text(self, __date : str , formating : str = '|{time}| {lesson}') -> str:
     
    """
    Возвращает текст с расписанием по заданной дате\n
    :param __date: Дата для которой нужно получить расписание DD.MM.YYYY
    :param formating: Строка форматирования {time} - {lesson}
    :return: Отформатированный текст с расписанием
    """
    # Сортировка по времени
    data = sorted(self.get_schedule(__date), key= lambda x : x['start'])
    time,lesson  = [],[]
    
    for i in data:
      time.append(f"{i['start'].split('T')[1][:5]} - {i['end'].split('T')[1][:5]}")
      lesson.append(f'{i["title"].splitlines()[0]}')


    rows = []
    for time,lesson in zip(time,lesson):
      dk = {'time':time,'lesson':lesson}
      row = formating.format(**dk)
      rows.append(row)
    return '\n'.join(rows)  

