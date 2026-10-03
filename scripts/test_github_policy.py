"""Safety checks for issue/branch/dependency merge policy."""
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

    @patch.object(policy, 'readiness', return_value=issue())
    def test_missing_or_foreign_issue_reference_denied(self, readiness):
        for body in ['No issue', 'Closes https://github.com/another/repo/issues/48']:
            with self.assertRaisesRegex(ValueError, 'close exactly one'):
                policy.check_pr({'body': body})

    @patch.object(policy, 'readiness', return_value=issue())
    def test_wrong_branch_denied(self, readiness):
        with self.assertRaisesRegex(ValueError, 'issue branch'):
            policy.check_pr({'body': 'Closes #48', 'head': {'ref': 'feature/demo'}, 'base': {'ref': 'main'}})

    @patch.object(policy, 'readiness', return_value=issue())
    def test_valid_pr_is_accepted(self, readiness):
        result = policy.check_pr({'body': 'Closes #48', 'head': {'ref': '48-define-the-demo-blueprint'}, 'base': {'ref': 'main'}})
        self.assertIn('valid', result)

    @patch.object(policy, 'api_pages')
    @patch.object(policy, 'api')
    def test_completed_prerequisite_allows_issue(self, api, pages):
        api.return_value = issue()
        pages.return_value = [issue(2, state='closed', reason='completed')]
        self.assertEqual(policy.readiness(48)['number'], 48)


if __name__ == '__main__':
    unittest.main()
