# import ydb
# import ydb.iam

# import os
# def run(endpoint, database):
#     driver_config = ydb.DriverConfig(
#         os.getenv("YDB_ENDPOINT"), os.getenv("YDB_DATABASE"), 
#         credentials=ydb.AccessTokenCredentials( os.getenv("aim_token"))
#         # credentials=ydb.iam.ServiceAccountCredentials(
#         #     service_account_id='ajehq0ijot1l2b9bre0m',
#         #     access_key_id='ajek681btmgmn714nep5',
#         #     private_key=PRIVATE_KEY
#         # )
#     )
#     with ydb.Driver(driver_config) as driver:
#         try:
#             driver.wait(timeout=5)
#         except Exception:
#             print("Connect failed to YDB")
#             print("Last reported errors by discovery:")
#             print(driver.discovery_debug_details())
#             exit(1)

from traceback import format_exc
import os
import ydb
from base_struct import Task, Employee
from typing import List
class Crud:
    def __init__(self):
        self.database = os.getenv("YDB_DATABASE")
        self.end_point = os.getenv("YDB_ENDPOINT")
        self.AIM_TOKEN = os.getenv("AIM_TOKEN")
        self.is_prod = os.getenv("IS_PROD")
        cur_credentials = None if self.is_prod == "True" else ydb.AccessTokenCredentials(self.AIM_TOKEN)
        self.driver = ydb.Driver(
            endpoint=self.end_point,
            database=self.database,
            credentials=cur_credentials
        )        
        self.driver.wait(fail_fast=True, timeout=5)
        self.session = self.driver.table_client.session().create()
    def get_employee_by_chat_id(self, chat_id):
        try:
            query = """
            PRAGMA TablePathPrefix("{}");
            DECLARE $chat_id AS Uint64;            
            SELECT
                name, last_name, middle_name, phone, position, chat_id,                
            FROM employee
            WHERE chat_id = $chat_id;
            """.format(self.database)

            prepared_query = self.session.prepare(query)
            result_sets = self.session.transaction(ydb.SerializableReadWrite()).execute(
                prepared_query, {
                    '$chat_id': chat_id,                        
                },
                commit_tx=True
            )    
        except TimeoutError:
            return self.driver.discovery_debug_details()
        except Exception:
            return 'sadsadsa' + format_exc()
        return [
                Employee(**data)
            for data in result_sets[0].rows]

    def get_employee_by_phone(self, phone):
        try:
            query = """
            PRAGMA TablePathPrefix("{}");
            DECLARE $phone AS Uint64;            
            SELECT
                name, last_name, middle_name                
            FROM employee
            WHERE phone = $phone;
            """.format(self.database)

            prepared_query = self.session.prepare(query)
            result_sets = self.session.transaction(ydb.SerializableReadWrite()).execute(
                prepared_query, {
                    '$phone': phone,                        
                },
                commit_tx=True
            )    
        except TimeoutError:
            return self.driver.discovery_debug_details()
        except Exception:
            return 'sadsadsa' + format_exc()
        return result_sets[0].rows
    def set_chat_id(self, chat_id:int, phone:int):
        try:        
            query = """
            PRAGMA TablePathPrefix("{}");

            DECLARE $chat_id AS Uint64;
            DECLARE $phone AS Uint64;

            UPDATE employee
            SET chat_id = CAST($chat_id AS Uint64)
            WHERE $phone = phone
            """.format(self.database)
            prepared_query = self.session.prepare(query)
            tx = self.session.transaction(ydb.SerializableReadWrite()).begin()
            tx.execute(
                prepared_query, {
                    '$chat_id': chat_id,
                    '$phone': phone,                
                }
            )        
            tx.commit()
            return 'Авторизация прошла успешно'
        except Exception:
            return format_exc()
    def get_project_list(self):
        try:        
            query = """
            PRAGMA TablePathPrefix("{}");
            
            SELECT
               *                
            FROM project
            """.format(self.database)

            prepared_query = self.session.prepare(query)
            result_sets = self.session.transaction(ydb.SerializableReadWrite()).execute(
                prepared_query, {},
                commit_tx=True
            )    
        except Exception:
            return format_exc()
        return result_sets[0].rows

    def get_empolyee_list(self)-> List[Employee]:
        try:        
            query = """
            PRAGMA TablePathPrefix("{}");
            SELECT
               *                
            FROM employee
            """.format(self.database)

            prepared_query = self.session.prepare(query)
            result_sets = self.session.transaction(ydb.SerializableReadWrite()).execute(
                prepared_query, {},
                commit_tx=True
            )    
        except Exception:
            return format_exc()
        return [
            Employee(**empl)
        for empl in result_sets[0].rows]
    def set_task(self, task:Task, chat_id_from:int ):
        try:        
            query = """
            PRAGMA TablePathPrefix("{}"); 

            DECLARE $executor_id AS Uint64;
            DECLARE $project_id AS Utf8;
            DECLARE $task_deadline AS Utf8;
            DECLARE $task_discription AS Utf8;
            DECLARE $task_name AS Utf8;
            DECLARE $chat_id_from AS Uint64;

            $auther_id = (
            SELECT
                phone
            FROM employee
            WHERE chat_id = $chat_id_from
            );

            $max_id = (
            SELECT 
                MAX(id)+1 
            FROM task
            );

            $parse = DateTime::Parse("%d.%M.%Y");
            $cur_date = DateTime::MakeDatetime($parse($task_deadline));
            UPSERT INTO task
                    (id,     executor_id,  project_id,  task_deadline,  task_discription,   task_name, auther_id )
            VALUES ($max_id, $executor_id, $project_id, $cur_date,      $task_discription, $task_name, $auther_id );
            """.format(self.database)

            prepared_query = self.session.prepare(query)
            self.session.transaction(ydb.SerializableReadWrite()).execute(
                prepared_query, {
                    '$executor_id': task.empl.phone,
                    '$project_id': task.project,
                    '$task_deadline': task.deadline,
                    '$task_discription': task.discription,
                    '$task_name': task.title,
                    '$chat_id_from': chat_id_from
                },
                commit_tx=True
            )    
        except Exception:
            return format_exc()
        return f'Задача создана'
    def get_task_by_chat_id_to_me(self, chat_id:int)->List[Task]:
        try:
            query = f"""
            PRAGMA TablePathPrefix("{self.database}");
            DECLARE $chat_id AS Uint64;
            
            $format = DateTime::Format("%d.%M.%Y");

            $my_phone = (SELECT phone FROM employee WHERE chat_id = $chat_id);

            SELECT
                name, last_name, middle_name, phone, position, chat_id,
                task_name AS title, project_id As project , $format(task_deadline) AS deadline, task_discription AS discription,
            FROM
                task
            INNER JOIN
                employee
            ON employee.phone = task.auther_id
            WHERE task.executor_id = $my_phone;
            """

            prepared_query = self.session.prepare(query)
            result_sets = self.session.transaction(ydb.SerializableReadWrite()).execute(
                prepared_query, {
                    '$chat_id': chat_id,                        
                },
                commit_tx=True
            )    
        except TimeoutError:
            return self.driver.discovery_debug_details()
        except Exception:
            return 'sadsadsa' + format_exc()
        # return result_sets[0].rows
        return [
            Task(auther=Employee(**dict_task), empl='я', **dict_task)
        for dict_task in result_sets[0].rows]
    def get_task_by_chat_id_from_me(self, chat_id:int)->List[Task]:
        try:
            query = f"""
            PRAGMA TablePathPrefix("{self.database}");
            DECLARE $chat_id AS Uint64;
            
            $format = DateTime::Format("%d.%M.%Y");
            $my_phone = (SELECT phone FROM employee WHERE chat_id = $chat_id);
            SELECT
                name, last_name, middle_name, phone, position, chat_id,
                task_name AS title, project_id As project , $format(task_deadline) AS deadline, task_discription AS discription,
            FROM
                task
            INNER JOIN
                employee
            ON employee.phone = task.executor_id
            WHERE task.auther_id = $my_phone;
            """

            prepared_query = self.session.prepare(query)
            result_sets = self.session.transaction(ydb.SerializableReadWrite()).execute(
                prepared_query, {
                    '$chat_id': chat_id,                        
                },
                commit_tx=True
            )    
        except TimeoutError:
            return self.driver.discovery_debug_details()
        except Exception:
            return 'sadsadsa' + format_exc()
        # return result_sets[0].rows
        return [
            Task(empl=Employee(**dict_task), auther='я', **dict_task,)
        for dict_task in result_sets[0].rows]