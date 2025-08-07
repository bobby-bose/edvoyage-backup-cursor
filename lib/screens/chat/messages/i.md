# Messages Screen UI Instructions (Frontend)

## Overview:
This screen displays a vertically scrollable list of users who have sent messages. The latest conversations appear at the top (descending timestamp). Each message preview includes the sender’s name, profile image, a short snippet of the last message, timestamp, and unread count.

---

## Layout Structure (Vertical Column)

1. **Top App Bar**
   - Title: `Messages`
   - Optional icons:
     - Left: Menu/Hamburger or back arrow
     - Right: New message icon or search icon

2. **Messages List (Scrollable)**
   - Each message entry is a **Card** or **ListTile** style widget containing:

     - **Left**: Circular avatar (Red container with initial letter for now)
     - **Center**:
       - Name (bold)
       - Latest message snippet (2-line max, ellipsized if long)
     - **Right**:
       - Timestamp (e.g., "8:10 PM")
       - Unread count badge (e.g., red circle with number)

---

## Avatar (Profile Image)
- Use a red circular container temporarily with the user’s first initial.
- Later replace with profileImage from the JSON.
- Example placeholder: `https://via.placeholder.com/150/FF0000/FFFFFF?text=A`

---

## Unread Message Badge
- Show only if `unreadCount > 0`
- Style:
  - Red circle (small)
  - White text
  - Positioned at the top-right corner or beside timestamp

---

## Scroll Behavior
- Entire list should be scrollable
- Pull-to-refresh can be added later

---

## Responsiveness
- Should work on phones and tablets.
- Text should not overflow; use ellipsis `...` for long messages.

---

## Data Handling Instructions (Backend Integration Later)
- Fetch message list from `messages.json`
- Sort entries by `timestamp` descending
- Parse `unreadCount` to determine if badge is needed
- Use fallback image if `profileImage` is missing

---

## Optional Enhancements (Future)
- Tap on a message item → navigate to full chat screen
- Long press for delete/archive
- Swipe left/right for quick actions

---

## Notes for Cursor AI
- Keep code modular
- Store data temporarily in a state or provider
- Use mock data now, wire up backend later
