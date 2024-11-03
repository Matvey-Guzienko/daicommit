import time

from enum import Enum
from typing import Any, Dict, List

from .config import get_config, DefaultTokenLimits
from .mergeDiffs import merge_diffs
from .tokenCount import token_count
from .prompts import get_main_commit_prompt
from .engine import get_engine

global_config = get_config()


class GenerateCommitMessageErrorEnum(Enum):
    TOO_MUCH_TOKENS = "TOO_MUCH_TOKENS"
    INTERNAL_ERROR = "INTERNAL_ERROR"
    EMPTY_MESSAGE = "EMPTY_MESSAGE"

    @property
    def output_tokens_too_high(self):
        return f"Token limit exceeded, TOKENS_MAX_OUTPUT must not be much higher than the default {DefaultTokenLimits.DEFAULT_MAX_TOKENS_OUTPUT} tokens."


def generate_commit_message_chat_completion_prompt(
    diff: str, full_git_moji_spec: bool
) -> List[Dict[str, Any]]:
    init_messages_prompt = get_main_commit_prompt(full_git_moji_spec)

    init_messages_prompt.append({"role": "user", "content": diff})

    return init_messages_prompt


def get_commit_msgs_promises_from_file_diffs(
    diff: str, max_diff_length: int, full_git_moji_spec: bool
):
    separator = "diff --git "

    diff_by_files = diff.split(separator)[1:]

    merged_files_diffs = merge_diffs(diff_by_files, max_diff_length)

    commit_message_promises = []

    for file_diff in merged_files_diffs:
        if token_count(file_diff) >= max_diff_length:
            messages_promises = get_messages_promises_by_changes_in_file(
                file_diff, separator, max_diff_length, full_git_moji_spec
            )

            commit_message_promises.extend(messages_promises)
        else:
            messages = generate_commit_message_chat_completion_prompt(
                separator + file_diff, full_git_moji_spec
            )

            engine = get_engine()
            commit_message_promises.append((engine.generate_commit_message, messages))

    return commit_message_promises


ADJUSTMENT_FACTOR = 20


def generate_commit_message_by_diff(diff: str, full_git_moji_spec: bool = False):
    init_messages_prompt = get_main_commit_prompt(full_git_moji_spec)

    init_messages_prompt_length = sum(
        token_count(msg["content"]) + 4 for msg in init_messages_prompt
    )

    max_request_tokens = (
        global_config["TOKENS_MAX_INPUT"]
        - ADJUSTMENT_FACTOR
        - init_messages_prompt_length
        - global_config["MAX_TOKENS_OUTPUT"]
    )

    if token_count(diff) >= max_request_tokens:
        commit_message_promises = get_commit_msgs_promises_from_file_diffs(
            diff, max_request_tokens, full_git_moji_spec
        )

        commit_messages = []

        for promise in commit_message_promises:
            commit_messages.append(promise[0](promise[1]))
            time.sleep(2)

        return "\n".join(commit_messages)

    messages = generate_commit_message_chat_completion_prompt(diff, full_git_moji_spec)

    engine = get_engine()
    commit_message = engine.generate_commit_message(messages)

    if not commit_message:
        raise Exception(GenerateCommitMessageErrorEnum.EMPTY_MESSAGE)

    return commit_message


def get_messages_promises_by_changes_in_file(
    file_diff: str, separator: str, max_change_length: int, full_git_moji_spec: bool
) -> list:
    hunk_header_separator = "@@ "
    file_header, *file_diff_by_lines = file_diff.split(hunk_header_separator)

    merged_changes = merge_diffs(
        [hunk_header_separator + line for line in file_diff_by_lines], max_change_length
    )

    line_diffs_with_header = []

    for change in merged_changes:
        total_change = file_header + change
        if token_count(total_change) > max_change_length:
            # Если total_change слишком велик, разбиваем на меньшие куски
            split_changes = split_diff(total_change, max_change_length)
            line_diffs_with_header.extend(split_changes)
        else:
            line_diffs_with_header.append(total_change)

    engine = get_engine()
    commit_msgs_from_file_line_diffs = [
        generate_commit_message_chat_completion_prompt(
            separator + line_diff, full_git_moji_spec
        )
        for line_diff in line_diffs_with_header
    ]

    # Генерируем сообщения коммитов
    return [
        (engine.generate_commit_message, messages)
        for messages in commit_msgs_from_file_line_diffs
    ]


def split_diff(diff: str, max_change_length: int):
    lines = diff.split("\n")
    split_diffs = []
    current_diff = ""

    if max_change_length <= 0:
        raise ValueError(GenerateCommitMessageErrorEnum.output_tokens_too_high)

    for line in lines:
        while token_count(line) > max_change_length:
            sub_line = line[:max_change_length]
            line = line[max_change_length:]
            split_diffs.append(sub_line)

        if token_count(current_diff) + token_count("\n" + line) > max_change_length:
            split_diffs.append(current_diff)
            current_diff = line
        else:
            current_diff += "\n" + line if current_diff else line

    if current_diff:
        split_diffs.append(current_diff)

    return split_diffs
