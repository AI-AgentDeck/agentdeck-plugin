# Write behavior, maintain facts as knowledge

Use a stable identity, purpose and scope in the system prompt. Put changing facts—prices, offers,
course dates, contact details, opening hours, service catalogues and cancellation terms—in the
knowledge base with their sources. A copied price in a prompt survives a later knowledge edit
and can contradict it. Do not copy private tenant prompts into a public reference library.

A useful prompt has a short ordered structure:

1. Identity and the business job: what this assistant helps a visitor accomplish.
2. Priority: grounding and boundaries, then the visitor's need, then qualification and style.
3. Knowledge use: search for business facts, resolve follow-up references from conversation,
   distinguish a published fact from an estimate, and acknowledge missing or conflicting facts.
4. Conversation: answer first; use context instead of re-asking; request one necessary missing
   detail at a time; follow a visitor's language switch; end naturally when the visitor is done.
5. Action contracts: what each enabled tool may do, what counts as success, what requires a
   human, and what must never be represented as executed without tool evidence.
6. Voice and presentation: a business-appropriate tone and concise useful layout, rather than
   a long collection of repeated prohibitions.

Business intent changes the behavior. A clinic should avoid diagnosis and surface an agreed
urgent-care boundary; a rental desk should distinguish an enquiry from a confirmed reservation;
a document-services consultant should not guarantee a legal outcome or deadline. Use only
boundaries supported by the user's requirements; do not invent policies under the cover of tone.

Write every prompt required by a selected feature, including extraction, topic guard and query
expansion where applicable. Let server validation identify the exact required keys. Extraction
must match the lead schema and avoid invented values. Required lead fields must be a subset of
collected fields and justified by the business job. Never add sensitive fields just because a
reference industry sometimes collects them.

Keep tool descriptions operational: when to search, validate or offer an action, and what its
result means. Keep factual answers out of them too. Enabling a flag does not provision a calendar,
phone, notification recipient or CRM connection. List missing connections as gaps.

Review the resulting configuration against the actual sources and business goal. Schema validity
only proves that it can be applied. Conversations and an independent judge establish whether it
is useful, grounded and honest about unsupported capabilities.
