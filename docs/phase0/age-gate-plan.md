# Age gate and minors' data: product plan

_This is a product plan, not legal advice. It describes what the site will do so counsel can say whether it is enough. Items marked **[counsel]** cannot be finalized until the matching question in `counsel-questions.md` is answered. Items marked **[vendor]** depend on the LLM vendor decision (Gemini exception, other vendor, or 18+ only)._

## Goals

1. Never create an account for an under-13 user without verifiable parental consent, because the amended COPPA Rule (compliance date April 22, 2026) covers under-13s and some PSAT 8/9 students will arrive.
2. Make a parent the payer and the contracting party, so consent, notice and billing happen in one place.
3. Collect as little as the product needs, name every third party that receives data, and keep tutor chat logs for a short, stated time.
4. Keep the flow neutral, so the screen doesn't teach a child what birthday to enter.
5. Leave room for whatever the LLM vendor path turns out to be, including an 18+-only launch.

## The flow

```
Landing page
  └─ "Start" ──> Date-of-birth screen (neutral)
                   ├─ computed age ≥ 18 ──> Adult signup (self-paid; or parent-paid if they choose)
                   ├─ 13–17 ─────────────> Student profile stub ──> Parent email ──> Parent checkout + notice ──> Account active
                   └─ < 13 ─────────────> Stop. Parent-email form only ──> Verifiable parental consent ──> Parent checkout ──> Account active
                                                                           (no student account exists until consent is recorded)
```

### Step 1: the date-of-birth screen

- One field: date of birth (month, day, year). No "Are you over 13?" checkbox, no wording that reveals a threshold, no example date near a cutoff.
- The page says only: "We ask everyone's date of birth so we can set up the right kind of account."
- After submit, store a one-way hash of the DOB plus the computed age bucket (under 13 / 13–17 / 18+) in a short-lived cookie, so the same browser can't resubmit a different date to get a different outcome within a reasonable window. **[counsel: 3.2]** on what "neutral" and "no retry" need to look like, and on how long that cookie may live.
- Don't store the raw DOB on the server before an account exists. For an account, store **birth year** (or the age bucket) only, unless counsel says the full DOB is needed.

### Step 2a: 18+

- Normal signup. Email, password (or magic link), first name.
- The parent-paid path is still offered as an option ("Someone else is paying? Enter their email."), because many 18-year-old seniors have a parent paying.
- **[vendor]** If the chosen path is "18+ only", this is the only path that creates an account; the 13–17 and under-13 branches below become a waitlist that collects a parent email and nothing else. Counsel question 1.4 asks whether 18+ verification by DOB alone would be defensible.

### Step 2b: 13–17

- Collect: first name, student email (optional; may be the parent's), a username, and the parent's email. No last name, phone, school or address.
- Send the parent an email with: what the product is, what data is collected (list below), who receives it (named third parties), how to delete the account, and a link to pay.
- The student can look at a limited free preview (sample questions, no AI chat, no stored progress) while waiting. **[counsel: 3.4]** on whether parental notice is required at all for 13–17 and whether this notice-plus-payment is sufficient.
- Account becomes active when the parent completes checkout. Parent and student are linked; the parent sees progress, can download data and can delete the account.

### Step 2c: under 13

- The student sees: "Thanks. A parent or guardian needs to set this up. Enter their email and we'll send them the next step." Nothing else is collected from the child, and no account is created.
- The child's email, if they typed one earlier, is not kept. Only the parent email is kept, and only to send the consent request. If the parent doesn't act within a set period (proposed: 14 days), the request and the parent email are deleted. **[counsel: 3.2]** on what may be collected and retained pre-consent, in light of the FTC's February 2026 policy statement on age-verification data (which the notes saw only through a law-firm summary).
- The parent gets a consent page that explains the product, the data collected, the named third parties (especially the AI vendor), and the right to review and delete. Consent is given by the parent completing checkout with a payment card, plus an explicit "I am the parent or guardian and I consent" checkbox. **[counsel: 3.3]** on whether "credit card plus transaction" counts as verifiable parental consent for this product and whether a free trial (no transaction) would need a different method.
- Only after consent is recorded does the parent create the child's profile (first name or nickname, birth year, username). The parent is the account holder; the child has a profile under it.

### Step 3: parent-paid checkout (Stripe)

- The parent is the Stripe customer, the ToS party and the billing contact. Stripe Checkout; no card data touches the site.
- The checkout page shows the consent and notice text, the price, and the cancellation terms. The "I consent" checkbox is required for any account where the student is under 18.
- Log: parent email, Stripe customer ID, timestamp, consent text version, student profile ID, IP address and user agent of the consent action. (This is the consent record; see "What to log".) **[counsel: 5.2]** on anything Stripe-specific for minors.
- Offer a "parent dashboard": progress, data download, delete account, change email, cancel.

## Data minimization: what the product collects

| Data | Why | Who gets it | Retention |
|---|---|---|---|
| Birth year / age bucket | Age gate, COPPA routing | Site only | Life of account |
| Student first name or nickname, username | Display in the app | Site only | Life of account |
| Student email (optional for 13–17; none for under-13) | Login, progress emails | Site, email provider | Life of account |
| Parent email, Stripe customer ID | Consent, billing, notices | Site, Stripe, email provider | Life of account + what billing law needs |
| Item attempts, answers, timings, skill estimates | The course itself (Elo/IRT, spaced review) | Site only | Life of account; aggregated after deletion |
| Calculator snapshots (expression text) | Tutor coaching on the student's own Desmos work | Site, AI vendor (text only, per request) | Same as chat logs |
| Tutor chat messages | The tutoring conversation | Site, AI vendor | Short retention: proposed 90 days, then deleted or de-identified **[counsel: 3.5]** |
| Error logs, basic analytics | Keeping the site working | Error-logging and analytics vendors, with PII filtered and training/sharing off | 30 days (proposed) |

Explicitly **not** collected at launch: last name, address, phone, school, photos, voice, camera, screen recording, location, ad identifiers. Voice and camera are deferred because the amended COPPA Rule treats voiceprints and face templates as personal information. Any "upload a screenshot of your calculator" feature stays off until counsel confirms it isn't biometric **[counsel: 3.6]**.

## Vendor settings that must be on before any minor uses the site

- **AI vendor [vendor]:** paid tier only; training on prompts and outputs off; shortest available log retention; a DPA. Which vendor and which settings depend on counsel's answers to group 1. The LLM layer stays behind `TutorProvider` so this can change.
- **Desmos:** calculator state stays in the browser and on our server; confirm with Desmos (`desmos-licensing-email.md`) what, if anything, the hosted script collects.
- **Email provider, analytics, error logging:** no ad use, no selling, PII scrubbing, DPA.
- **Privacy policy** names each of these as a recipient category and by name where the rule requires it **[counsel: 3.5]**.

## Guardrails that are also privacy features

- The tutor chat is topic-limited to SAT math by system prompt and a classifier; a self-harm or crisis message gets a resource response and a flag, not a conversation. **[counsel: 4.3]** on state chatbot-for-minors disclosure and protocol requirements.
- The chat screen always says the tutor is an AI.
- Daily message quotas per user limit both cost and how much a minor's data is sent to the vendor.

## What to log (and what not to)

Keep:
- Consent records (who, when, which text version, how verified, IP and user agent). Immutable, kept for the life of the account plus the period counsel sets.
- Age-gate outcomes as counts only (how many under-13 / 13–17 / 18+ attempts per day), with no identifiers, to see whether under-13s are arriving.
- Parent notices sent (timestamp, template version).
- Data-deletion requests and completion.
- Vendor API calls: timestamp, model ID, token counts, and a reference to the chat message. Not a second copy of the content.

Don't keep:
- Raw DOB of failed or abandoned signups.
- Children's emails typed before consent.
- Full chat transcripts in error logs or analytics.
- Any ad or tracking pixels on pages where minors are logged in.

## Open items

| Item | Blocked on |
|---|---|
| Whether the under-13 branch is "consent flow" or "block entirely" | Counsel 3.1–3.3; also product choice (is the PSAT 8/9 audience worth it?) |
| Whether 13–17 accounts need parental notice, consent or neither | Counsel 3.4 |
| Whether an 18+-only launch is the path, which would collapse this plan to step 2a | Counsel 1.1–1.4 and the vendor decision |
| Consent method for a free trial with no payment | Counsel 3.3 |
| Chat retention period and the exact third-party list in the policy | Counsel 3.5 |
| Any state-law additions (design codes, chatbot disclosures, Utah/Texas) | Counsel group 4 |
| Final ToS, privacy policy and consent text | Counsel 5.1 |

## Build notes for `web/`

- The age gate is a route before signup; the age bucket is the only thing it outputs.
- Accounts have a `holder` (parent or adult) and zero or more `profiles` (students). Billing hangs off the holder.
- A `consent_records` table with the fields under "Keep". Nothing in the tutor path runs for a profile with no active consent record when the profile's age bucket requires one.
- A scheduled job deletes expired pre-consent parent-email requests and expired chat logs.
