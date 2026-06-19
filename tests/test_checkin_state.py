import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from checkin import format_check_in_notification, generate_balance_hash


def test_balance_hash_changes_when_quota_changes():
	before = {'account_1': {'quota': 100.0, 'used': 20.0}}
	after = {'account_1': {'quota': 125.0, 'used': 20.0}}

	assert generate_balance_hash(before) != generate_balance_hash(after)


def test_balance_hash_changes_when_used_quota_changes():
	before = {'account_1': {'quota': 100.0, 'used': 20.0}}
	after = {'account_1': {'quota': 100.0, 'used': 21.0}}

	assert generate_balance_hash(before) != generate_balance_hash(after)


def test_balance_hash_is_stable_for_equivalent_balances():
	left = {
		'account_2': {'quota': 50.0, 'used': 1.0},
		'account_1': {'quota': 100.0, 'used': 20.0},
	}
	right = {
		'account_1': {'used': 20.0, 'quota': 100.0},
		'account_2': {'used': 1.0, 'quota': 50.0},
	}

	assert generate_balance_hash(left) == generate_balance_hash(right)


def test_check_in_notification_keeps_emoji_for_unchanged_balance():
	message = format_check_in_notification(
		{
			'name': 'Account 1',
			'before_quota': 2238.92,
			'before_used': 936.08,
			'after_quota': 2238.92,
			'after_used': 936.08,
			'check_in_reward': 0,
			'usage_increase': 0,
			'balance_change': 0,
		}
	)

	assert '📍 签到前' in message
	assert '💵 余额: $2238.92' in message
	assert '📊 累计消耗: $936.08' in message
	assert 'ℹ️  今日已签到，无变化' in message


def test_check_in_notification_keeps_emoji_for_balance_changes():
	message = format_check_in_notification(
		{
			'name': 'Account 1',
			'before_quota': 100,
			'before_used': 20,
			'after_quota': 125,
			'after_used': 21,
			'check_in_reward': 26,
			'usage_increase': 1,
			'balance_change': 25,
		}
	)

	assert '🎁 签到获得: +$26.00' in message
	assert '📉 期间消耗: $1.00' in message
	assert '📈 余额变化: +$25.00' in message
