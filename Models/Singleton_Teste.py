from Models.DAO.TXTAgendaDAO import TXTAgendaDAO
from Models.DAO.JSONAgendaDAO import JSONAgendaDAO

txt1 = TXTAgendaDAO()
txt2 = TXTAgendaDAO()

json1 = JSONAgendaDAO()
json2 = JSONAgendaDAO()

print("TXT Singleton:", txt1 is txt2)
print("JSON Singleton:", json1 is json2)

print("TXT e JSON são a mesma instância:", txt1 is json1)