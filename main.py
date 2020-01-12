documents = [
        {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
        {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
        {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"},
        {"type": "insurance", "number": "5400 028765"},
        {"type": "insurance", "number": "5455 002299"}
      ]

directories = {
        '1': ['2207 876234', '11-2', '5455 028765'],
        '2': ['10006', '5400 028765', '5455 002299'],
        '3': []
      }

def get_applicant(document_number):
  for document in documents:
    if document_number.strip() == document['number']:
      try:
        return document['name']
      except KeyError as error:
        return 'не указано'  
  return None

def print_documents():
  for document in documents:
    try:
        print('{} \"{}\" \"{}\", полка {}'.format(document['type'], document['number'], document['name'], get_directory_number(document['number'])))
    except KeyError as error:
        print(f'Для документа {document["number"]} не заведен ключ {error}')

def print_directories():
  for key in directories:
    print(f'Полка - {key}: ', end=' ')    
    print(*directories.get(key), sep = ', ')

def get_directory_number(document_number):
  for key in directories:
    if document_number in directories[key]:
       return key
  return None  

def add_document(document_type, document_number, document_name, directory_number):
  if document_type == '' or document_number == '' or document_name == '':
    return -1
 
  def_result = 0
  if directory_number not in directories.keys():
    directory_number = '1'
    def_result = 1
  
  documents.append({"type": document_type, "number": document_number, "name": document_name})
  directories[directory_number].append(document_number)

  return def_result

def del_document(document_number):
  
  directory_number = get_directory_number(document_number)
  if directory_number == None:
    return -1
  
  doc_del = dict()
  for document in documents:
    if document_number == document['number']:
      doc_del = document
      break
  documents.remove(doc_del)
  directories[directory_number].remove(document_number)

  return 0

def move_document(document_number, directory_number):
  if get_applicant(document_number) == None:
    return -1
  
  if directory_number not in directories.keys():
    return -2

  directories[get_directory_number(document_number)].remove(document_number)
  directories[directory_number].append(document_number)

  return 0

def add_shelf(directory_number):
  
  if directory_number in directories.keys():
    return -1    
    
  directories.setdefault(directory_number, [])
  return 0

def show_menu():
  print('Перечень команд для исполнения', 
    '\np – people – команда, которая спросит номер документа и выведет имя человека, которому он принадлежит',
    '\nl– list – команда, которая выведет список всех документов в формате passport "2207 876234" "Василий Гупкин"',
    '\ns – shelf – команда, которая спросит номер документа и выведет номер полки, на которой он находится',
    '\na – add – команда, которая добавит новый документ в каталог и в перечень полок, спросив его номер, тип, имя владельца и номер полки, на котором он будет храниться',
    '\nd – delete – команда, которая спросит номер документа и удалит его из каталога и из перечня полок',
    '\nm – move – команда, которая спросит номер документа и целевую полку и переместит его с текущей полки на целевую',
    '\nas – add shelf – команда, которая спросит номер новой полки и добавит ее в перечень',
    '\nls – list shelf – команда, которая отобразит перечень полок и документов на них',
    '\nq - quit - завершить работу программы')

def main():
  show_menu()
  while True:
    command = input('\nВведите команду ("r" чтобы вывести перечень команд): ').strip()
    if command == 'p':
      applicant = get_applicant(input('Введите номер документа: ').strip())
      if applicant != None:
        print(f'ФИО по указанному номеру документа - {applicant}')
      else:
        print('Ошибка: документ с таким номером отсуствует в нашей картотеке, либо указан пустой номер. Проверьте номер и повторите команду')
    
    elif command == 'l':
      print_documents()
    
    elif command == 's':
      number = get_directory_number(input('Введите номер документа: ').strip())
      if number != None:
        print(f'Указанный документ лежит на полке {number}')
      else:
        print('Ошибка: документ с таким номером отсуствует в нашей картотеке, либо указан пустой номер. Проверьте номер и повторите команду')

    elif command == 'a':
      
      command_result = add_document(
        input('Введите тип документа: ').strip(), 
        input('Введите номер документа: ').strip(),
        input('Введите ФИО: ').strip(),
        input('На какую полку кладем документ: ').strip())
      if command_result == 1:
        print('Документ создан и размещен на полке 1, т.к. указана несуществующая полка, либо её номер введен некорректно')
      elif command_result == 0:
        print('Документ создан')
      elif command_result == -1:
        print('Ошибка создания документа: не заполнены обязательные поля')
      
    elif command == 'd':
           
      command_result = del_document(input('Введите номер удаляемого документа: ').strip())
      if command_result == 0:
        print('Документ удален')
      else:
        print('Ошибка удаления документа: документ с таким номером отсутствует в нашей картотеке')

    elif command == 'm':
      
      command_result = move_document(
        input('Введите номер документа: ').strip(),
        input('На какую полку перемещаем документ: ').strip())
      if command_result == 0:
        print('Документ перемещен на указанную полку')
      elif command_result == -1:
        print('Ошибка перемещения документа: указанный документ не существует')
      elif command_result == -2:
        print('Ошибка перемещения документа: указанная полка не существует')
    
    elif command == 'as':
      
      command_result = add_shelf(input('Введите номер создаваемой полки: ').strip())
      if command_result ==0:
        print('Новая полка создана')
      else:
        print('Ошибка создания полки: полка с таким номером уже существует')

    elif command == 'ls':

      print_directories()
    
    elif command == 'r':

      show_menu()

    elif command == 'q':
      
      break
    
    else:
      print('Вы указали неверную команду. Попробуйте снова или нажмите "r" чтобы вывести перечень команд: ')
    
main()

