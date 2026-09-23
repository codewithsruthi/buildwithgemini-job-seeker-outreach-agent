# ruff: noqa
# Copyright 2026 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from google.adk.agents import Agent
from google.adk.agents.callback_context import CallbackContext
from google.adk.apps import App
from google.adk.models import Gemini
from google.adk.tools.preload_memory_tool import PreloadMemoryTool
from google.genai import types

from a2ui.basic_catalog.provider import BasicCatalog
from a2ui.schema.manager import A2uiSchemaManager

from .a2ui_utils import a2ui_callback
from .app_utils.job_seeker_tools import (
    analyze_post_for_opportunity,
    evaluate_job_seeker_draft,
    fetch_and_save_new_post,
    fetch_job_seeking_frameworks,
    fetch_saved_posts_from_storage,
    get_candidate_profile,
    mark_post_processed_in_storage,
    save_opportunity_draft,
    save_post_to_storage,
    update_candidate_profile,
)

MODEL = "gemini-3.6-flash"


# WRITE: Memory callback to persist user candidate background and target preferences
async def generate_memories_callback(callback_context: CallbackContext):
    try:
        await callback_context.add_session_to_memory()
    except Exception:
        # Gracefully handle when memory service is not active in local dev runner
        pass
    return None


schema_manager = A2uiSchemaManager(
    version="0.8",
    catalogs=[BasicCatalog.get_config("0.8")],
)

instruction = schema_manager.generate_system_prompt(
    role_description=(
        "You are an expert LinkedIn Job-Seeker Cold Message Assistant. "
        "Your purpose is to help professionals who are actively looking for new opportunities "
        "craft authentic, respectful, and high-converting cold outreach messages to hiring managers, "
        "engineering leaders, founders, and recruiters.\n\n"
        "AUTOMATIC LINK HANDLING:\n"
        "- When the user gives you a LinkedIn post link and says to save it (e.g., 'Save this post to my storage: <URL>'), "
        "call `fetch_and_save_new_post(post_url)` to automatically fetch details and save it to Cloud Storage.\n"
        "- When the user gives you a link and says to draft a message (or save and draft), fetch and save it, and draft the message immediately!\n\n"
        "USER PROFILE & RULES (PERSISTENT):\n"
        "- Current Role: Data Engineer at Meta\n"
        "- Target Roles: Data Engineer, Business Analyst, Data Analyst, Analytics Engineer\n"
        "- Candidate Skills: SQL, Python, Analysis, Experimentation, LLMs, Claude, Agents, Workflows\n"
        "- CRITICAL RULE: NEVER list all skills in a draft. Only select 2-3 skills that directly match the target role/post.\n"
        "- NO PLACEHOLDERS RULE: NEVER output generic placeholder brackets like '[Target Company]' or '[Job Role]'. If the company or role was not fully specified, infer it naturally from the context (e.g. 'your team', 'Data Engineer / Analytics Engineer') or state the exact role directly.\n"
        "- Greeting Rule: ALWAYS start with a warm, natural greeting (e.g. 'Hi [Name], hope you're having a great week!').\n"
        "- Intent Rule: Clearly state that the user is actively looking for new opportunities.\n"
        "- Length Rule: Keep drafts strictly between 45 and 80 words for mobile readability."
    ),
    workflow_description=(
        "1. If a URL is shared, use `fetch_and_save_new_post` or `analyze_post_for_opportunity`.\n"
        "2. If asked to review saved leads, call `fetch_saved_posts_from_storage`.\n"
        "3. Select 2-3 relevant skills matching the target role from the candidate's Meta Data Engineer background.\n"
        "4. Draft a tailored message following greeting -> post recognition -> active search intent -> low-pressure ask.\n"
        "5. Evaluate each draft with `evaluate_job_seeker_draft` and render as structured A2UI cards."
    ),
    ui_description=(
        "Keep every surface tiny and flat: ONE Card > ONE Column > a few Text rows. "
        "Never nest a Card inside a Card. "
        "Use ONLY these components: Card, Column, Row, Text, and Divider. Do not use "
        "Table or Heading (unsupported), or Buttons, actions, or forms (they do "
        "nothing in adk web). "
        "No markdown in text; use the usageHint property ('h1', 'h2', 'body') for "
        "headings and emphasis. "
        "Output ONLY the raw A2UI JSON array — no prose, and never wrap it in "
        "<a2a_datapart_json> tags or 'kind'/'data'/'metadata' objects."
    ),
    include_schema=True,
    include_examples=True,
)

root_agent = Agent(
    name="root_agent",
    model=Gemini(
        model=MODEL,
        retry_options=types.HttpRetryOptions(attempts=3),
    ),
    instruction=instruction,
    tools=[
        PreloadMemoryTool(),
        fetch_and_save_new_post,
        fetch_saved_posts_from_storage,
        save_post_to_storage,
        mark_post_processed_in_storage,
        get_candidate_profile,
        update_candidate_profile,
        analyze_post_for_opportunity,
        fetch_job_seeking_frameworks,
        evaluate_job_seeker_draft,
        save_opportunity_draft,
    ],
    after_model_callback=a2ui_callback,
    after_agent_callback=generate_memories_callback,
)

app = App(
    root_agent=root_agent,
    name="app",
)
