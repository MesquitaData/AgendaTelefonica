from Models.DAO.AgendaDAO import AgendaDAO

dao1 = AgendaDAO()
dao2 = AgendaDAO()

print("DAO 1:", id(dao1))
print("DAO 2:", id(dao2))

print("Mesma instância:", dao1 is dao2)