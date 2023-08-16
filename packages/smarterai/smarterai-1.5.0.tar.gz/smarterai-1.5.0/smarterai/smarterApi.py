import json
import logging
import traceback
from smarterai.smarterStore import SmarterStore
from typing import Callable, Optional, Any, Tuple, Union

logger = logging.getLogger("__SMARTER_API__")
logger.setLevel(level=logging.WARNING)


class SmarterMessage(dict):
    pass


class SmarterApi:
    def __init__(self,
                 app_slug: str,
                 deploy_dir: str,
                 delegate: Callable[[SmarterMessage, str], Optional[SmarterMessage]],
                 db,
                 task_manager,
                 smarter_logger):
        self.__smarter_store = SmarterStore(deploy_dir=deploy_dir)
        self.__core = self.__smarter_store.get_manifest_property(property_sequence="core")
        self.__usage_key = "_usageKey"
        self.delegate = delegate
        self.__db = db
        self.app_slug = app_slug
        self.task_manager = task_manager
        self.smarter_logger = smarter_logger
        self.logging_levels = {"DEBUG": logging.DEBUG,
                               "INFO": logging.INFO,
                               "ERROR": logging.ERROR,
                               "WARN": logging.WARNING,
                               "WARNING": logging.WARNING}

    @staticmethod
    def __is_number(val: Any) -> bool:
        if type(val) in [int, float]:
            return True
        if not isinstance(val, str):
            return False
        if val.isdigit() or val.replace(".", "", 1).isdigit():
            return True
        else:
            return False

    def __check_limit(self, usage_data, exp_slug) -> int:
        state = self.__core.get("state")
        if not exp_slug or state != "inUse":
            # Experiment's creator incrementing their own usage
            return 0
        trial_limit = self.__smarter_store.get_manifest_property(property_sequence="price.paygTrialUnits")
        trial_limit = eval(trial_limit) if SmarterSender.__is_number(trial_limit) else None
        is_subscribed = self.__core.get("isSubscribed")
        if not is_subscribed and trial_limit and usage_data.get(exp_slug) > trial_limit:
            # Reached the trial limit
            return -1
        return usage_data.get(exp_slug)

    def __increment_usage(self, inc: int, user_id: str) -> Any:
        exp_slug = self.__core.get("expSlug")
        usage_data = self.__smarter_store.read_global_store(pattern=self.__usage_key)
        if user_id not in usage_data:
            usage_data[user_id] = {}
        project_slug = self.__core.get("slug")
        if exp_slug not in usage_data:
            usage_data[user_id][exp_slug] = 0
        usage_data[user_id][exp_slug] += inc
        limit_reached = self.__check_limit(usage_data=usage_data, exp_slug=exp_slug)
        if limit_reached in [0, -1]:
            return limit_reached
        self.__smarter_store.write_global_store(pattern="index." + self.__usage_key,
                                                data=usage_data)
        new_message = SmarterMessage({"action": "updateUsage",
                                      "args": {"expSlug": exp_slug,
                                               "projectSlug": project_slug,
                                               "value": usage_data[exp_slug]
                                               }})
        self.send_message(message=new_message, port='#gui')
        return usage_data[exp_slug]

    def __get_usage(self, user_id: str) -> int:
        usage_data = self.__smarter_store.read_global_store(pattern=self.__usage_key)
        exp_slug = self.__core.get("expSlug")
        return usage_data.get(user_id, {}).get(exp_slug, 0)

    def __get_user(self, schema_id: str, user_id: str, data_type_filter: str = None) -> Tuple:
        """
           Gets the current user's previously persisted data.
            Args:
                :param data_type_filter:  Optional - It can be used to identify what type of data are you getting.
                    Use this if you had data_type_id in SmarterApi.set_user_data
                :param user_id: Ignored for backward compatability
           Returns:
                A tuple of all current user's data
        """
        if not user_id or not schema_id:
            logger.error(f"get_user_data found missing ids for the current message. "
                         f"Got currentId: {user_id} and schemaId: {schema_id}")
            return ()
        if not self.check_table_exists(schema_name=schema_id, table_name='static'):
            return ()
        if data_type_filter:
            query = f"SELECT rawdata " \
                    f"FROM {schema_id}.static " \
                    f"WHERE type='{self.app_slug}' " \
                    f"AND sourcetype='APP' " \
                    f"AND subtype='{data_type_filter}'" \
                    f"AND custid='{user_id}'"
        else:
            query = f"SELECT rawdata " \
                    f"FROM {schema_id}.static " \
                    f"WHERE type='{self.app_slug}' " \
                    f"AND sourcetype='APP' " \
                    f"AND custid='{user_id}'"
        return self.query_data_lake(sql_query=query, commit=False)

    def __set_user(self, schema_id: str, user_id: str, data: Any, data_type_id: str = None) -> None:
        def merge_data(old_data: Any, new_data: Any) -> Any:
            if isinstance(old_data, dict) and isinstance(new_data, dict):
                return {**old_data, **new_data}
            else:
                return new_data

        existing_data = self.__get_user(schema_id=schema_id,
                                        user_id=user_id,
                                        data_type_filter=data_type_id)
        existing_data = existing_data[0][0] if existing_data else None
        updated_data = merge_data(old_data=existing_data, new_data=data)
        try:
            string_data = json.dumps(updated_data)
        except Exception:
            logger.error(f"Failed to convert user data to JSON for the user {user_id}")
            logger.error(traceback.format_exc())
            return
        if data_type_id:
            insert_query = "INSERT INTO %s.static (custid, type, sourcetype, subtype, rawdata, normdata) " \
                           "VALUES %s" % (
                               schema_id,
                               (user_id, self.app_slug, 'APP', data_type_id, string_data, '{}'))

            delete_query = f"DELETE FROM {schema_id}.static " \
                           f"WHERE type='{self.app_slug}' " \
                           f"AND sourcetype='APP' " \
                           f"AND custid='{user_id}'" \
                           f"AND subtype='{data_type_id}'"

        else:
            insert_query = "INSERT INTO %s.static (custid, type, sourcetype, rawdata, normdata) " \
                           "VALUES %s" % (schema_id, (user_id, self.app_slug, 'APP', string_data, '{}'))

            delete_query = f"DELETE FROM {schema_id}.static " \
                           f"WHERE type='{self.app_slug}' " \
                           f"AND sourcetype='APP'" \
                           f"AND custid='{user_id}'"

        self.query_data_lake(sql_query=delete_query)
        self.query_data_lake(sql_query=insert_query)

    def get_app_slug(self) -> str:
        """
        Returns the current app's slug
        Returns:
            :return: string of the current app's slug
        """
        return self.app_slug

    def send_message(self, message: SmarterMessage, port: str) -> Optional[SmarterMessage]:
        """
        Takes in a message from a python code component and sends it to its output port.
        Args:
            :param message: A SmarterMessage to be sent through an output port
            :param port: The output port to be
        Returns:
            :return: Optional SmarterMessage if the receiver replies back with a message
        """
        return self.delegate(message, port)

    def set_data(self, pattern: str, data: Any, persist: bool = True) -> None:
        """
        Takes in JSON serializable data and sets it to a specific front-end GUI component.
        Args:
            :param pattern: The front-end GUI pattern to set the data to
            :param data: The data to be sent to the GUI. It needs to match the format the pattern expects the data in.
                            Example a chart expects a table-like format, while a textField expects some text.
            :param persist: Whether to save data in store or just set data in the frontend
        Returns:
            :return: None
        """
        message = SmarterMessage({"action": "setData",
                                  "args": {"pattern": pattern, "data": data}})
        return_message = self.send_message(message=message, port='#gui')
        if persist:
            current_user_id = return_message.get("user", {}).get("currentId")
            self.__smarter_store.set_pattern_data(pattern=pattern, data=data, user_id=current_user_id)

    def clear_data(self, pattern: str, persist: bool = True) -> None:
        """
        Clears any data associated with a specific pattern in the GUI components
        Args:
            :param pattern: The front-end GUI pattern to set the data to
            :param persist: Whether to save data in store or just set data in the frontend
        Returns:
            :return: None
        """
        message = SmarterMessage({"action": "setData",
                                  "args": {"pattern": pattern, "data": None}})
        return_message = self.send_message(message=message, port='#gui')
        if persist:
            current_user_id = return_message.get("user", {}).get("currentId")
            self.__smarter_store.set_pattern_data(pattern=pattern, data=None, user_id=current_user_id)

    def append_data(self, pattern: str, data: Any, limit: int, persist: bool = True) -> None:
        """
        Appends new data to previously sent data to a specific pattern.
        Args:
            :param pattern: The front-end GUI pattern to append the data to.
            :param data: The data to be appended to a GUI component's previous data.
            :param limit: If the data's total size is bigger than limit, then a sliding window will be
                implemented to hold the latest added elements
            :param persist: Whether to save data in store or just set data in the frontend
        Returns:
            :return: None
        """
        message = SmarterMessage({"action": "setData",
                                  "args": {"pattern": pattern, "data": data if isinstance(data, list) else [data]},
                                  "options": {"append": True, "limitLength": limit}})
        return_message = self.send_message(message=message, port='#gui')
        if persist:
            current_user_id = return_message.get("user", {}).get("currentId")
            self.__smarter_store.append_pattern_data(pattern=pattern, data=data, user_id=current_user_id)

    def prepend_data(self, pattern: str, data: Any, limit: int, persist: bool = True) -> None:
        """
        Prepends new data to previously sent data to a specific pattern.
        Args:
            :param pattern: The front-end GUI pattern to append the data to.
            :param data: The data to be prepended to a GUI component's previous data.
            :param limit: If the data's total size is bigger than limit, then a sliding window
                will be implemented to hold the latest added elements
            :param persist: Whether to save data in store or just set data in the frontend
        Returns:
            :return: None
        """
        message = SmarterMessage({"action": "setData",
                                  "args": {"pattern": pattern, "data": data if isinstance(data, list) else [data]},
                                  "options": {"prepend": True, "limitLength": limit}})
        return_message = self.send_message(message=message, port='#gui')
        if persist:
            current_user_id = return_message.get("user", {}).get("currentId")
            self.__smarter_store.prepend_pattern_data(pattern=pattern, data=data, user_id=current_user_id)

    def get_data(self, pattern: str) -> Any:
        """
        Returns the data set to a specific pattern if it exists, otherwise returns None
        Args:
            :param pattern: The pattern to return
        Returns:
            :return: json serializable SmarterMessage
        """
        return_message = self.send_message(message=SmarterMessage(), port="#user")
        current_user_id = return_message.get("user", {}).get("currentId")
        return self.__smarter_store.get_pattern_data(pattern=pattern, user_id=current_user_id)

    def reply_back(self, message: SmarterMessage) -> None:
        """
        Takes in a message to reply back to front-end REST/Websocket topics. An equivalent  to 'return' with a message.
        Uses built-in port #action to identify the front-end topic
        Args:
            :param message: A SmarterMessage JSON Serializable
        Returns:
            :return: None
        """

        self.send_message(message=message, port='#action')

    def popup_message(self, popup_type: str, message: Any) -> None:
        """
        Shows a popup message in the GUI
        Args:
            :param popup_type: = success OR info OR error OR warning
            :param message: A JSON Serializable message
        Returns:
            :return: None
        """
        new_message = SmarterMessage({"action": "message",
                                      "args": {"message": message,
                                               "type": popup_type}})
        self.send_message(message=new_message, port='#gui')

    def refresh(self) -> None:
        """
        Reloads the current page in the GUI
        Returns:
            :return: None
        """
        new_message = SmarterMessage({"action": "refresh"})
        self.send_message(message=new_message, port='#gui')

    def open_experiment(self, experiment_slug: str) -> None:
        """
        Opens a specific experiment in the GUI
        Args:
            :param experiment_slug: The experiment you wish to open
        Returns:
            :return: None
        """
        new_message = SmarterMessage({"action": "gotoExperiment",
                                      "projectSlug": experiment_slug})
        self.send_message(message=new_message, port='#gui')

    def open_page(self, page_slug: str) -> None:
        """
        Go to a specific page in the GUI
        Args:
            :param page_slug: The page slug to go to
        Returns:
            :return: None
        """
        new_message = SmarterMessage({"action": "gotoNav",
                                      "args": {"page": page_slug}})
        self.send_message(message=new_message, port='#gui')

    def set_page_json(self, page_id: str, page_json: Any) -> None:
        """
        Replaces all or parts of the page json with new json in the GUI
        Args:
            :param page_id: The ID of the page or part of the page to be replaced
            :param page_json: The JSON content to be added
        Returns:
            :return: None
        """
        new_message = SmarterMessage({"action": "setPage",
                                      "args": {"pattern": page_id,
                                               "json": page_json}})
        self.send_message(message=new_message, port='#gui')

    def set_wait(self, wait_message: str = None) -> None:
        """
        Sets the wait text on the GUI (or set it to blank to hide)
        Args:
            :param wait_message: Message to be rendered while "waiting"
        Returns:
            :return: None
        """
        new_message = SmarterMessage({"action": "setWait",
                                      "args": {"message": wait_message}})
        self.send_message(message=new_message, port='#gui')

    def increment_usage(self, increment_value: int = 1) -> int:
        """
        Increments the trial usage by the provided inc value. This is useful in the case of creating trial versions, it
        can be used to track the usage of the users of the solutions and allowing them to "try" it in a limited fashion.
        Args:
            :param increment_value: incremental value to be added to the user's usage counter
        Returns:
            :return: The user's updated usage.
                     Returns -1 if they reached or exceeded the trial limit.
                     Returns 0 if no trial limit was set
                     Otherwise returns a value >= 1 depending on the user's current usage after increment.
        """
        # TODO: use currentId for the user Id
        return_message = self.send_message(message=SmarterMessage(), port="#user")
        current_user_id = return_message.get("user", {}).get("currentId")
        return self.__increment_usage(increment_value, user_id=current_user_id)

    def get_usage(self) -> int:
        """
        Gets the current trial usage of the user.
        Returns:
            :return: The user's current usage.
                     Returns 0 if no trial limit was set or if the user is the solution's creator
                     Otherwise returns a value >= 1 depending on the user's current usage.
        """
        return_message = self.send_message(message=SmarterMessage(), port="#user")
        current_user_id = return_message.get("user", {}).get("currentId")
        return self.__get_usage(user_id=current_user_id)

    def query_data_lake(self, sql_query: str, parameters=None, paramstyle: str = "format", commit=True, *args,
                        **kwargs) -> Tuple:
        """
        Takes an SQL query on the data lake and returns all remaining rows of a query result.
        Args:
            :param sql_query: The SQL statement to execute on the data Lake
            :param args: If :`paramstyle` is ``qmark``, ``numeric``, or ``format``,
                this argument should be an array of parameters to bind into the
                statement.  If :data:`paramstyle` is ``named``, the argument should
                be a dict mapping of parameters.  If the `paramstyle` is
                ``pyformat``, the argument value may be either an array or a
                mapping.
            :param parameters: If you wish to pass parameters to the sql query you can set it here
            :param paramstyle: can be one of ('qmark', 'numeric', 'format','named', 'pyformat')
            :param commit: commits the database update permanently
        Returns:
            :return: A sequence, each entry of which is a sequence of field values making up a row.
        """
        data = self.__db.execute_sql_query(query=sql_query,
                                           parameters=parameters,
                                           paramstyle=paramstyle,
                                           commit=commit,
                                           fetch="all",
                                           *args,
                                           **kwargs)
        return data

    def write_dataframe_to_lake(self, dataframe, table_name: str, commit=True, *args, **kwargs) -> None:
        """
        Inserts a :class:`pandas.DataFrame` into table within the current dat lake.
        Args:
             :param dataframe: pd.DataFrame
                Contains row values to insert into `table`
             :param table_name: str
                The name of the table to insert to in the lake.
            :param commit: bool
                If you wish to commit the changes in the data lake permanently
        Returns:
            :return: None
         """
        self.__db.write_from_dataframe(dataframe=dataframe,
                                       table_name=table_name,
                                       commit=commit,
                                       *args,
                                       **kwargs)

    def set_user_data(self, data: Any, user_id: str = None, data_type_id: str = None) -> None:
        """
        Persists user-specific data in the data lake. This can be handy for shared apps,
        rebooting/restarting apps, and running apps in a stateless manner.
        Args:
            :param data: JSON Serializable dictionary that will be stored in the user's data lake
            :param data_type_id:  Optional - It can be used to identify what type of data are you setting.
                This will help in indexing and retrieving relevant data when using get_user_data.
            :param user_id: Ignored for backward compatability
       Returns:
            None
        """
        if user_id is not None:
            logger.warning("DeprecationWarning: use of user_id in set_user_data is deprecated and will be ignored!")
        return_message = self.send_message(message=SmarterMessage(), port="#user")
        current_user_id = return_message.get("user", {}).get("currentId")
        current_schema_id = return_message.get("user", {}).get("schema")
        if not current_user_id or not current_schema_id:
            logger.error(f"set_user_data found missing ids for the current message. "
                         f"Got currentId: {current_user_id} and schemaId: {current_schema_id}")
            return
        self.__set_user(schema_id=current_schema_id,
                        user_id=current_user_id,
                        data=data,
                        data_type_id=data_type_id)

    def set_user_session(self, data: Any, data_type_id: str = None) -> None:
        """
        Persists user's session-specific data in the data lake. This can be handy for apps remembering the user's
        session's usage data
        Args:
            :param data: JSON Serializable dictionary that will be stored in the user's data lake
            :param data_type_id:  Optional - It can be used to identify what type of data are you setting.
                This will help in indexing and retrieving relevant data when using get_user_data.
       Returns:
            None
        """

        return_message = self.send_message(message=SmarterMessage(), port="#user")
        user_id = return_message.get("user", {}).get("userId")
        current_schema_id = return_message.get("user", {}).get("schema")
        if not user_id or not current_schema_id:
            logger.error(f"set_user_data found missing ids for the current message. "
                         f"Got currentId: {user_id} and schemaId: {current_schema_id}")
            return
        self.__set_user(schema_id=current_schema_id,
                        user_id=user_id,
                        data=data,
                        data_type_id=data_type_id)

    def check_table_exists(self, table_name: str, schema_name: str = None) -> bool:
        """
        Checks if a table exists in the Data Lake.
        Usage Examples:
        1. check_table_exists(table_name='static')
            => Returns True if <current_user_id>.static exists
        2. check_table_exists(table_name='static', schema_name='user_id')
            => Returns True if user_id.static exists
        3. check_table_exists(table_name='user_id.static')
            => Returns True if user_id.static exists
        4. check_table_exists(table_name='user_id.static', schema_name='other_user_id')
            => Returns True if user_id.static exists (schema_name will be ignored)
        Args:
            table_name: Whether 'static' or 'events'
            schema_name: the schema for the table. If not provided it will default to the current user's ID.

        Returns:
            True if the schema_name.table_name exits, False otherwise
        """
        if not schema_name:
            return_message = self.send_message(message=SmarterMessage(), port="#user")
            schema_name = return_message.get("user", {}).get("schema")
        if "." in table_name:
            s_t = table_name.split(".")
            if len(s_t) != 2:
                return False
            schema_name = s_t[0]
            table_name = s_t[1]
        query = f"SELECT EXISTS (" \
                f"SELECT FROM pg_tables " \
                f"WHERE schemaname = '{schema_name}'" \
                f"AND tablename  = '{table_name}')"
        res = self.query_data_lake(sql_query=query, commit=False)
        return res[0][0] if res else False

    def get_user_data(self, user_id: str = None, data_type_filter: str = None) -> Tuple:
        """
           Gets the current user's previously persisted data.
            Args:
                :param data_type_filter:  Optional - It can be used to identify what type of data are you getting.
                    Use this if you had data_type_id in SmarterApi.set_user_data
                :param user_id: Ignored for backward compatability
           Returns:
                A tuple of all current user's data
        """
        if user_id is not None:
            logger.warning("DeprecationWarning: use of user_id in get_user_data is deprecated and will be ignored!")
        return_message = self.send_message(message=SmarterMessage(), port="#user")
        current_user_id = return_message.get("user", {}).get("currentId")
        current_schema_id = return_message.get("user", {}).get("schema")
        return self.__get_user(schema_id=current_schema_id,
                               user_id=current_user_id,
                               data_type_filter=data_type_filter)

    def notify_data_lake(self, table: str, user_id: str, source_type: str, type: str,
                         last_id: Union[str, int, None]) -> None:
        """
        Notifies the data lake that an update has happened in case of some listeners watching for lake updates
        Args:
            table: Table name, 'events' or 'static'
            user_id: The id for the relevant user
            source_type: Source type that is updated in the data lake
            type: type that is updated in the data lake
            last_id: the last ID in the table before the data was inserted

        Returns:
            None
        """
        message = SmarterMessage({"table": table,
                                  "userId": user_id,
                                  "type": type,
                                  "sourceType": source_type,
                                  "lastId": last_id})
        self.send_message(message=message, port='#lake')
        pass

    def get_user_id(self) -> str:
        """
        :return: The current user's ID of type string. If no user exists (ex. calling get_user_id in boot)
                the returned string will be an empty string
        """
        return_message = self.send_message(message=SmarterMessage(), port="#user")
        current_user_id = return_message.get("user", {}).get("currentId", "")
        return current_user_id

    def submit_task(self, app_task: Callable, maintain_sequential_execution=True, callback: Callable = None,
                    *args, **kwargs) -> None:
        """
        Time Expensive tasks can be executed in a threading environment to free up the main App thread
        to receive and process other messages easily. An expensive task can be training step, inference, etc.
        The API allows you to submit the function(s) (called tasks) you want to run,
        along with the functions’ parameters, and a flag to specify if you want to run multiple submitted tasks
        concurrently or in sequence for each user.
        Defaults to Sequential FIFO execution.
        i.e. if you submit Task1 first and then Task2 it will not start with Task2 unless Task1 is done.
        Args:
            :param app_task: The method you wish to run in a separate thread
            :param maintain_sequential_execution: If you wish to run multiple tasks for the same user in FIFO sequence
                then you to set this to True. It is recommended to set to False if both tasks are independent.
            :param callback: An optional callback method that can be called when the task is completed. The function
                should have 1 input of type concurrent.futures.Future that you can use to fetch the task results using
                future.result(). Example:
                def custom_callback(future :concurrent.futures.Future):
                    print(f'The custom callback was called with task result {future.result()}')
            *args: All the arguments you wish to pass to the app_task callable. Make sure not to use core_user_id
                as that is unique to the api, and it will be overwritten.
            **kwargs:  All the keywords arguments you wish to pass to the app_task callable.
                Make sure not to use core_user_id as that is unique to the api, and it will be overwritten.

        Returns:
            None
        """
        return_message = self.send_message(message=SmarterMessage(), port="#user")
        current_core_user_id = return_message.get("user", {}).get("currentId")
        self.task_manager.submit_task(core_user_id=current_core_user_id,
                                      app_task=app_task,
                                      maintain_sequential_execution=maintain_sequential_execution,
                                      callback=callback,
                                      *args, **kwargs)

    def get_tasks_results(self, wait_for_return: bool = False, as_completed: bool = True,
                          clean_up_results: bool = False) -> Optional[list]:
        """
        Gives you access to the returned values from the previously submitted tasks for the current user.
        It will raise InvalidUserException if the current user has been idle for a while/hasn't submitted
        a task recently.
        Args:
            :param wait_for_return:  if set to True will wait until all the tasks for the current user are done,
                get all the return values, adds them to a list and returns them.
            :param as_completed: if set to True will add the return results in a list in the order of the tasks
                have been completed, otherwise it will add them in the order they were submitted.
                Example Task1 submitted at T0 and tasks 1 minute, Task2 submitted at T1 and tasks 30 seconds.
                If as_completed=True return result will be [<Task2_return_result>, <Task1_return_result>],
                otherwise [<Task1_return_result>, <Task2_return_result>]
            :param clean_up_results: By default the results for each submitted task are persisted for some time,
                it means that for each get_tasks_results you will receive a list of all the submitted tasks results.
                If this is not a behaviour you want, then you need to set clean_up_results=True

        Returns:
            List of returned results from each submitted task for the current user.
        """
        return_message = self.send_message(message=SmarterMessage(), port="#user")
        current_core_user_id = return_message.get("user", {}).get("currentId")
        try:
            res = self.task_manager.get_result(user_id=current_core_user_id,
                                               as_completed=as_completed,
                                               wait=wait_for_return,
                                               clean_up=clean_up_results)
            return res
        except Exception:
            logger.error(f"Failed to get task results for user: {current_core_user_id}")
            logger.error(traceback.format_exc())

    def is_busy(self) -> bool:
        """
        Checks if the current user's thread(s) are busy executing tasks.
        It will raise InvalidUserException if the current user has been idle for a while/hasn't submitted
        a task recently.
        Returns:
            True if the current user's thread is busy with a previously submitted task
        """
        return_message = self.send_message(message=SmarterMessage(), port="#user")
        current_user_id = return_message.get("user", {}).get("currentId")
        try:
            return self.task_manager.is_busy(user_id=current_user_id)
        except Exception:
            logger.error(f"Failed to check status for user{current_user_id}")
            logger.error(traceback.format_exc())

    def debug(self, log: Any, exc_info: bool = False, *args, **kwargs) -> None:
        """
        Sending debug log to Smarter.ai's logging system
        Args:
            :param log: The logging message
            :param exc_info: if set to True it will log any exception information if/when they are thrown
        Returns:
            :return: None
        """
        props = self.send_message(message=SmarterMessage(), port="#user") or {}
        self.smarter_logger.debug(props, log, exc_info, *args, **kwargs)

    def info(self, log: Any, exc_info: bool = False, *args, **kwargs) -> None:
        """
        Sending info log to Smarter.ai's logging system
        Args:
            :param log: The logging message
            :param exc_info: if set to True it will log any exception information if/when they are thrown
        Returns:
            :return: None
        """
        props = self.send_message(message=SmarterMessage(), port="#user") or {}
        self.smarter_logger.info(props, log, exc_info, *args, **kwargs)

    def warn(self, log: Any, exc_info: bool = False, *args, **kwargs) -> None:
        """
        Sending warning log to Smarter.ai's logging system
        Args:
            :param log: The logging message
            :param exc_info: if set to True it will log any exception information if/when they are thrown
        Returns:
            :return: None
        """
        props = self.send_message(message=SmarterMessage(), port="#user") or {}
        self.smarter_logger.warn(props, log, exc_info, *args, **kwargs)

    def error(self, log: Any, exc_info: bool = False, *args, **kwargs) -> None:
        """
        Sending error log to Smarter.ai's logging system
        Args:
            :param log: The logging message
            :param exc_info: if set to True it will log any exception information if/when they are thrown
        Returns:
            :return: None
        """
        props = self.send_message(message=SmarterMessage(), port="#user") or {}
        self.smarter_logger.error(props, log, exc_info, *args, **kwargs)

    def set_logger_name(self, name: str) -> None:
        """
        Changing/Setting the logger name for the current code
        Args:
            :param name: The logger's new name
        Returns:
            :return: None
        """
        self.smarter_logger.set_logger_name(logger_name=name)

    def set_logger_level(self, level: str) -> None:
        """
        Changing/Setting the logger's level for the current code
        Args:
            :param level: The logger's new level
        Returns:
            :return: None
        """
        if level not in self.logging_levels:
            logger.error(f"Please set a valid level. Supported Levels: {list(self.logging_levels.keys())}")
            return
        self.smarter_logger.set_logger_level(logging_level=level)

    def set_error(self, error: str) -> None:
        """
        Notifying the stream of an error message
        Args:
            :param error: The error message
        Returns:
            :return: None
        """
        self.set_data(data=error, pattern="error", persist=False)

    def set_result(self, data: Any) -> None:
        """
        Sending data to the stream's next steps
        Args:
            :param data: The data to be sent
        Returns:
            :return: None
        """
        self.set_data(data=data, pattern="success", persist=False)


SmarterSender = SmarterApi
