Absolutely, here's a **detailed frontend description and design plan** for the **"Cavity" screen** based on the JSON structure and dropdown-post system you've outlined:

---

## 🧾 **Cavity Screen – Frontend Design & Behavior (No Code)**

### 🎯 **Purpose**

The **Cavity screen** serves as a knowledge-sharing or discussion hub where **medical students** and **aspirants** can read posts created by others from various medical year levels (e.g., NEET 2025, MBBS 1st year, Internship, etc.).

---

## 🧱 **Page Structure Overview**

### 1. **Header Section**

* **Title/Logo:** Top-left corner – a simple app name or logo (e.g., “Cavity”).
* **Dropdown Menu:**

  * Labelled with a default year (e.g., **“NEET 2025”**).
  * Beside the text, include a **dropdown arrow icon (⌄)**.
  * When tapped, a **modal pops up** from the bottom or center showing all the options:

    ```
    NEET 2025
    1st year MBBS
    2nd year MBBS
    3rd year MBBS
    4th year MBBS
    Overseas Edu
    Next Exam
    X Group
    ```
  * Modal includes:

    * Search box (optional, for large lists).
    * Tap to select another year group.
    * Modal closes automatically on selection.
  * After selection:

    * The dropdown label updates.
    * The **post feed reloads** with content relevant to the selected group.

---

### 2. **Main Feed Area**

Each **user** (author) has **1 medical year tag** (from the dropdown options), but may have **multiple posts**. Posts are grouped under users.

#### 🧑‍⚕️ Author Card (for each user):

* **Profile Section:**

  * Placeholder **large red square** (used for profile image).
  * Right side:

    * **Author Name** (e.g., *Dr. Aisha Rehman*).
    * **Role/Tag**: Year label (e.g., “3rd year MBBS”), styled like a pill-shaped tag.
* **Divider** (light gray line or spacing) to separate user section.

#### ✍️ Post Block (Under Each User):

* Each post contains:

  * **Date or Time** (optional – like “2 days ago” or “July 30, 2025”).
  * **Content Text**:

    * Between **2 to 6 paragraphs** per post.
    * Paragraphs should have **line height spacing** and a clean **serif font** for reading comfort.
    * Emojis (optional) can be used for engagement.
  * **Actions Row** (optional):

    * Icons for **like**, **comment**, or **share** (inactive for now).
    * Count bubbles like “12 likes”, “5 comments” (optional).

---

### 3. **Floating Action Button (FAB)** (Optional)

* Bottom-right floating **“+” button**.
* Clicking/tapping opens a modal/screen to **add new post** *(if posting is allowed)*.

---

## 🧩 UI/UX Notes

* All sections should be **vertically scrollable**.
* Use **cards or white containers** for each user’s section.
* Dropdown and modal must be **responsive** (expand full screen on small devices).
* **No page refresh** – content should reload dynamically when dropdown is changed.
* Group user posts **clearly** so that each author’s identity and year is easily identifiable.

---

## 🪄 Animation Suggestions

* **Modal open/close**: Slide-up from bottom or fade-in.
* **Dropdown arrow**: Rotate 180° when active.
* **Post entries**: Fade-in or slide-from-bottom when loaded or switched.

---

## 🎨 Styling Guidelines

| Element           | Style Suggestion             |
| ----------------- | ---------------------------- |
| Background        | Light gray or off-white      |
| Profile image     | Square with red background   |
| Fonts             | Serif or humanist sans-serif |
| Paragraph spacing | 1.6x line height             |
| Dropdown pills    | Rounded edges, soft shadow   |
| Modal background  | White with light border      |
| Divider lines     | #E0E0E0 or similar           |

---

## 🧪 Testing Ideas

* Switch between years quickly – ensure smooth data transition.
* Ensure long posts don’t break layout.
* Try displaying 3 users with 2-3 posts each and scroll through.

---

Would you like a wireframe or UI mockup suggestion next?
