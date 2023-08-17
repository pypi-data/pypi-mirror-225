import json
import unittest

from switcore.ui.element_components import OpenLink
from switcore.ui.select import Select, Option


class SelectTest(unittest.TestCase):

    def test_valid_select01(self):
        select = Select(
            trigger_on_input=True,
            options=[
                Option(
                    label="test label1",
                    action_id="action_id1"
                ),
                Option(
                    label="test label2",
                    action_id="action_id2"
                ),
            ]
        )
        expected = {
            'type': 'select',
            'multiselect': False,
            'trigger_on_input': True,
            'options': [
                {
                    'label': 'test label1',
                    'action_id': 'action_id1'
                },
                {
                    'label': 'test label2',
                    'action_id': 'action_id2'
                }
            ]
        }
        # print(json.dumps(expected, indent=4))
        self.assertEqual(expected, select.dict(exclude_none=True))

    def test_valid_select02(self):
        select = Select(
            trigger_on_input=True,
            options=[
                Option(
                    label="test label1",
                    action_id="action_id1",
                    static_action=OpenLink(
                        link_url="https://www.google.com"
                    )
                ),
                Option(
                    label="test label2",
                    action_id="action_id2"
                ),
            ]
        )
        expected = {'multiselect': False,
                    'options': [{'action_id': 'action_id1',
                                 'label': 'test label1',
                                 'static_action': {'link_url': 'https://www.google.com',
                                                   'action_type': 'open_link'}},
                                {'action_id': 'action_id2', 'label': 'test label2'}],
                    'trigger_on_input': True,
                    'type': 'select'}
        print(json.dumps(expected, indent=4))
        self.assertEqual(expected, select.dict(exclude_none=True))
