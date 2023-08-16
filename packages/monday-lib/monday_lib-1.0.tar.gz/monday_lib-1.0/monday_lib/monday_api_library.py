import requests
import re
import time
import logging

class monday_endpoints:
    def __init__(self, api_secret, wait_for_complexity=False, logging_file=None):
        self.secret = api_secret
        self.complexity_wait = wait_for_complexity
        self.complexity_points = 10000000
        self.requests_reset = 60
        self.complexity_retries = 0
        self.real_data_dict = []
        if logging_file:
            logging.basicConfig(filename=logging_file, encoding="utf-8",level=0)
    
    def make_request(self, body, get_raw_request=False):
        """
        Helper function for the module.\n
        Makes the request and handles timeouts.
        """
        request = None
        dataList = []

        if self.complexity_wait:
            if "query" in body[:8]:
                body = body[:8] + "complexity {after reset_in_x_seconds} " + body[8:]
            elif "mutation" in body[:11]:
                body = body[:11] + "complexity {after reset_in_x_seconds} " + body[11:]

        while self.if_next_page(body, request):
            body = self.determine_next_page(body)
            if self.complexity_points <= 1000:
                time.sleep(self.requests_reset)
            while True:
                request = requests.post("https://api.monday.com/v2", headers={
                    "Authorization":self.secret,
                    "Content-Type":"application/json",
                    "API-Version":"2023-07"
                }, json={
                    "query":str(body)
                })

                if request.status_code == 403:
                    logging.critical("API user is not authorized.")
                    raise Exception("User is not authorized")
                elif request.status_code == 401:
                    logging.critical("API User key is not correct.")
                    raise Exception("API key is not correct.")
                elif request.status_code == 429:
                    logging.warning("Rate Limited, waiting 60 seconds.")
                    time.sleep(60)
                elif request.status_code == 400:
                    logging.warning("Error: " + request.json()['error_data'])
                    raise Exception("Error: " + request.json()['error_data'])
                else:
                    break
            logging.debug('Request: ' + str(request.json()))
            if 'query' in body and not "me" in request.json()['data'].keys() and not "account" in request.json()['data'].keys():
                data_in_request = self.get_data(request.json())
                dataList.extend(data_in_request)

            if self.complexity_wait:
                self.requests_reset = request.json()['data']['complexity']['reset_in_x_seconds']
                self.complexity_points = request.json()['data']['complexity']['after']

        if 'query' in body and not "me" in request.json()['data'].keys() and not "account" in request.json()['data'].keys() and get_raw_request == False:
            return dataList
        else:
            
            return request.json()

    def if_next_page(self,body=None, request=None):
        """
        Helper function for the module.\n
        Checks if there are a new page.
        """
        if request and 'query' in body and 'page' in body:

            limit_regex = int(re.findall("(?<=limit:)(\\d*)(?=,)", body)[0])
            item_count = len(self.get_data(request.json()))

            if limit_regex == item_count:
                return True
            else:
                return False

        elif request:
            return False
        else:
            return True
    
    def determine_next_page(self, body):
        """
        Helper function for the module.\n
        Adds page to the request body.
        """
        if 'page:' in body:
            page_number = int(re.findall("(?<=page:)(\\d*)(?=\\))", body)[0])
            page_number += 1
            body = re.sub("(?<=page:)(\\d*)(?=\\))", str(page_number), body)
        return body
    
    def get_data(self, data_dict):
        """
        Helper function for the module.\n
        Used to figure out where the data is nested.
        """
        items_not_to_unpack = [
            "items",
            "replies",
            "column_values"
        ]

        headers_not_to_unpack = [
            "extensions"
        ]
        
        for key in data_dict:
            if type(data_dict[key]) == dict and key not in headers_not_to_unpack:
                self.get_data(data_dict[key])
            elif type(data_dict[key]) == list:
                self.real_data_dict = data_dict[key]

        if self.real_data_dict or self.real_data_dict == []:
            if not self.real_data_dict == []:
                for key, value in self.real_data_dict[0].items():
                    if type(value) == list and key not in items_not_to_unpack:
                        self.real_data_dict = value
            return self.real_data_dict

    def put_parameter(self, request_body, data_name, parameter_dict):
        """
        Helper function for the module.\n
        Puts additional parameters in the mutation request body.
        """

        string_keys = ["value","column_id", "column_values", "url", "config"]

        parameter_dict = {key: value for key, value in parameter_dict.items() if value}

        parameters_string = ""
        for key, parameter in parameter_dict.items():
            parameter = str(parameter).replace('"','\\"')
            if parameter == "True" or parameter == "False":
                parameter = parameter.lower()
            if list(parameter_dict.keys()).index(key) == len(parameter_dict) - 1:
                if " " in str(parameter) or key in string_keys:
                    parameters_string += f"{key}:\"{parameter}\""
                else:
                    parameters_string += f"{key}:{parameter}"
            else:
                if " " in str(parameter) or key in string_keys:
                    parameters_string += f"{key}:\"{parameter}\","
                else:
                    parameters_string += f"{key}:{parameter},"
        
        request_body_data_name_index = request_body.find(data_name + ' (') + len(data_name + ' (')
        request_body_with_parameters = request_body[:request_body_data_name_index] + parameters_string + request_body[request_body_data_name_index:]
        return request_body_with_parameters 

    def get_account_metadata(self):
        """
        Gets the current accounts metadata.
        """
        account_request = self.make_request("query { users { account { id logo show_timeline_weekends first_day_of_the_week sign_up_product_kind plan { period } tier slug }}}")[0]
        return account_request

    def get_app_subscription(self):
        """
        Gets information about the billing of the Monday subscription
        """
        app_subscription_request = self.make_request("query { app_subscription { billing_period days_left is_trial plan_id renewal_date }}")
        return app_subscription_request
    
    def get_board_activity(self, board_id, activity_from="2022-01-31", activity_to="2022-12-31"):
        """
        Gets board activity on a specific board.
        """
        board_activity_request = self.make_request('query { boards (ids: ' + str(board_id) + ') { activity_logs (limit:25, from: "' + activity_from + 'T00:00:00Z", to: "' + activity_to + 'T00:00:00Z", page:0) { id account_id user_id created_at event entity data }}}')
        return board_activity_request

    def get_all_boards(self, workspace_id=None):
        """
        Gets all boards the user has access to.
        """
        board_request = self.make_request("query { boards (limit:25, page:0) { id name state board_folder_id workspace_id creator { id } type }}")
            
        if workspace_id:
            board_request = [x for x in board_request if x['workspace_id'] == workspace_id]
        return board_request

    def create_board(self, board_name, board_kind, board_folder_id=None, workspace_id=None, template_id=None, board_owner_ids=[], board_subscriber_ids=[]):
        """
        Create board in Monday, if you are using some parameters and not others please use the parameter name like: create_board("Name", "public", template_id=12312)\n
        board_kind is one of which: public, private, or share\n
        If template_id it must be a account template.
        """
        parameter_dict = {
                "board_name":board_name,
                "board_kind":board_kind,
                "folder_id":board_folder_id,
                "workspace_id":workspace_id,
                "template_id":template_id,
                "board_owner_ids":board_owner_ids,
                "board_subscriber_ids":board_subscriber_ids
                }
        
        request_body = self.put_parameter("mutation { create_board () { id }}", "create_board", parameter_dict)
        create_board_request = self.make_request(request_body)
        return create_board_request
    
    def archive_board(self, board_id):
        """
        Archive board in Monday.
        """
        request_body = self.put_parameter("mutation { archive_board () { id } }", "archive_board", {"board_id":board_id})
        archive_board_request = self.make_request(request_body)
        return archive_board_request
    
    def add_users_to_board(self, board_id, user_ids, kind):
        """
        Add subscribers to board.\n
        user_ids is a list.
        """
        request_body = self.put_parameter("mutation { add_users_to_board () { id } }", "add_users_to_board",{"board_id":board_id, "user_ids":user_ids, "kind":kind})
        add_subscribers_to_board_request = self.make_request(request_body)
        return add_subscribers_to_board_request

    def delete_subscribers_from_board(self, board_id, user_ids):
        """
        Delete subscribers from board.\n
        user_ids is a list.
        """
        request_body = self.put_parameter("mutation { delete_subscribers_from_board () { id } }", "delete_subscribers_from_board", {"board_id":board_id, "user_ids":user_ids})
        delete_subscribers_from_board_request = self.make_request(request_body)
        return delete_subscribers_from_board_request
    
    def duplicate_board(self, board_id, duplicate_type, board_name=None, workspace_id=None, folder_id=None, keep_subscribers=False):
        """
        Duplicate a already existing board.\n
        Duplicate Types: duplicate_board_with_structure, duplicate_board_with_pulses, duplicate_board_with_pulses_and_updates
        """
        parameter_dict = {
            "board_id":board_id, 
            "duplicate_type":duplicate_type,
            "board_name":board_name,
            "workspace_id":workspace_id,
            "folder_id":folder_id,
            "keep_subscribers":keep_subscribers
        }

        request_body = self.put_parameter("mutation { duplicate_board () { board { id }}}", "duplicate_board",parameter_dict)
        duplicate_board_request = self.make_request(request_body)
        return duplicate_board_request

    def update_board(self, board_id, board_attribute_to_update, new_value):
        """
        Updates a boards attribute.\n
        Either description or name.
        """

        request_body = self.put_parameter("mutation { update_board () }", "update_board", {"board_id":board_id,"board_attribute":board_attribute_to_update, "new_value":new_value})
        update_board_request = self.make_request(request_body)
        return update_board_request
    
    def delete_board(self, board_id):
        """
        Deletes a board.
        """

        delete_board_request = self.make_request("mutation { delete_board (board_id:" + str(board_id) + ") { id }}")
        return delete_board_request

    def get_board_views(self, board_id):
        """
        Gets all board views on a specific board.
        """

        board_views_request = self.make_request("query { boards (ids: " + str(board_id) + ") { views { id name type }}}")
        return board_views_request
    
    def get_board_columns(self, board_id):
        """
        Gets all board columns on a specific board.
        """

        board_columns_request = self.make_request("query { boards (ids: " + str(board_id) + ") { columns { id archived title description type settings_str width }}}")
        return board_columns_request
    
    def create_board_column(self, board_id, column_title, column_description, column_type):
        """
        Create a column on a board.\n
        Column type can be one of the following: auto_number, checkbox, contry, color_picker, creation_log, date, dependency, dropdown\n
        email, file, hour, item_id, last_updated, link, location, long_text, numbers, people, phone, progress, rating, status, team\n
        tags, text, timeline, time_tracking, vote, week, world_clock 
        """

        request_body = self.put_parameter("mutation { create_column () { id title description type }}", "create_column", {"board_id":board_id, "title":column_title, "column_type":column_type, "description":column_description})
        create_board_column_request = self.make_request(request_body)
        return create_board_column_request
    
    def change_simple_column_value(self, board_id, item_id, column_id, new_value):
        """
        Changes a column value on a specific item on a specific board.
        """
        
        request_body = self.put_parameter("mutation { change_simple_column_value () { id }}", "change_simple_column_value", {"board_id":board_id, "item_id":item_id, "column_id":column_id, "value":new_value})
        change_simple_column_value_request = self.make_request(request_body)
        return change_simple_column_value_request

    def change_column_value(self, board_id, item_id, column_id, json_value):
        """
        //TODO: Fix JSON_value 
        Changes a column value with json values.\n
        See reference for what to put into json_value: https://developer.monday.com/api-reference/docs/guide-to-changing-column-data\n
        The library will escape the json for you.
        """

        parameter_dictionary = {
            "item_id":item_id,
            "board_id":board_id,
            "column_id":column_id,
            "value":str(json_value).replace('"','\\"')
        }

        request_body = self.put_parameter("mutation { change_column_value () { id }}","change_column_value",parameter_dictionary)
        change_column_value_request = self.make_request(request_body)
        return change_column_value_request
    
    def change_multiple_column_values(self, board_id, item_id, column_values):
        """
        Changes multiple column values, at the same time.\n
        See reference for what to put into column_values: https://developer.monday.com/api-reference/docs/columns-queries-1#change-multiple-columns-values\n
        Column_values should be JSON in a string.
        """
        
        parameter_dictionary = {
            "item_id":item_id,
            "board_id":board_id,
            "column_values":column_values.replace('"','\"')
        }

        request_body = self.put_parameter("mutation { change_multiple_column_values () { id }}","change_multiple_column_values", parameter_dictionary)
        change_multiple_column_values_request = self.make_request(request_body)
        return change_multiple_column_values_request
    
    def change_column_title(self, board_id, column_id, new_title):
        """
        Changes a columns title on a specific board.
        """

        request_body = self.put_parameter("mutation { change_column_title () { id }}", "change_column_title", {"column_id":column_id, "board_id":board_id, "title":new_title})
        change_column_title_request = self.make_request(request_body)
        return change_column_title_request

    def change_column_description(self, board_id, column_id, new_description):
        """
        Changes a columns description on a specific board.
        """
        parameter_dictionary = {
            "column_id":column_id,
            "board_id":board_id,
            "column_property":"description",
            "value":new_description
        }

        request_body = self.put_parameter("mutation { change_column_metadata () { id title description }}", "change_column_metadata", parameter_dictionary)
        change_column_description_request = self.make_request(request_body)
        return change_column_description_request

    def delete_board_column(self, board_id, column_id):
        """
        Delete a column on a specific board.
        """

        request_body = self.put_parameter("mutation { delete_column () { id }}", "delete_column", {"board_id":board_id, "column_id":column_id})
        delete_board_column_request = self.make_request(request_body)
        return delete_board_column_request
    
    def get_board_items(self, board_id):
        """
        Get board items and their column values.
        """

        request_body = "query { boards (ids: " + str(board_id) + ",limit:25, page:0) { items { id, name, creator_id, name, state, updated_at column_values { id title value text } group { id title }}}}"
        get_board_items_request = self.make_request(request_body)
        return get_board_items_request

    def create_board_item(self, board_id, item_name, group_id=None, column_values=None, create_labels_if_missing=False):
        """
        Creates item to existing board.
        """

        parameter_dictionary = {
            "board_id":board_id,
            "group_id":group_id,
            "item_name":item_name,
            "column_values":column_values,
            "create_labels_if_missing":create_labels_if_missing
        }

        request_body = self.put_parameter("mutation { create_item () { id }}", "create_item",parameter_dictionary)
        create_board_item_request = self.make_request(request_body)
        return create_board_item_request
    
    def create_board_subitem(self, parent_item_id, item_name, column_values):
        """
        Creates subitem to existing item.
        """
        
        parameter_dictionary = {
            "parent_item_id": parent_item_id,
            "item_name": item_name,
            "column_values":column_values
        }

        request_body = self.put_parameter("mutation { create_subitem () { id board { id }}}", "create_subitem", parameter_dictionary)
        create_board_subitem_request = self.make_request(request_body)
        return create_board_subitem_request
    
    def clear_item_updates(self, item_id):
        """
        Clears all item updates on item.
        """

        request_body = self.put_parameter("mutation { clear_item_updates () { id }}", "clear_item_updates", {"item_id":item_id})
        clear_item_updates_request = self.make_request(request_body)
        return clear_item_updates_request
    
    def get_board_groups(self, board_id):
        """
        Gets all groups in a board.
        """

        get_board_groups_request = self.make_request("query { boards (ids: " + str(board_id) + ") { groups { id color title }}}")
        return get_board_groups_request

    def move_item_to_group(self, item_id, group_id):
        """
        Moves item to a specific group, on a specific board.
        """

        request_body = self.put_parameter("mutation { move_item_to_group () { id }}", "move_item_to_group",{"item_id":item_id, "group_id":group_id})
        move_item_to_group_request = self.make_request(request_body)
        return move_item_to_group_request
    
    def get_item(self, item_id):
        """
        Gets a item by id.
        """

        request_body = "query { items (ids: " + str(item_id) + ") { id, name, creator_id, name, state, updated_at column_values { id title value } group { id title }}}"
        get_item_request = self.make_request(request_body)
        return get_item_request

    def archive_item(self, item_id):
        """
        Archives an item.
        """

        request_body = self.put_parameter("mutation { archive_item () { id }}", "archive_item",{"item_id":item_id})
        archive_item_request = self.make_request(request_body)
        return archive_item_request

    def delete_item(self, item_id):
        """
        Deletes an item.
        """

        request_body = self.put_parameter("mutation { delete_item () { id }}", "delete_item", {"item_id":item_id})
        delete_item_request = self.make_request(request_body)
        return delete_item_request
    
    def duplicate_item(self, board_id, item_id, with_updates=False):
        """
        Duplicates an item.
        """

        request_body = self.put_parameter("mutation { duplicate_item () { id }}", "duplicate_item", {"board_id":board_id, "item_id":item_id, "with_updates":with_updates})
        duplicate_item_request = self.make_request(request_body)
        return duplicate_item_request

    def get_items_by_column_values(self, board_id, column_id, column_value, column_type=None, state=None):
        """
        Get items filtered by a column value.
        """

        parameter_dictionary = {
            "board_id":board_id,
            "column_id":column_id, 
            "column_value":column_value,
            "column_type":column_type,
            "state":state
        }

        request_body = self.put_parameter("query { items_by_column_values () { id name created_at creator_id group { id title } parent_item { id name } state updated_at }}", "items_by_column_values", parameter_dictionary)
        get_items_by_column_values_request = self.make_request(request_body)
        return get_items_by_column_values_request
    
    def get_items_by_multiple_column_values(self, board_id, column_id, column_values=[]):
        """
        Get items filtered by multiple column values.
        """

        get_items_by_multiple_column_values_request = self.make_request('query { items_by_multiple_column_values (board_id:' + str(board_id) + ', column_id:"' + str(column_id) + '", column_values:' + str(column_values).replace("'",'"') + ') { id name created_at creator_id group { id title } parent_item { id name } state updated_at }}')
        return get_items_by_multiple_column_values_request


    def who_am_i(self):
        """
        Gets information about what user are being used in the API requests.
        """

        get_me_request = self.make_request("query { me { id birthday country_code created_at join_date email enabled id is_admin is_guest is_pending is_view_only location mobile_phone name phone photo_original photo_small photo_thumb photo_thumb_small photo_tiny time_zone_identifier title url utc_hours_diff } }")
        return get_me_request

    def create_notification_to_user(self, text, user_id, target_id, target_type):
        """
        Send notification to user, without actually creating update or item.\n
        Target_type is either Project/Post\n
        When using Project target_id must be a item or board.\n
        When using Post target_id must be an update.
        """

        parameter_dictionary = {
            "text":text,
            "user_id":user_id,
            "target_id":target_id,
            "target_type":target_type
        }

        request_body = self.put_parameter("mutation { create_notification () { text }}", "create_notification",parameter_dictionary)
        create_notification_to_user_request = self.make_request(request_body)
        return create_notification_to_user_request

    def get_monday_plan(self):
        """
        Gets information about active Monday plan.
        """

        get_monday_plan_request = self.make_request("query { account { plan { max_users period tier version }}}")
        return get_monday_plan_request
    
    def get_tags(self):
        """
        Get all tags of a board.
        """

        get_board_tags_request = self.make_request("query { tags { id name color }}")
        return get_board_tags_request
    
    def create_or_get_tag(self, board_id, tag_name):
        """
        Create a tag, if it already exists retrieve data instead.
        """

        parameter_dictionary = {
            "tag_name":tag_name,
            "board_id":board_id
        }

        request_body = self.put_parameter("mutation { create_or_get_tag () { id name color }}", "create_or_get_tag",parameter_dictionary)
        create_or_get_tag_request = self.make_request(request_body)
        return create_or_get_tag_request

    def get_teams(self):
        """
        Gets all teams.
        """

        get_teams_request = self.make_request("query { teams { id name picture_url users { id name }}}", get_raw_request=True)
        return get_teams_request
    
    def get_item_updates(self, item_id):
        """
        Gets an items updates.
        """
        get_item_updates_request = self.make_request("query { items (ids:" + str(item_id) + ") { updates (limit:25, page:0) { id body created_at creator { id name } item_id replies { id creator_id creator { id name } created_at text_body updated_at body }}}}")
        return get_item_updates_request

    def create_item_update(self, item_id, update_text, parent_update_id=None):
        """
        Create a update to an item.
        """

        parameter_dictionary = {
            "item_id":item_id,
            "body":update_text,
            "parent_id":parent_update_id
        }

        request_body = self.put_parameter("mutation { create_update () { id }}", "create_update",parameter_dictionary)
        create_item_update_request = self.make_request(request_body)
        return create_item_update_request

    def delete_item_update(self, update_id):
        """
        Delete a update to an item.
        """

        request_body = self.put_parameter("mutation { delete_update () { id }}", "delete_update", {"id":update_id})
        delete_item_update_request = self.make_request(request_body)
        return delete_item_update_request

    def get_all_users(self):
        """
        Gets all users.
        """

        get_all_users_request = self.make_request("query { users (limit:100) { id birthday country_code created_at join_date email enabled id is_admin is_guest is_pending is_view_only location mobile_phone name phone photo_original photo_small photo_thumb photo_thumb_small photo_tiny time_zone_identifier title url utc_hours_diff  }}")
        return get_all_users_request

    def get_board_webhooks(self, board_id):
        """
        Get all webhooks of a board.
        """

        get_board_webhooks_request = self.make_request("query { webhooks(board_id:" + str(board_id) + "){ id event board_id config }}")
        return get_board_webhooks_request
    
    def create_board_webhook(self, board_id, url, event, config=None):
        """
        Creates a board webhook.\n
        See documentation for how to accept the webhook: https://developer.monday.com/api-reference/docs/webhooks-1
        """

        parameter_dictionary = {
            "board_id":board_id,
            "url":url,
            "event":event,
            "config":config
        }
        request_body = self.put_parameter("mutation { create_webhook () { id board_id } }", "create_webhook", parameter_dictionary)
        create_board_webhook_request = self.make_request(request_body)
        return create_board_webhook_request
    
    def delete_board_webhook(self, webhook_id):
        """
        Delete a specific webhook on a board.
        """

        delete_board_webhook = self.make_request("mutation { delete_webhook (id:" + str(webhook_id)+ ") { id board_id }}")
        return delete_board_webhook
    
    def get_all_workspaces(self):
        """
        Get all workspaces.
        """

        get_all_workspaces_request = self.make_request("query { workspaces (limit:25, page:0) { id name kind description created_at }}")
        return get_all_workspaces_request
    
    def create_workspace(self, name, kind, description):
        """
        Creates a workspace.\n
        Kind is either open or closed.
        """

        parameter_dictionary = {
            "name":name,
            "kind":kind,
            "description":description
        }

        request_body = self.put_parameter("mutation { create_workspace () { id name kind description }}","create_workspace", parameter_dictionary)
        create_workspace_request = self.make_request(request_body)
        return create_workspace_request
    
    def delete_workspace(self, workspace_id):
        """
        Deletes a workspace by workspace_id.
        """

        request_body = self.put_parameter("mutation { delete_workspace () { id }}", "delete_workspace", {"workspace_id":workspace_id})
        delete_workspace_request = self.make_request(request_body)
        return delete_workspace_request
    
    def add_users_to_a_workspace(self, workspace_id, kind, user_ids=[]):
        """
        Subscribes users to a specific workspace.\n
        User_ids must be a list with ids as ints.\n
        Kind is either subscriber or owner
        """

        parameter_dictionary = {
            "workspace_id":workspace_id,
            "user_ids":user_ids,
            "kind":kind
        }

        request_body = self.put_parameter("mutation { add_users_to_workspace () { id }}","add_users_to_workspace",parameter_dictionary)
        add_users_to_a_workspace_request = self.make_request(request_body)
        return add_users_to_a_workspace_request

    def delete_users_from_a_workspace(self, workspace_id, user_ids=[]):
        """
        Desubscribes users from a specific workspace.\n
        User_ids must be a list with ids as ints.
        """

        parameter_dictionary = {
            "workspace_id":workspace_id,
            "user_ids":user_ids
        }

        request_body = self.put_parameter("mutation { delete_users_from_workspace () { id }}", "delete_users_from_workspace",parameter_dictionary)
        delete_users_to_a_workspace_request = self.make_request(request_body)
        return delete_users_to_a_workspace_request

    def add_teams_to_a_workspace(self, workspace_id, team_ids=[]):
        """
        Subscribes whole teams to a workspace.\n
        team_ids must be a list with ids as ints.
        """

        parameter_dictionary = {
            "workspace_id":workspace_id,
            "team_ids":team_ids
        }

        request_body = self.put_parameter("mutation { add_teams_to_workspace () { id }}","add_teams_to_workspace",parameter_dictionary)
        add_teams_to_a_workspace_request = self.make_request(request_body)
        return add_teams_to_a_workspace_request
    
    def delete_teams_from_a_workspace(self, workspace_id, team_ids=[]):
        """
        Desubscribes whole teams from a workspace.\n
        team_ids must be a list with ids as ints.
        """

        parameter_dictionary = {
            "workspace_id":workspace_id,
            "team_ids":team_ids
        }

        request_body = self.put_parameter("mutation { delete_teams_from_workspace () { id }}", "delete_teams_from_workspace",parameter_dictionary)
        delete_teams_from_a_workspace_request = self.make_request(request_body)
        return delete_teams_from_a_workspace_request

    """
    def upload_file_to_file_column(self, board_id, item_id, column_id, file_path):
        
        Uploads a file to a specific item file column.
        
        parameter_dictionary = {
            "item_id":item_id,
            "column_id":column_id,
            "file":"$file"
        }

        request_body = self.put_parameter("mutation add_file($file: File!) {add_file_to_column () {id}}", "add_file_to_column", parameter_dictionary)

        self.make_file_request(request_body, file_path)
    """

    """
    
    def make_file_request(self, body, filePath):

        //TODO: Fix File Uploads
        Helper function for the module.\n
        Uploads a file.

        fileToUpload = open(filePath, "rb")
        
        fileName = os.path.basename(filePath)
        m = MultipartEncoder(fields={
                "query": str(body),
                "map":'{"file":"variables.file"}',
                "files":[('file', (fileName, fileToUpload, "Mime-type"))]
            })
        request = requests.post("https://api.monday.com/v2/file", headers={
            'Authorization':self.secret,
            'Content-Type':m.content_type
        }, data={
            m
        })

        return request.json()
    """