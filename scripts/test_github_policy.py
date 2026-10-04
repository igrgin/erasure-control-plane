"""Checks for the local issue-readiness and branch helpers."""
import unittest
from unittest.mock import patch
import github_policy as policy


def issue(number=48, state='open', reason=None, label='implement'):
    return {'id': 100 + number, 'number': number, 'title': '[ERA-037] Define the demo blueprint',
            'state': state, 'state_reason': reason, 'labels': [{'name': label}]}


class PolicyTests(unittest.TestCase):
    def test_branch_has_number_and_flat_kebab_title(self):
        self.assertEqual(policy.branch_name(48, '[ERA-037] Define The Demo Blueprint'), '48-define-the-demo-blueprint')

    def test_discarded_issue_is_not_accepted(self):
        self.assertFalse(policy.completed(issue(state='closed', reason='not_planned')))
        self.assertTrue(policy.completed(issue(state='closed', reason='completed')))

    @patch.object(policy, 'api_pages')
    @patch.object(policy, 'api')
    def test_open_native_blocker_denies_readiness(self, api, pages):
        api.return_value = issue()
        pages.return_value = [issue(2)]
        with self.assertRaisesRegex(ValueError, 'prerequisites'):
            policy.readiness(48)

    @patch.object(policy, 'api_pages')
    @patch.object(policy, 'api')
    def test_epic_integration_waits_for_children(self, api, pages):
        api.return_value = issue(label='epic')
        pages.side_effect = [[], [issue(2)]]
        with self.assertRaisesRegex(ValueError, 'integration awaits'):
            policy.readiness(48)

    @patch.object(policy, 'api_pages')
    @patch.object(policy, 'api')
    def test_multiple_type_labels_denied(self, api, pages):
        actual = issue()
        actual['labels'].append({'name': 'spike'})
        api.return_value = actual
        with self.assertRaisesRegex(ValueError, 'exactly one'):
            policy.readiness(48)

    @patch.object(policy, 'api_pages')
    @patch.object(policy, 'api')
    def test_completed_prerequisite_allows_issue(self, api, pages):
        api.return_value = issue()
        pages.return_value = [issue(2, state='closed', reason='completed')]
        self.assertEqual(policy.readiness(48)['number'], 48)


if __name__ == '__main__':
    unittest.main()
