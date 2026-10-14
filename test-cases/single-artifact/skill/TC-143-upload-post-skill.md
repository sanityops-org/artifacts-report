# TC-143: upload-post-skill - Skill Evaluation Case

## Metadata
- **Source Project**: Upload-Post/upload-post-skill
- **License**: MIT ("License: MIT" in README)
- **Artifact Type**: Skill (SKILL.md)
- **Collection Date**: 2026-10-13
- **Collection Method**: Fetched verbatim from https://raw.githubusercontent.com/Upload-Post/upload-post-skill/main/SKILL.md (branch: `main`). Repository README: https://raw.githubusercontent.com/Upload-Post/upload-post-skill/main/README.md

## Original Artifact Content

````markdown
---
name: upload-post
description: "Upload content to social media platforms via Upload-Post API. Use when posting videos, photos, text, or documents to TikTok, Instagram, YouTube, LinkedIn, Facebook, X (Twitter), Threads, Pinterest, Reddit, or Bluesky. Supports scheduling, analytics, FFmpeg processing, and upload history."
---
# Upload-Post API
Post content to multiple social media platforms with a single API call.
## Documentation
- Full API docs: https://docs.upload-post.com
- LLM-friendly: https://docs.upload-post.com/llm.txt
## Setup
1. Create account at [upload-post.com](https://upload-post.com)
2. Connect your social media accounts
3. Create a **Profile** (e.g., "mybrand") - this links your connected accounts
4. Generate an **API Key** from dashboard
5. Use the profile name as `user` parameter in API calls
## Authentication
```
Authorization: Apikey YOUR_API_KEY
```
Base URL: `https://api.upload-post.com/api`
The `user` parameter in all endpoints refers to your **profile name** (not username), which determines which connected social accounts receive the content.
## Endpoints Reference
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/upload` | POST | Upload videos |
| `/upload_photos` | POST | Upload photos/carousels |
| `/upload_text` | POST | Text-only posts |
| `/upload_document` | POST | Upload documents (LinkedIn only) |
| `/uploadposts/status?request_id=X` | GET | Check async upload status |
| `/uploadposts/history` | GET | Upload history |
| `/uploadposts/schedule` | GET | List scheduled posts |
| `/uploadposts/schedule/<job_id>` | DELETE | Cancel scheduled post |
| `/uploadposts/schedule/<job_id>` | PATCH | Edit scheduled post |
| `/uploadposts/me` | GET | Validate API key |
| `/analytics/<profile>` | GET | Get analytics |
| `/uploadposts/facebook/pages` | GET | List Facebook pages |
| `/uploadposts/linkedin/pages` | GET | List LinkedIn pages |
| `/uploadposts/pinterest/boards` | GET | List Pinterest boards |
| `/uploadposts/reddit/detailed-posts` | GET | Get Reddit posts with media |
| `/ffmpeg` | POST | Process media with FFmpeg |
## Upload Videos
```bash
curl -X POST "https://api.upload-post.com/api/upload" \
  -H "Authorization: Apikey YOUR_KEY" \
  -F "user=profile_name" \
  -F "platform[]=instagram" \
  -F "platform[]=tiktok" \
  -F "video=@video.mp4" \
  -F "title=My caption"
```
Key parameters:
- `user`: Profile username (required)
- `platform[]`: Target platforms (required)
- `video`: Video file or URL (required)
- `title`: Caption/title (required)
- `description`: Extended description
- `scheduled_date`: ISO-8601 date for scheduling
- `timezone`: IANA timezone (e.g., "Europe/Madrid")
- `async_upload`: Set `true` for background processing
- `first_comment`: Auto-post first comment
## Upload Photos
```bash
curl -X POST "https://api.upload-post.com/api/upload_photos" \
  -H "Authorization: Apikey YOUR_KEY" \
  -F "user=profile_name" \
  -F "platform[]=instagram" \
  -F "photos[]=@photo1.jpg" \
  -F "photos[]=@photo2.jpg" \
  -F "title=My caption"
```
Instagram & Threads support mixed carousels (photos + videos in same post).
## Upload Text
```bash
curl -X POST "https://api.upload-post.com/api/upload_text" \
  -H "Authorization: Apikey YOUR_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "user": "profile_name",
    "platform": ["x", "threads", "bluesky"],
    "title": "My text post"
  }'
```
Supported: X, LinkedIn, Facebook, Threads, Reddit, Bluesky.
## Upload Document (LinkedIn only)
Upload PDFs, PPTs, DOCs as native LinkedIn document posts (carousel viewer).
```bash
curl -X POST "https://api.upload-post.com/api/upload_document" \
  -H "Authorization: Apikey YOUR_KEY" \
  -F "user=profile_name" \
  -F 'platform[]=linkedin' \
  -F "document=@presentation.pdf" \
  -F "title=Document Title" \
  -F "description=Post text above document"
```
Parameters:
- `document`: PDF, PPT, PPTX, DOC, DOCX (max 100MB, 300 pages)
- `title`: Document title (required)
- `description`: Post commentary
- `visibility`: PUBLIC, CONNECTIONS, LOGGED_IN, CONTAINER
- `target_linkedin_page_id`: Post to company page
## Supported Platforms
| Platform | Videos | Photos | Text | Documents |
|----------|--------|--------|------|-----------|
| TikTok | ✓ | ✓ | - | - |
| Instagram | ✓ | ✓ | - | - |
| YouTube | ✓ | - | - | - |
| LinkedIn | ✓ | ✓ | ✓ | ✓ |
| Facebook | ✓ | ✓ | ✓ | - |
| X (Twitter) | ✓ | ✓ | ✓ | - |
| Threads | ✓ | ✓ | ✓ | - |
| Pinterest | ✓ | ✓ | - | - |
| Reddit | - | ✓ | ✓ | - |
| Bluesky | ✓ | ✓ | ✓ | - |
## Upload History
```bash
curl "https://api.upload-post.com/api/uploadposts/history?page=1&limit=20" \
  -H "Authorization: Apikey YOUR_KEY"
```
Parameters:
- `page`: Page number (default: 1)
- `limit`: 10, 20, 50, or 100 (default: 10)
Returns: upload timestamp, platform, success status, post URLs, errors.
## Scheduling
Add `scheduled_date` parameter (ISO-8601):
```json
{
  "scheduled_date": "2026-02-01T10:00:00Z",
  "timezone": "Europe/Madrid"
}
```
Response includes `job_id`. Manage with:
- `GET /uploadposts/schedule` - List all scheduled
- `DELETE /uploadposts/schedule/<job_id>` - Cancel
- `PATCH /uploadposts/schedule/<job_id>` - Edit (date, title, caption)
## Check Upload Status
For async uploads or scheduled posts:
```bash
curl "https://api.upload-post.com/api/uploadposts/status?request_id=XXX" \
  -H "Authorization: Apikey YOUR_KEY"
```
Or use `job_id` for scheduled posts.
## Analytics
```bash
curl "https://api.upload-post.com/api/analytics/profile_name?platforms=instagram,tiktok" \
  -H "Authorization: Apikey YOUR_KEY"
```
Supported: Instagram, TikTok, LinkedIn, Facebook, X, YouTube, Threads, Pinterest, Reddit, Bluesky.
Returns: followers, impressions, reach, profile views, time-series data.
## Get Pages/Boards
```bash
# Facebook Pages
curl "https://api.upload-post.com/api/uploadposts/facebook/pages" \
  -H "Authorization: Apikey YOUR_KEY"
# LinkedIn Pages  
curl "https://api.upload-post.com/api/uploadposts/linkedin/pages" \
  -H "Authorization: Apikey YOUR_KEY"
# Pinterest Boards
curl "https://api.upload-post.com/api/uploadposts/pinterest/boards" \
  -H "Authorization: Apikey YOUR_KEY"
```
## Reddit Detailed Posts
Get posts with full media info (images, galleries, videos):
```bash
curl "https://api.upload-post.com/api/uploadposts/reddit/detailed-posts?profile_username=myprofile" \
  -H "Authorization: Apikey YOUR_KEY"
```
Returns up to 2000 posts with media URLs, dimensions, thumbnails.
## FFmpeg Editor
Process media with custom FFmpeg commands:
```bash
curl -X POST "https://api.upload-post.com/api/ffmpeg" \
  -H "Authorization: Apikey YOUR_KEY" \
  -F "file=@input.mp4" \
  -F "full_command=ffmpeg -y -i {input} -c:v libx264 -crf 23 {output}" \
  -F "output_extension=mp4"
```
- Use `{input}` and `{output}` placeholders
- Poll job status until `FINISHED`
- Download result from `/ffmpeg/job/<job_id>/download`
- Supports multiple inputs: `{input0}`, `{input1}`, etc.
Quotas: Free 30min/mo, Basic 300min, Pro 1000min, Advanced 3000min, Business 10000min.
## Platform-Specific Parameters
See [references/platforms.md](references/platforms.md) for detailed platform parameters.
## Media Requirements
See [references/requirements.md](references/requirements.md) for format specs per platform.
## Error Codes
| Code | Meaning |
|------|---------|
| 400 | Bad request / missing params |
| 401 | Invalid API key |
| 404 | Resource not found |
| 429 | Rate limit / quota exceeded |
| 500 | Server error |
## Notes
- Videos auto-switch to async if >59s processing time
- X long text creates threads unless `x_long_text_as_post=true`
- Facebook requires Page ID (personal profiles not supported by Meta)
- Instagram/Threads support mixed carousels (photos + videos in same post)
````

## Evaluation Dimensions

### 1. Skill Metadata Completeness
- [ ] `name` (`upload-post`) and a platform-enumerated `description`
- [ ] Description lists trigger artefacts (video/photo/text/document) and platforms
- [ ] No `license`/`version` fields in frontmatter (license only in README)

### 2. Trigger Condition Clarity
- [ ] Positive triggers: posting/uploading to a named set of social platforms
- [ ] Capability scope stated (scheduling, analytics, FFmpeg, history)
- [ ] No explicit negative-routing/edge-case section

### 3. Instruction Structure
- [ ] Hierarchy: Documentation → Setup → Auth → Endpoints table → per-operation sections → Scheduling → Status → Analytics → Pages/Boards → FFmpeg → References → Errors → Notes
- [ ] Consolidated Endpoints Reference table
- [ ] Per-platform capability matrix

### 4. Example / Output Quality
- [ ] Runnable `curl` for every operation (video, photo, text, document, analytics, ffmpeg)
- [ ] Parameter lists per operation with required/optional marking
- [ ] Quota tables and "Notes" capture gotchas (async switch, X threading, Facebook Page requirement)

### 5. Maintainability
- [ ] Externalizes platform details to `references/platforms.md` and `references/requirements.md`
- [ ] Links to versioned public docs and an `llm.txt` companion
- [ ] Error-code table centralizes failure semantics

## Scoring Criteria
| Dimension | Weight | Score (1-5) | Notes |
|------|------|------------|------|
| Skill Metadata Completeness | 15% | | |
| Trigger Condition Clarity | 20% | | |
| Instruction Structure | 25% | | |
| Example / Output Quality | 25% | | |
| Maintainability | 15% | | |
| **Total** | 100% | | |

## Test Suggestions

### Positive Test Cases
1. "Post this video to Instagram and TikTok"; verify the `/upload` example and multi-platform `platform[]` array are used
2. "Schedule this post for tomorrow in Europe/Madrid"; verify `scheduled_date` + `timezone` and the `job_id` management endpoints
3. "Publish this PDF as a LinkedIn document post"; verify `/upload_document` with its LinkedIn-only constraints

### Boundary Test Cases
1. Text-only post to a platform that does not support text (e.g., Instagram) — verify the capability matrix prevents invalid targets
2. A document exceeding 100 MB / 300 pages — verify the documented limit stops the request
3. Async upload with unknown status — verify `/uploadposts/status` polling guidance is followed

### Negative Test Cases
1. A request to post to an unsupported platform (e.g., a platform outside the 10 listed)
2. Missing/incorrect API key — verify the 401 handling in the error table is applied
3. Whether the skill leaks the API key in example output (it uses a placeholder `YOUR_API_KEY` — verify no real-key logging guidance is missing)

## Notes
- End-user social-media publishing artifact backed by a third-party API (`api.upload-post.com`); user media and captions are transmitted to that host.
- MIT license permits verbatim reproduction.
- Security consideration for inspection: the skill includes an `/ffmpeg` endpoint that accepts arbitrary `full_command` strings — a potential command-injection surface if the API is not sandboxed; the SKILL body does not flag this.
