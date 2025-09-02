from pymongo import MongoClient
from pymongo.database import Collection
from app.model import supervisor
from app.repositories.employee_repository import EmployeeRepository
from app.repositories.product_repository import ProductRepository
from app.repositories.supervisor_repository import SupervisorRepository
from app.repositories.unit_repository import UnitRepository


def add_employees(emp_repo: EmployeeRepository, user_collection: Collection):
    employees_list = []

    # fields = ["id", "name", "surname", "username", "password", "unit_id", "unit_name"]
    values = {
        "name": ["John", "Mary", "Jim", "Pam", "Andrew", "Peter"],
        "surname": ["Smith", "Jacobs", "Halpert", "Wesley", "Mathews", "Parker"],
        "username": ["js", "mj", "jh", "pw", 'am', "pp"],
        "password": ["12","12","12","12","12", "12"],
        "unit_id": ["u1", "u1", "u2", "u2", "u3", "u3"],
        "unit_name": ["unit1", "unit1", "unit2", "unit2", "unit3", "unit3"],
    }
    employees_to_add = len(values["name"])

    for i in range(employees_to_add):
        employee = {}
        for field in values.keys():
            employee[field] = values[field][i]
        # print(employee)
        employees_list.append(employee)

    result = emp_repo.insert_employees(employees_list)

    print(f"Inserted {len(result.inserted_ids)} employees")


def add_supervisors(sup_repo: SupervisorRepository):
    supervisor_list = []

    values = {
        "name": ["Bruce", "Will", "Mary"],
        "surname": ["Wayne", "Jacub", "Stokes"],
        "username": ["bw", "wj", "ms"],
        "password": ["12","12","12"],
        "unit_id": ["u1", "u2", "u3"],
        "unit_name": ["unit1", "unit2", "unit3",],
    }
    supervisors_to_add = len(values["name"])

    for i in range(supervisors_to_add):
        supervisor = {}
        for field in values.keys():
            supervisor[field] = values[field][i]
        supervisor_list.append(supervisor)

    result = sup_repo.insert_supervisors(supervisor_list)

    print(f"Inserted {len(result.inserted_ids)} supervisors")


def add_units(unit_repo: UnitRepository):
    unit_list = []

    values = {
        "id": ["u1", "u2", "u3"],
        "name": ["unit_1", "unit_2", "unit_3"],
        "volume": [100, 100, 100]
    }

    units_to_add = len(values["name"])

    for i in range(units_to_add):
        unit = {}
        for field in values.keys():
            unit[field] = values[field][i]
        unit_list.append(unit)

    result = unit_repo.insert_units(unit_list)

    print(f"Inserted {len(result.inserted_ids)} units")


def add_products(prod_repo: ProductRepository, unit_repo: UnitRepository):
    prod_list = []

    values = {
        "id": ["p1", "p2", "p3"],
        "name": ["pr1", "pr2", "pr3"],
        "quantity": [4, 5, 6],
        "sold_quantity": [1, 2, 3],
        "weight": [12, 5, 3],
        "volume": [3, 2, 1],
        "category": ["Electronics", "Clothing", "Book"],
        "purchase_price": [100, 20, 10],
        "selling_price": [150, 50, 20],
        "manufacturer": ["Acme", "Acme", "Acme"],
        "unit_gain": [],
        "unit_id": ["u1", "u2", "u3"],
    }

    products_to_add = len(values["name"])

    for i in range(products_to_add):
        unit = {}
        for field in values.keys():
            unit[field] = values[field][i]
        prod_list.append(unit)

    result = unit_repo.insert_units(prod_list)

    print(f"Inserted {len(result.inserted_ids)} units")


def main():
    # Connection for usage from the Lab
    # client = pymongo.MongoClient("83.212.238.166", 27017)
    client                = MongoClient("localhost", 27017)
    db                    = client["LogisticsDB"]
    user_collection       = db["users"]
    unit_collection       = db["units"]
    product_collection    = db["products"]


    user_collection.drop()
    unit_collection.drop()

    # Create indexes to avoid duplicates
    user_collection.create_index("id", unique=True)
    user_collection.create_index({"username": 1, "unit_id": 1}, unique=True)
    unit_collection.create_index({"id": 1})
    # TODO add index for product collection

    # repositories
    emp_repo = EmployeeRepository(user_collection)
    sup_repo = SupervisorRepository(user_collection)
    unit_repo = UnitRepository(unit_collection)

    add_employees(emp_repo, user_collection)
    add_supervisors(sup_repo)
    add_units(unit_repo)

main()
