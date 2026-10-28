# Publishing

A READY agent has no further switch to flip: it answers wherever its snippet is placed, and the
customer may place it on several websites. Conversations started from the client hub's test chat,
the preview link or `test_agent` are test chats and trigger no alerts, CRM writes or bookings;
conversations anywhere else are real.

Publishing is therefore a handover, not an API call. Prepare it with:

- Agent UUID, environment, reviewed version and portable bundle path.
- The server-returned widget snippet, and the websites the user wants it on.
- Acceptance report and unresolved business or integration questions.
- Channels requested (WhatsApp, Instagram, Messenger, phone) and the client hub flows that connect them.

Placing the snippet on a public site and connecting channels make the agent reach real people: do it
only with the user's explicit authorization for that agent, environment and site. Keep real-channel
smoke tests separate from test chats and disclose any real calls or notifications before performing
them. Plans, payment and customer self-service belong to later product phases.
