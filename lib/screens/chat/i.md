🔍 DETAILED FRONTEND STRUCTURE & UX FLOW (for Contact Search Screen)
This screen resembles a WhatsApp contact search interface, designed to help users find and connect with others by name.

🧱 SCREEN LAYOUT BREAKDOWN
1. Top Bar (Search Context UI)
Time Indicator (Top-left): Standard device time.

Network + Battery Indicators (Top-right): Native iOS status icons.

Search Field:

A grey rounded-corner text field.

Prefix icon: Magnifying glass (search icon).

Placeholder Text: “Search by name…” (initially greyed out).

User Typed Text: Appears in black.

Clear (X) Button: Tapping this clears the input instantly.

Cancel (Right-aligned text button):

Tapping it exits the search screen and returns to previous screen.

2. Search Results Display
Each result is shown as a Card Row style layout with the following:

➤ Card Structure
Rounded white container with a soft shadow.

Profile Image:

Circular red placeholder container (for testing).

Fixed dimensions (e.g., 48x48px).

Name (Bold): Large, readable font (black or dark grey).

Role (Subtitle): Smaller, grey font (e.g., “Medical Student”).

Institution (Subtext): Faded or lighter grey font (e.g., “AIIMS Delhi”).

➤ Right Side of Each Card
Add/Invite Icon (Green circular button with plus “+”):

Positioned to the right.

When tapped:

May trigger an “Add” action (like send invite, follow, or request).

3. Footer Element
See More:

Center-aligned text at the bottom.

Green color to match app theme.

Tapping can load more users (pagination or scroll expansion).

4. Keyboard Integration
Keyboard is fully expanded for real-time typing.

Search results update live as the user types.

The screen automatically scrolls to keep the typed area visible.

5. Interactions
Real-time filtering: As user types, only matching names appear.

Debounce logic: Avoid searching on every keystroke; use a small delay.

Tapping a profile: (future scope) can open a detailed profile screen.

“+” button: May initiate action like “Add as peer” or “Send request”.

6. Design System Suggestions
Color palette: White, soft greys, and app's primary green.

Rounded corners for all containers and fields.

Elevation/shadow for the cards.

Use padding and spacing for a neat vertical list.