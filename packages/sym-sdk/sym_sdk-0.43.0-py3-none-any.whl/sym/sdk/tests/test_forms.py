from collections import OrderedDict

import pytest

from sym.sdk.forms import FieldOption, FieldType, PromptField, SlackUserSelection, SymPromptForm


class TestForms:
    def test_sym_prompt_form_construction_succeeds(self):
        slack_user1 = SlackUserSelection(user_id="U12345", username="test@symops.io")
        slack_user2 = SlackUserSelection(user_id="U67890", username="user@symops.io")

        fields = OrderedDict(
            {
                "reason": PromptField(
                    name="reason",
                    type=FieldType.STRING,
                    value="For testing things",
                ),
                "urgency": PromptField(
                    name="urgency",
                    label="Urgency",
                    type=FieldType.STRING,
                    required=False,
                    current_allowed_values=[
                        FieldOption(value="low", label="Low"),
                        FieldOption(value="high", label="High"),
                    ],
                    original_allowed_values=[
                        FieldOption(value="low", label="Low"),
                        FieldOption(value="medium", label="Medium"),
                        FieldOption(value="high", label="High"),
                    ],
                ),
                "user": PromptField(
                    name="some-user",
                    label="User",
                    type=FieldType.SLACK_USER,
                    current_allowed_values=[FieldOption(value=slack_user1, label="Test User")],
                    original_allowed_values=[
                        FieldOption(value=slack_user1, label="Test User"),
                        FieldOption(value=slack_user2, label="Other User"),
                    ],
                ),
            }
        )

        form = SymPromptForm(fields=fields)
        assert form

    def test_prompt_field_immutable_values_cannot_be_changed(self):
        field = PromptField(
            name="urgency",
            type=FieldType.STRING,
            current_allowed_values=[
                FieldOption(value="low", label="Low"),
            ],
            original_allowed_values=[
                FieldOption(value="low", label="Low"),
                FieldOption(value="medium", label="Medium"),
                FieldOption(value="high", label="High"),
            ],
        )

        with pytest.raises(TypeError, match="cannot be assigned"):
            field.name = "nope"

        with pytest.raises(TypeError, match="cannot be assigned"):
            field.type = FieldType.BOOL

        with pytest.raises(TypeError, match="cannot be assigned"):
            field.original_allowed_values = []

    def test_slack_user_selection_immutable_values_cannot_be_changed(self):
        user = SlackUserSelection(user_id="U12345", username="user@symops.io")

        with pytest.raises(TypeError, match="cannot be assigned"):
            user.user_id = "nope"

        with pytest.raises(TypeError, match="cannot be assigned"):
            user.username = "nope"
