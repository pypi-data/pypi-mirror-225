import unittest
from monday_lib.monday_api_library import monday_endpoints

monday = monday_endpoints(api_secret="API SECRET", wait_for_complexity=True, logging_file="test.log")

boards = monday.get_all_boards()
for board in boards:
    if board['type'] == 'board':
        board_id = board['id']
        break

monday_users = monday.get_all_users()
for monday_user in monday_users:
    monday_user_id = monday_user['id']
    break

test_descructive_tests = False
delete_board_id = 123

class TestMonday(unittest.TestCase):
    def test_case_get_all_boards(self, id=None):
        if id:
            self.boards = monday.get_all_boards(workspace_id=id)
        else:
            self.boards = monday.get_all_boards()
        self.assertEqual(type(self.boards), list, "Should be a list")
        for board in self.boards:
            board_keys = board.keys()
            self.assertEqual(list(board_keys), ["id","name","state","board_folder_id","workspace_id","creator","type"],"Should be correct keys")
            for key, value in board.items():
                if key == "id":
                    self.assertEqual(type(value), str, "Id should be str")
                elif key == "name":
                    self.assertEqual(type(value), str, "Name should be str")
                elif key == "state":
                    self.assertEqual(type(value), str, "State should be str")
                elif key == "board_folder_id":
                    self.check_if_type_is_correct(value, (int, type(None)))
                elif key == "workspace_id":
                    self.check_if_type_is_correct(value, (int, type(None)))
                elif key == "creator":
                    self.assertEqual(isinstance(value, (dict)), True, "Creator should be dict")
                    for creator_key, creator_value in value.items():
                        if creator_key == "id":
                            self.assertEqual(isinstance(creator_value, (int)), True, "Creator id should be int")
                elif key == "type":
                    self.assertEqual(isinstance(value, (str)), True, "Type should be str")
                else:
                    raise Exception(key + " is not caught in test!")
                
    def test_account_metadata(self):
        self.account_metadata = monday.get_account_metadata()
        #self.assertEqual(self.account_metadata, {'account': {'id': 18271227, 'logo': None, 'show_timeline_weekends': True, 'first_day_of_the_week': 'monday', 'sign_up_product_kind': None, 'plan': None, 'tier': None, 'slug': 'hobbits-group'}}, "Account metadata, should match expected output")
        for key, value in self.account_metadata.items():
            if key == 'account':
                self.assertEqual(type(value), dict, "Account should be dict")
                for account_key, account_value in value.items():
                    if account_key == "id":
                        self.assertEqual(type(account_value), int, "Account_id should be int")
                    elif account_key == "logo":
                        self.assertEqual(isinstance(account_value, (str, type(None))), True, "Logo should be str or None")
                    elif account_key == "show_timeline_weekends":
                        self.assertEqual(type(account_value), bool, "show_timeline_weekends should be bool")
                    elif account_key == "first_day_of_the_week":
                        self.assertEqual(type(account_value), str, "first_day_of_the_week should be str")
                    elif account_key == "sign_up_product_kind":
                        self.assertEqual(isinstance(account_value, (str, type(None))), True, "sign_up_product_kind should be str or None")
                    elif account_key == "plan":
                        self.assertEqual(isinstance(account_value, (dict, type(None))), True, "plan should be dict or None")
                    elif account_key == "tier":
                        self.assertEqual(isinstance(account_value, (str, type(None))), True, "tier should be str or None")
                    elif account_key == "slug":
                        self.assertEqual(isinstance(account_value, (str)), True, "slug should be str or None")
                    else:
                        raise Exception(account_key + " is not caught in test!")
            else:
                raise Exception(key + " is not caught in test!")
    def test_get_all_users(self):
        self.get_all_users = monday.get_all_users()
        self.assertEqual(type(self.get_all_users), list, "All Users should be in a list")
        for user in self.get_all_users:
            self.assertEqual(list(user.keys()), ['id', 'birthday', 'country_code', 'created_at', 'join_date', 'email', 'enabled', 'is_admin', 'is_guest', 'is_pending', 'is_view_only', 'location', 'mobile_phone', 'name', 'phone', 'photo_original', 'photo_small', 'photo_thumb', 'photo_thumb_small', 'photo_tiny', 'time_zone_identifier', 'title', 'url', 'utc_hours_diff'], "Output should match expected output")
            for key, value in user.items():
                if key == "id":
                    self.check_if_type_is_correct(value, int)
                elif key == "birthday":
                    self.check_if_type_is_correct(value, (str, type(None)))
                elif key == "country_code":
                    self.check_if_type_is_correct(value, str)
                elif key == "created_at":
                    self.check_if_type_is_correct(value, str)
                elif key == "join_date":
                    self.check_if_type_is_correct(value, (str, type(None)))
                elif key == "email":
                    self.check_if_type_is_correct(value, str)
                elif key == "enabled":
                    self.check_if_type_is_correct(value, bool)
                elif key == "enabled":
                    self.check_if_type_is_correct(value, bool)
                elif key == "is_admin":
                    self.check_if_type_is_correct(value, bool)
                elif key == "is_guest":
                    self.check_if_type_is_correct(value, bool)
                elif key == "is_pending":
                    self.check_if_type_is_correct(value, bool)
                elif key == "is_view_only":
                    self.check_if_type_is_correct(value, bool)
                elif key == "location":
                    self.check_if_type_is_correct(value, (str, type(None)))
                elif key == "mobile_phone":
                    self.check_if_type_is_correct(value, (str, type(None)))
                elif key == "name":
                    self.check_if_type_is_correct(value, str)
                elif key == "phone":
                    self.check_if_type_is_correct(value, (str, type(None)))
                elif key == "photo_original":
                    self.check_if_type_is_correct(value, str)
                elif key == "photo_small":
                    self.check_if_type_is_correct(value, str)
                elif key == "photo_thumb":
                    self.check_if_type_is_correct(value, str)
                elif key == "photo_thumb_small":
                    self.check_if_type_is_correct(value, str)
                elif key == "photo_tiny":
                    self.check_if_type_is_correct(value, str)
                elif key == "time_zone_identifier":
                    self.check_if_type_is_correct(value, str)
                elif key == "title":
                    self.check_if_type_is_correct(value, (str, type(None)))
                elif key == "url":
                    self.check_if_type_is_correct(value, str)
                elif key == "utc_hours_diff":
                    self.check_if_type_is_correct(value, int)
                else:
                    raise Exception(key + " is not caught in test!")

    def test_get_all_workspaces(self):
        self.all_workspaces = monday.get_all_workspaces()
        self.check_if_type_is_correct(self.all_workspaces, list)
        for workspace in self.all_workspaces:
            self.check_if_type_is_correct(workspace, dict)
            self.assertEqual(list(workspace.keys()), ['id', 'name', 'kind', 'description', 'created_at'], "Output should match expected output")
            for workspace_key, workspace_value in workspace.items():
                if workspace_key == "id":
                    self.check_if_type_is_correct(workspace_value, int)
                elif workspace_key == "name":
                    self.check_if_type_is_correct(workspace_value, str)
                elif workspace_key == "kind":
                    self.check_if_type_is_correct(workspace_value, str)
                elif workspace_key == "description":
                    self.check_if_type_is_correct(workspace_value, (str, type(None)))
                elif workspace_key == "created_at":
                    self.check_if_type_is_correct(workspace_value, str)
                else:
                    raise Exception(workspace_key + " is not caught in test!")
    
    def test_get_board_activity(self):
        self.board_activity = monday.get_board_activity(board_id=board_id, activity_to="2023-12-31")
        self.check_if_type_is_correct(self.board_activity, list)
        for board_activity in self.board_activity:
            self.check_if_type_is_correct(board_activity, dict)
            for key, value in board_activity.items():
                if key == "id":
                    self.check_if_type_is_correct(value, str)
                elif key == "account_id":
                    self.check_if_type_is_correct(value, str)
                elif key == "data":
                    self.check_if_type_is_correct(value, str)
                elif key == "entity":
                    self.check_if_type_is_correct(value, str)
                    self.assertEqual(value in ["pulse", "board"], True, "Should be either pulse or board")
                elif key == "event":
                    self.check_if_type_is_correct(value, str)
                elif key == "user_id":
                    self.check_if_type_is_correct(value, str)
                elif key == "created_at":
                    self.check_if_type_is_correct(value, str)
                else:
                    raise Exception(key + " is not caught in test!")
    
    def test_get_board_columns(self):
        self.board_columns = monday.get_board_columns(board_id)
        self.check_if_type_is_correct(self.board_columns, list)
        for board_column in self.board_columns:
            self.check_if_type_is_correct(board_column, dict)
            for key, value in board_column.items():
                if key == "id":
                    self.check_if_type_is_correct(value, str)
                elif key == "archived":
                    self.check_if_type_is_correct(value, bool)
                elif key == "description":
                    self.check_if_type_is_correct(value, (str, type(None)))
                elif key == "settings_str":
                    self.check_if_type_is_correct(value, str)
                elif key == "title":
                    self.check_if_type_is_correct(value, str)
                elif key == "type":
                    self.check_if_type_is_correct(value, str)
                elif key == "width":
                    self.check_if_type_is_correct(value, (int, type(None)))
                else:
                    raise Exception(key + " is not caught in test!")
    
    def test_get_board_groups(self):
        self.board_groups = monday.get_board_groups(board_id)
        self.check_if_type_is_correct(self.board_groups, list)
        for board in self.board_groups:
            self.check_if_type_is_correct(board, dict)
            for key, value in board.items():
                if key == "archived":
                    self.check_if_type_is_correct(value, (bool, type(None)))
                elif key == "color":
                    self.check_if_type_is_correct(value, str)
                elif key == "deleted":
                    self.check_if_type_is_correct(value, (bool, type(None)))
                elif key == "id":
                    self.check_if_type_is_correct(value, str)
                elif key == "position":
                    self.check_if_type_is_correct(value, str)
                elif key == "title":
                    self.check_if_type_is_correct(value, str)
                else:
                    raise Exception(key + " is not caught in test!")
    
    def test_get_board_items(self):
        self.board_items = monday.get_board_items(board_id)
        self.check_if_type_is_correct(self.board_items, list)
        self.check_if_type_is_correct(self.board_items[0], dict)
        self.check_if_type_is_correct(self.board_items[0]['items'], list)
        for item in self.board_items[0]['items']:
            self.check_if_type_is_correct(item, dict)
            for key, value in item.items():
                if key == "id":
                    self.check_if_type_is_correct(value, str)
                elif key == "name":
                    self.check_if_type_is_correct(value, str)
                elif key == "creator_id":
                    self.check_if_type_is_correct(value, str)
                elif key == "state":
                    self.check_if_type_is_correct(value, str)
                    self.assertEqual(value in ["all","active","archived","deleted"], True, "Output should be in expected list")
                elif key == "updated_at":
                    self.check_if_type_is_correct(value, str)
                elif key == "column_values":
                    self.check_if_type_is_correct(value, list)
                    for column_values in value:
                        self.check_if_type_is_correct(column_values, dict)
                        for column_value_key, column_value_value in column_values.items():
                            if column_value_key == "id":
                                self.check_if_type_is_correct(column_value_value, str)
                            elif column_value_key == "title":
                                self.check_if_type_is_correct(column_value_value, str)
                            elif column_value_key == "value":
                                self.check_if_type_is_correct(column_value_value, (type(None),str))
                            elif column_value_key == "text":
                                self.check_if_type_is_correct(column_value_value, (type(None),str))
                            else:
                                raise Exception(column_value_key + " is not caught in test!")
                elif key == "group":
                    self.check_if_type_is_correct(value, dict)
                    for group_key, group_value in value.items():
                        if group_key == "id":
                            self.check_if_type_is_correct(group_value, str)
                        elif group_key == "title":
                            self.check_if_type_is_correct(group_value, str)
                        else:
                            raise Exception(group_key + " is not caught in test!")
                else:
                    raise Exception(key + " is not caught in test!")
    
    def test_get_board_views(self):
        self.board_views = monday.get_board_views(board_id)
        self.check_if_type_is_correct(self.board_views, list)
    
    def test_get_board_webhooks(self):
        self.board_webhooks = monday.get_board_webhooks(board_id)
        self.check_if_type_is_correct(self.board_webhooks, list)
        for webhook in self.board_webhooks:
            self.check_if_type_is_correct(webhook, dict)
            for key, value in webhook.items():
                if key == "id":
                    self.check_if_type_is_correct(value, str)
                elif key == "event":
                    webhook_events = [
                        "change_column_value",
                        "change_status_column_value",
                        "change_subitem_column_value",
                        "change_specific_column_value",
                        "change_name",
                        "create_item",
                        "item_archived",
                        "item_deleted",
                        "item_moved_to_any_group",
                        "item_moved_to_specific_group",
                        "item_restored",
                        "create_subitem",
                        "change_subitem_name",
                        "move_subitem",
                        "subitem_archived",
                        "subitem_deleted",
                        "create_column",
                        "create_update",
                        "edit_update",
                        "delete_update",
                        "create_subitem_update",
                        "incoming_notification",
                        "when_date_arrived"
                    ]
                    self.check_if_type_is_correct(value, str)
                    self.assertEqual(value in webhook_events, True, "Should be in webhook events.")
                elif key == "board_id":
                    self.check_if_type_is_correct(value, int)
                elif key == "config":
                    self.check_if_type_is_correct(value, str)
                else:
                    raise Exception(key + " is not caught in test!")
    
    def test_add_subscribers_to_board(self):
        self.add_subscribers = monday.add_users_to_board(board_id, [monday_user_id], "subscriber")
        self.check_if_type_is_correct(self.add_subscribers, dict)
        for top_key, top_value in self.add_subscribers["data"].items():
            if top_key == "complexity":
                self.check_if_type_is_correct(top_value, dict)
                for complexity_key, complexity_value in top_value.items():
                    if complexity_key == "after":
                        self.check_if_type_is_correct(complexity_value, int)
                    elif complexity_key == "reset_in_x_seconds":
                        self.check_if_type_is_correct(complexity_value, int)
                    else:
                        raise Exception(complexity_key + " is not caught in test!")
            elif top_key == "add_users_to_board":
                self.check_if_type_is_correct(top_value, list)
                for add_user_in_value in top_value:
                    for add_users_to_board_key, add_users_to_board_value in add_user_in_value.items():
                        if add_users_to_board_key == "id":
                            self.check_if_type_is_correct(add_users_to_board_value, int)
                        else:
                            raise Exception(add_users_to_board_key + " is not caught in test!")
            else:
                raise Exception(top_key + " is not caught in test!")
    
    def test_create_board(self):
        if not test_descructive_tests:
            return
        self.add_board = monday.create_board("Test Board Name", "public", board_folder_id=None, workspace_id=271687, board_owner_ids=[47200716])
        self.check_if_type_is_correct(self.add_board, dict)
        for top_key, top_value in self.add_board["data"].items():
            if top_key == "complexity":
                self.check_if_type_is_correct(top_value, dict)
                for complexity_key, complexity_value in top_value.items():
                    if complexity_key == "after":
                        self.check_if_type_is_correct(complexity_value, int)
                    elif complexity_key == "reset_in_x_seconds":
                        self.check_if_type_is_correct(complexity_value, int)
                    else:
                        raise Exception(complexity_key + " is not caught in test!") 
            elif top_key == "create_board":
                self.check_if_type_is_correct(top_value, dict)
                for create_board_key, create_board_value_value in top_value.items():
                    if create_board_key == "id":
                        self.check_if_type_is_correct(create_board_value_value, str)
                    else:
                        raise Exception(create_board_key + " is not caught in test!")
            else:
                raise Exception(top_key + " is not caught in test!")

    def test_archive_board(self):
        if not test_descructive_tests:
            return
        self.archive_board = monday.archive_board(1249058418)
        self.check_if_type_is_correct(self.archive_board, dict)
        for top_key, top_value in self.archive_board["data"].items():
            if top_key == "complexity":
                self.check_if_type_is_correct(top_value, dict)
                for complexity_key, complexity_value in top_value.items():
                    if complexity_key == "after":
                        self.check_if_type_is_correct(complexity_value, int)
                    elif complexity_key == "reset_in_x_seconds":
                        self.check_if_type_is_correct(complexity_value, int)
                    else:
                        raise Exception(complexity_key + " is not caught in test!") 
            elif top_key == "archive_board":
                self.check_if_type_is_correct(top_value, dict)
                for archive_board_key, archive_board_value_value in top_value.items():
                    if archive_board_key == "id":
                        self.check_if_type_is_correct(archive_board_value_value, str)
                    else:
                        raise Exception(archive_board_key + " is not caught in test!")
            else:
                raise Exception(top_key + " is not caught in test!")
    
    def test_duplicate_board(self):
        if not test_descructive_tests:
            return
        self.duplicate_board = monday.duplicate_board(1249058674, "duplicate_board_with_structure", "Test Duplicated", 271687, folder_id=None, keep_subscribers=None)
        self.check_if_type_is_correct(self.duplicate_board, dict)
        for top_key, top_value in self.duplicate_board["data"].items():
            if top_key == "complexity":
                self.check_if_type_is_correct(top_value, dict)
                for complexity_key, complexity_value in top_value.items():
                    if complexity_key == "after":
                        self.check_if_type_is_correct(complexity_value, int)
                    elif complexity_key == "reset_in_x_seconds":
                        self.check_if_type_is_correct(complexity_value, int)
                    else:
                        raise Exception(complexity_key + " is not caught in test!") 
            elif top_key == "duplicate_board":
                self.check_if_type_is_correct(top_value, dict)
                for duplicate_board_key, duplicate_board_value_value in top_value.items():
                    if duplicate_board_key == "board":
                        self.check_if_type_is_correct(duplicate_board_value_value, dict)
                        for key, value in duplicate_board_value_value.items():
                            if key == "id":
                                self.check_if_type_is_correct(value, str)
                            else:
                                raise Exception(key + " is not caught in test!")
                    else:
                        raise Exception(duplicate_board_key + " is not caught in test!")
            else:
                raise Exception(top_key + " is not caught in test!")

    def test_update_board(self):
        self.update_board = monday.update_board(board_id, "description", "Test Value Description")
        self.check_if_type_is_correct(self.update_board, dict)
        for top_key, top_value in self.update_board["data"].items():
            if top_key == "complexity":
                self.check_if_type_is_correct(top_value, dict)
                for complexity_key, complexity_value in top_value.items():
                    if complexity_key == "after":
                        self.check_if_type_is_correct(complexity_value, int)
                    elif complexity_key == "reset_in_x_seconds":
                        self.check_if_type_is_correct(complexity_value, int)
                    else:
                        raise Exception(complexity_key + " is not caught in test!") 
            elif top_key == "update_board":
                self.check_if_type_is_correct(top_value, str)
            else:
                raise Exception(top_key + " is not caught in test!")

    def test_delete_board(self):
        if not test_descructive_tests:
            return
        self.delete_board = monday.delete_board(delete_board_id)
        self.check_if_type_is_correct(self.delete_board, dict)
        for top_key, top_value in self.delete_board["data"].items():
            if top_key == "complexity":
                self.check_if_type_is_correct(top_value, dict)
                for complexity_key, complexity_value in top_value.items():
                    if complexity_key == "after":
                        self.check_if_type_is_correct(complexity_value, int)
                    elif complexity_key == "reset_in_x_seconds":
                        self.check_if_type_is_correct(complexity_value, int)
                    else:
                        raise Exception(complexity_key + " is not caught in test!") 
            elif top_key == "delete_board":
                self.check_if_type_is_correct(top_value, dict)
                for delete_board_key, delete_board_value_value in top_value.items():
                    if delete_board_key == "id":
                        self.check_if_type_is_correct(delete_board_value_value, str)
                    else:
                        raise Exception(delete_board_key + " is not caught in test!")
            else:
                raise Exception(top_key + " is not caught in test!")
    
    def test_create_board_column(self):
        if not test_descructive_tests:
            return
        self.create_board_column = monday.create_board_column(board_id, "Test Column", "Test", "text")
        self.check_if_type_is_correct(self.create_board_column, dict)
        for top_key, top_value in self.create_board_column["data"].items():
            if top_key == "complexity":
                self.check_if_type_is_correct(top_value, dict)
                for complexity_key, complexity_value in top_value.items():
                    if complexity_key == "after":
                        self.check_if_type_is_correct(complexity_value, int)
                    elif complexity_key == "reset_in_x_seconds":
                        self.check_if_type_is_correct(complexity_value, int)
                    else:
                        raise Exception(complexity_key + " is not caught in test!") 
            elif top_key == "create_column":
                self.check_if_type_is_correct(top_value, dict)
                for create_column_key, create_column_value_value in top_value.items():
                    if create_column_key == "id":
                        self.check_if_type_is_correct(create_column_value_value, str)
                    elif create_column_key == "title":
                        self.check_if_type_is_correct(create_column_value_value, str)
                    elif create_column_key == "description":
                        self.check_if_type_is_correct(create_column_value_value, str)
                    elif create_column_key == "type":
                        self.check_if_type_is_correct(create_column_value_value, str)
                    else:
                        raise Exception(create_column_key + " is not caught in test!")
            else:
                raise Exception(top_key + " is not caught in test!")
    
    def test_change_simple_column_value(self):
        if not test_descructive_tests:
            return
        self.change_simple_column_value = monday.change_simple_column_value(board_id, 1249059963, "test_column5", "Test")
        self.check_if_type_is_correct(self.change_simple_column_value, dict)
        for top_key, top_value in self.change_simple_column_value["data"].items():
            if top_key == "complexity":
                self.check_if_type_is_correct(top_value, dict)
                for complexity_key, complexity_value in top_value.items():
                    if complexity_key == "after":
                        self.check_if_type_is_correct(complexity_value, int)
                    elif complexity_key == "reset_in_x_seconds":
                        self.check_if_type_is_correct(complexity_value, int)
                    else:
                        raise Exception(complexity_key + " is not caught in test!") 
            elif top_key == "change_simple_column_value":
                self.check_if_type_is_correct(top_value, dict)
                for change_simple_column_value_key, change_simple_column_value_value_value in top_value.items():
                    if change_simple_column_value_key == "id":
                        self.check_if_type_is_correct(change_simple_column_value_value_value, str)
                    else:
                        raise Exception(change_simple_column_value_key + " is not caught in test!")
            else:
                raise Exception(top_key + " is not caught in test!")
    
    def test_get_item(self):
        self.get_item = monday.get_item(1249059963)
        self.check_if_type_is_correct(self.get_item, list)
        for item in self.get_item:
            for key, value in item.items():
                if key == "id":
                    self.check_if_type_is_correct(value, str)
                elif key == "name":
                    self.check_if_type_is_correct(value, str)
                elif key == "creator_id":
                    self.check_if_type_is_correct(value, str)
                elif key == "state":
                    self.check_if_type_is_correct(value, str)
                    self.assertEqual(value in ["all","active","archived","deleted"], True, "Should match exptected output")
                elif key == "updated_at":
                    self.check_if_type_is_correct(value, (str, type(None)))
                elif key == "column_values":
                    self.check_if_type_is_correct(value, list)
                    for column in value:
                        for column_key, column_value in column.items():
                            if column_key == "id":
                                self.check_if_type_is_correct(column_value, str)
                            elif column_key == "title":
                                self.check_if_type_is_correct(column_value, str)
                            elif column_key == "value":
                                self.check_if_type_is_correct(column_value, (str,type(None)))
                            else:
                                raise Exception(column_key + " is not caught in test!")
                elif key == "group":
                    self.check_if_type_is_correct(value, dict)
                    for group_key, group_value in value.items():
                        if group_key == "id":
                            self.check_if_type_is_correct(column_value, str)
                        elif group_key == "title":
                            self.check_if_type_is_correct(column_value, str)
                        else:
                            raise Exception(group_key + " is not caught in test!")
    def check_if_type_is_correct(self, value, expected):
        if type(expected) == tuple:
            self.assertEqual(isinstance(value, expected), True, f"{value} should be either {expected} and is {type(value)}")
        else:
            self.assertEqual(type(value), expected, f"{value} should be {expected} and is {type(value)}")

unittest.main()