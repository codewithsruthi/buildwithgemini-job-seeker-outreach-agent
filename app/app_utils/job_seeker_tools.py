"""Tools for drafting opportunity-focused LinkedIn cold messages leveraging high-performing posts."""

import json
import re
from typing import Any, Dict, List, Optional


JOB_SEEKER_FRAMEWORKS = {
    "high_post_reaction": {
        "id": "high_post_reaction",
        "name": "High-Impact Post to Opportunity Bridge",
        "description": "Engage a leader/recruiter based on an impressive post (milestone, tech breakthrough, team culture) and bridge to your active job search.",
        "best_for": "Engaging hiring managers, CTOs, Engineering Directors, and founders who just shared an insightful or viral post.",
        "hook_example": "Hi [Name], loved your recent post on [Topic]—especially how your team tackled [Specific Challenge].",
        "framework": (
            "1. Natural, warm greeting (e.g., 'Hi [Name], hope you're having a great week!')\n"
            "2. Specific compliment/insight on their high-engagement post\n"
            "3. Seamless transition stating you are actively exploring new opportunities in this domain\n"
            "4. Quick 1-line value proposition / relevant background match\n"
            "5. Low-friction conversational ask (e.g., 'Open to a brief connection or chat if your team is growing?')"
        ),
        "example_draft": (
            "Hi {{first_name}},\n\n"
            "Hope you're having a great week! Loved your recent post about {{topic}}—especially how you handled {{specific_point}}. Resonated strongly with what I've seen in the field.\n\n"
            "I'm currently actively exploring new {{role_title}} opportunities and admire the direction {{company}} is taking. I've spent the last {{years}} years specializing in {{core_skill}}.\n\n"
            "If your team is growing or open to new talent, would you be open to connecting?"
        ),
    },
    "team_growth_milestone": {
        "id": "team_growth_milestone",
        "name": "Hiring Announcement / Team Milestone",
        "description": "Reach out directly when someone posts about team expansion, product launches, or funding.",
        "best_for": "Teams with active headcount expansion or recent major releases.",
        "hook_example": "Hi [Name], huge congratulations on [Milestone / Launch]!",
        "framework": (
            "1. Warm greeting & genuine congratulations on the milestone\n"
            "2. Note on how their mission/scale excites you\n"
            "3. Transparent note that you are on the market seeking your next challenge\n"
            "4. Low-friction ask to send your background or chat briefly"
        ),
        "example_draft": (
            "Hi {{first_name}},\n\n"
            "Congratulations on the recent {{milestone}}! Seeing {{company}}'s trajectory with {{product_or_area}} is really inspiring.\n\n"
            "I'm currently on the market actively seeking my next {{role_title}} role. Having built {{relevant_project_or_metric}}, I'd love to bring that momentum to {{company}}.\n\n"
            "Are you open to a quick 10-minute introductory chat to see if there might be a fit?"
        ),
    },
    "technical_alignment": {
        "id": "technical_alignment",
        "name": "Engineering Deep Dive / Architecture Post",
        "description": "Align directly with a technical post (architecture choice, refactoring, performance win).",
        "best_for": "Connecting with engineering managers, staff engineers, or technical recruiters.",
        "hook_example": "Hi [Name], really appreciated your breakdown on [Tech / Architecture Decision].",
        "framework": (
            "1. Respectful greeting\n"
            "2. Direct technical callout from their post\n"
            "3. State that you work in the exact same stack and are currently seeking new opportunities\n"
            "4. Conversational question or offer to share portfolio"
        ),
        "example_draft": (
            "Hi {{first_name}},\n\n"
            "Hope all is well! Really enjoyed your post detailing {{tech_topic}}—your approach to {{sub_point}} was spot on.\n\n"
            "I work extensively with {{tech_stack}} and am actively looking for my next opportunity building scalable systems. Would love to stay connected and explore whether there could be mutual fit as {{company}} grows.\n\n"
            "Would you be open to connecting?"
        ),
    },
}


def analyze_post_for_opportunity(
    post_content: str,
    target_name: str,
    company: Optional[str] = None,
    desired_role: Optional[str] = None,
    candidate_background: Optional[str] = None
) -> str:
    """Analyzes a high-engagement LinkedIn post and derives personalized hooks bridging to an active job search.

    Args:
        post_content: The text or summary of the target's high-performing LinkedIn post.
        target_name: Name of the hiring manager, recruiter, or author.
        company: Company or organization name.
        desired_role: The role the candidate is seeking (e.g. 'Senior Software Engineer', 'Product Manager').
        candidate_background: Brief summary of candidate's key skills or experience.

    Returns:
        JSON string containing the extracted hook, bridge narrative, and recommended outreach strategy.
    """
    first_name = target_name.split()[0] if target_name else "there"
    
    # Extract topics or keywords
    post_preview = post_content.strip()[:80] + ("..." if len(post_content) > 80 else "")

    recommendations = {
        "first_name": first_name,
        "target_company": company or "their company",
        "desired_role": desired_role or "your target role",
        "post_analysis": {
            "post_preview": post_preview,
            "bridge_strategy": (
                f"Acknowledge the specific insight from their post, express genuine interest in {company or 'their team'}'s engineering/product culture, "
                f"and transparently state you are actively exploring {desired_role or 'new'} opportunities."
            )
        },
        "suggested_greeting": f"Hi {first_name}, hope you're having a great week!",
        "key_elements_to_include": [
            "1. Natural, polite greeting (always start with 'Hi [Name], ...' or 'Hey [Name], hope all is well!')",
            "2. Specific reference to their post so it feels 100% handcrafted.",
            "3. Clear, confident statement: actively exploring new opportunities in this domain.",
            "4. 1-sentence value snapshot (e.g., tech stack, past achievements).",
            "5. Low-pressure call to action (connect, or share a brief resume/portfolio link)."
        ]
    }
    return json.dumps(recommendations, indent=2)


def fetch_job_seeking_frameworks(angle: Optional[str] = None) -> str:
    """Fetches proven cold outreach frameworks tailored for job seekers reaching out to hiring managers.

    Args:
        angle: Optional filter ('high_post_reaction', 'team_growth_milestone', 'technical_alignment', or 'all').

    Returns:
        JSON string of frameworks.
    """
    if not angle or angle.lower() in ("all", "none", ""):
        return json.dumps(list(JOB_SEEKER_FRAMEWORKS.values()), indent=2)

    cat_key = angle.lower().strip()
    for key, tmpl in JOB_SEEKER_FRAMEWORKS.items():
        if cat_key in key or key in cat_key:
            return json.dumps(tmpl, indent=2)

    return json.dumps({
        "all_frameworks": list(JOB_SEEKER_FRAMEWORKS.values())
    }, indent=2)


def evaluate_job_seeker_draft(
    draft_text: str,
    target_role: Optional[str] = None
) -> str:
    """Evaluates a job-seeker LinkedIn cold message on greeting, post relevance, active-search tone, word count, and CTA.

    Args:
        draft_text: The complete text of the cold message.
        target_role: The role being targeted.

    Returns:
        JSON string with word count, greeting check, CTA analysis, and improvement recommendations.
    """
    clean_text = draft_text.strip()
    words = clean_text.split()
    word_count = len(words)
    char_count = len(clean_text)

    score = 100
    strengths = []
    deductions = []

    # 1. Greeting Check
    greetings = ["hi ", "hello ", "hey ", "good morning", "good afternoon"]
    has_greeting = any(clean_text.lower().startswith(g) for g in greetings)
    if not has_greeting:
        score -= 20
        deductions.append("Missing a natural greeting at the start (e.g., 'Hi [Name],' or 'Hey [Name], hope you're having a great week!').")
    else:
        strengths.append("Starts with a warm, natural greeting.")

    # 2. Opportunity / Job Seeking Intent
    search_keywords = ["actively exploring", "actively looking", "on the market", "seeking", "opportunity", "opportunities", "next role", "growing your team", "hiring"]
    has_search_intent = any(k in clean_text.lower() for k in search_keywords)
    if not has_search_intent:
        score -= 15
        deductions.append("Does not explicitly clarify that you are actively seeking opportunities or inquiring about team growth.")
    else:
        strengths.append("Clearly states your active search intent with confidence.")

    # 3. Post reference
    post_keywords = ["post", "article", "recent share", "read your", "congratulations", "saw your"]
    has_post_ref = any(k in clean_text.lower() for k in post_keywords)
    if not has_post_ref:
        score -= 15
        deductions.append("Does not clearly anchor on their high-performing post or milestone.")
    else:
        strengths.append("Grounds the message in their recent post or announcement.")

    # 4. Length check (Ideal: 45 - 85 words for cold messages)
    if word_count < 30:
        score -= 15
        deductions.append(f"Too short ({word_count} words). Elaborate slightly on your background or the post insight.")
    elif 30 <= word_count <= 85:
        strengths.append(f"Ideal length ({word_count} words). High mobile engagement likelihood.")
    elif 85 < word_count <= 120:
        score -= 10
        deductions.append(f"A bit long ({word_count} words). Busy hiring managers prefer messages under 85 words.")
    else:
        score -= 25
        deductions.append(f"Too long ({word_count} words). Trim down context to increase response rates.")

    # 5. Call to action
    has_question = "?" in clean_text
    if not has_question:
        score -= 15
        deductions.append("No clear conversational question or CTA found.")
    else:
        strengths.append("Includes a clear, low-pressure question/ask.")

    final_score = max(10, min(100, score))
    status = "Excellent" if final_score >= 85 else ("Good" if final_score >= 70 else "Needs Improvement")

    return json.dumps({
        "overall_score": final_score,
        "status": status,
        "metrics": {
            "word_count": word_count,
            "character_count": char_count,
            "has_proper_greeting": has_greeting,
            "has_post_reference": has_post_ref,
            "has_opportunity_mention": has_search_intent,
            "target_role": target_role or "Unspecified"
        },
        "strengths": strengths,
        "improvement_suggestions": deductions if deductions else ["Message is sharp, respectful, and ready to send!"]
    }, indent=2)


_SAVED_OPPORTUNITIES: List[Dict[str, Any]] = []

def save_opportunity_draft(
    target_name: str,
    company: str,
    role_sought: str,
    post_reference: str,
    draft_text: str
) -> str:
    """Saves a draft and target details to your active opportunity tracker.

    Args:
        target_name: Name of hiring manager/author.
        company: Target company.
        role_sought: Role you are targeting.
        post_reference: Note on the post that inspired the reach-out.
        draft_text: The drafted cold message.

    Returns:
        JSON string confirming save.
    """
    entry = {
        "id": len(_SAVED_OPPORTUNITIES) + 1,
        "target_name": target_name,
        "company": company,
        "role_sought": role_sought,
        "post_reference": post_reference,
        "draft_text": draft_text,
        "status": "Ready to Send"
    }
    _SAVED_OPPORTUNITIES.append(entry)
    return json.dumps({
        "success": True,
        "total_saved": len(_SAVED_OPPORTUNITIES),
        "entry": entry
    }, indent=2)

import os

PROFILE_PATH = os.path.join(os.path.dirname(__file__), "..", "candidate_profile.json")

def get_candidate_profile() -> str:
    """Retrieves the user's stored professional background, skills portfolio, and message preferences.

    Returns:
        JSON string containing current role, company, target roles, skills, and drafting rules.
    """
    try:
        with open(PROFILE_PATH, "r") as f:
            data = json.load(f)
            return json.dumps(data, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Could not load candidate profile: {e}"})


def update_candidate_profile(
    current_role: Optional[str] = None,
    current_company: Optional[str] = None,
    target_roles: Optional[List[str]] = None,
    skills: Optional[List[str]] = None
) -> str:
    """Updates the user's stored profile and skills preferences.

    Args:
        current_role: Current job title (e.g. 'Data Engineer').
        current_company: Current employer (e.g. 'Meta').
        target_roles: List of roles being targeted.
        skills: List of key skills.

    Returns:
        JSON string with confirmation and updated profile.
    """
    try:
        data = {}
        if os.path.exists(PROFILE_PATH):
            with open(PROFILE_PATH, "r") as f:
                data = json.load(f)
        if current_role:
            data["current_role"] = current_role
        if current_company:
            data["current_company"] = current_company
        if target_roles:
            data["target_roles"] = target_roles
        if skills:
            data["skills_portfolio"] = skills
        with open(PROFILE_PATH, "w") as f:
            json.dump(data, f, indent=2)
        return json.dumps({"success": True, "updated_profile": data}, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Failed to update profile: {e}"})

from google.cloud import storage

BUCKET_NAME = os.environ.get("GCS_BUCKET_NAME", "linkedin-outreach-assets-6330d2b1f32f")
SAVED_POSTS_BLOB = "posts/saved_posts.json"

def fetch_saved_posts_from_storage(limit: int = 5, filter_role: Optional[str] = None) -> str:
    """Fetches saved LinkedIn posts directly from Cloud Storage bucket for drafting messages.

    Args:
        limit: Maximum number of posts to fetch (default: 5).
        filter_role: Optional keyword filter for target role (e.g., 'Data Engineer', 'Business Analyst').

    Returns:
        JSON string containing the fetched posts and their details.
    """
    try:
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(SAVED_POSTS_BLOB)
        
        if not blob.exists():
            return json.dumps({
                "status": "empty",
                "message": f"No saved posts file found at gs://{BUCKET_NAME}/{SAVED_POSTS_BLOB}. Please save some posts first."
            })
        
        content = blob.download_as_text()
        posts = json.loads(content)
        
        # Filter pending posts
        pending = [p for p in posts if p.get("status") in ("pending", "to_draft", None)]
        
        if filter_role:
            role_kw = filter_role.lower().strip()
            pending = [p for p in pending if role_kw in p.get("target_role", "").lower() or role_kw in p.get("post_content", "").lower()]
        
        selected = pending[:limit]
        
        return json.dumps({
            "status": "success",
            "bucket": BUCKET_NAME,
            "total_pending": len(pending),
            "returned_count": len(selected),
            "posts": selected
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Failed to fetch posts from Cloud Storage: {str(e)}"})


def save_post_to_storage(
    target_name: str,
    company: str,
    post_content: str,
    target_role: Optional[str] = None,
    post_url: Optional[str] = None
) -> str:
    """Saves a new LinkedIn post or lead into your Cloud Storage bucket (posts/saved_posts.json).

    Args:
        target_name: Name of hiring manager / author.
        company: Target company.
        post_content: Text or summary of the post.
        target_role: Role targeted (e.g. 'Data Engineer', 'Business Analyst').
        post_url: URL to the post if available.

    Returns:
        JSON string confirming post was added to Cloud Storage.
    """
    try:
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(SAVED_POSTS_BLOB)
        
        posts = []
        if blob.exists():
            try:
                posts = json.loads(blob.download_as_text())
            except Exception:
                posts = []
                
        new_entry = {
            "id": f"post_{len(posts) + 1:03d}",
            "target_name": target_name,
            "company": company,
            "target_role": target_role or "Data Engineer / Analyst",
            "post_url": post_url or "",
            "post_content": post_content,
            "status": "pending"
        }
        posts.append(new_entry)
        
        blob.upload_from_string(json.dumps(posts, indent=2), content_type="application/json")
        
        return json.dumps({
            "success": True,
            "message": f"Successfully saved post for {target_name} at {company} to Cloud Storage (gs://{BUCKET_NAME}/{SAVED_POSTS_BLOB})",
            "total_posts": len(posts),
            "entry": new_entry
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": f"Failed to save post to Cloud Storage: {str(e)}"})


def mark_post_processed_in_storage(post_id: str, status: str = "drafted") -> str:
    """Marks a post as processed/drafted in Cloud Storage so it isn't repeatedly drafted.

    Args:
        post_id: The ID of the post (e.g. 'post_001').
        status: New status, e.g. 'drafted' or 'sent'.

    Returns:
        JSON confirmation.
    """
    try:
        client = storage.Client()
        bucket = client.bucket(BUCKET_NAME)
        blob = bucket.blob(SAVED_POSTS_BLOB)
        
        if not blob.exists():
            return json.dumps({"error": "Saved posts file does not exist."})
            
        posts = json.loads(blob.download_as_text())
        updated = False
        for p in posts:
            if p.get("id") == post_id:
                p["status"] = status
                updated = True
                break
                
        if updated:
            blob.upload_from_string(json.dumps(posts, indent=2), content_type="application/json")
            return json.dumps({"success": True, "message": f"Marked {post_id} as {status}."})
        else:
            return json.dumps({"error": f"Post ID {post_id} not found."})
    except Exception as e:
        return json.dumps({"error": f"Failed to update post status: {str(e)}"})

import urllib.request
import re
from html import unescape

def fetch_and_save_new_post(
    post_url: str,
    target_role: Optional[str] = None
) -> str:
    """Fetches a LinkedIn post directly from a public URL, extracts details, and automatically saves it to Cloud Storage.

    Args:
        post_url: The public URL of the LinkedIn post.
        target_role: Optional role targeted (e.g., 'Data Engineer', 'Business Analyst').

    Returns:
        JSON string containing the extracted author, company, content preview, and confirmation that it was saved to GCS.
    """
    try:
        req = urllib.request.Request(
            post_url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
        )
        html_text = ""
        with urllib.request.urlopen(req, timeout=10) as response:
            html_text = response.read().decode("utf-8", errors="ignore")
            
        author = "Author"
        company = ""
        post_content = ""

        # 1. First attempt: parse structured Schema.org ld+json (highest fidelity)
        ld_matches = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html_text, re.DOTALL)
        for match in ld_matches:
            try:
                data = json.loads(match.strip())
                if isinstance(data, dict):
                    if data.get("articleBody"):
                        post_content = data.get("articleBody")
                    if isinstance(data.get("author"), dict) and data.get("author", {}).get("name"):
                        author = data["author"]["name"]
            except Exception:
                pass

        # 2. Extract og tags
        title_match = re.search(r'<meta property="og:title" content="(.*?)"', html_text, re.IGNORECASE)
        desc_match = re.search(r'<meta property="og:description" content="(.*?)"', html_text, re.IGNORECASE)
        raw_title = unescape(title_match.group(1)) if title_match else ""
        raw_desc = unescape(desc_match.group(1)) if desc_match else ""

        if not post_content:
            post_content = raw_desc or raw_title or "Post regarding hiring and team growth"

        if author == "Author" and raw_title:
            if " | " in raw_title:
                author = raw_title.split(" | ")[-1].strip()
            elif "on LinkedIn" in raw_title:
                author = raw_title.split("on LinkedIn")[0].strip()

        if " at " in raw_title:
            company_part = raw_title.split(" at ")[1]
            company = re.split(r'[,|.]', company_part)[0].strip()

        # If company still not found, check author profile or title
        if not company or company == "Target Company":
            # Search for company mentions in post content (e.g. at [Company] or join [Company])
            comp_match = re.search(r'(?:at|join|with)\s+([A-Z][A-Za-z0-9&.'\s]{2,25}?)(?:\s+(?:team|and|is|are|,|\.|
|$))', post_content)
            if comp_match:
                company = comp_match.group(1).strip()
            else:
                company = "their team"
        
        save_res = save_post_to_storage(
            target_name=author,
            company=company,
            post_content=post_content,
            target_role=target_role or "Data Engineer / Analyst",
            post_url=post_url
        )
        
        return json.dumps({
            "status": "success",
            "extracted_data": {
                "author": author,
                "company": company,
                "content_preview": post_content[:150] + ("..." if len(post_content) > 150 else ""),
                "post_url": post_url
            },
            "gcs_save_result": json.loads(save_res)
        }, indent=2)
    except Exception as e:
        # If web request fails (e.g. auth required), save the URL so user or agent can provide details
        fallback = save_post_to_storage(
            target_name="LinkedIn Lead",
            company="Company",
            post_content=f"Post URL: {post_url}",
            target_role=target_role or "Data Engineer / Analyst",
            post_url=post_url
        )
        return json.dumps({
            "status": "partial",
            "message": f"Saved URL to Cloud Storage (could not pre-fetch full HTML: {e})",
            "gcs_save_result": json.loads(fallback)
        }, indent=2)
