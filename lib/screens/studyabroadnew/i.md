Here is a **very detailed breakdown and UI construction guide** for the **“Study Abroad” screen** you shared, prepared in a clean `.md` documentation format. You can give this directly to your Cursor IDE or frontend team.

---

## 📘 `study_abroad_screen.md` – Study Abroad Page UI & Functional Spec

---

# ✈️ Study Abroad – UI Construction Documentation

---

## 🧭 Overview

This screen acts as an **informative and action-driven landing page** to guide users interested in studying MBBS abroad. It highlights the **benefits of guidance**, builds **trust**, and encourages users to **start their journey** by pressing the "Begin" button.

This screen is positioned under the "Study Abroad" tab in the bottom navigation bar (indicated by a red airplane icon).

---

## 📐 Layout Structure

### ⬆️ 1. Status Bar

* Simulated iOS status bar
* Contains time on left (`9:41`)
* Network/wifi/battery indicators on right

---

### 🟢 2. Header Section

#### 📌 Title:

* **Text**: `Study Abroad`
* **Font Style**: Bold, large (24–28px)
* **Alignment**: Center aligned
* **Color**: Dark teal or black (#005F55 or #111111)
* **Top Margin**: Medium (\~20–24px)
* **Background**: White

#### 🧱 Border Separator:

* Thin gray horizontal line or divider below title

---

### 🧍‍♂️ 3. Hero Graphic Section

#### 🖼️ Illustration:

* Centered 3D illustration of a student sitting on a stack of books with a bulb above his head (symbolizing learning or an idea moment)
* Use `.svg`, `.png`, or Lottie if needed
* Suggested max height: 30–35% of screen height
* Positioned with enough top and bottom padding (16–24px)

---

### 📢 4. Content Block (Informative Text)

#### 🧾 Subtitle:

* **Text**: `Overseas Study Expert`
* **Font Size**: 18–20px
* **Style**: Bold
* **Color**: Dark teal (#00796B)
* **Alignment**: Centered
* **Spacing**: \~16px below illustration

---

#### 📋 Bullet Points:

Each point is clearly displayed for readability.

* **Font Size**: 16px
* **Font Color**: #444444 or dark gray
* **Line Height**: \~1.5x for readability
* **Bullet Style**: Dot (•), indented
* **Left Margin**: Properly indented from screen edge
* **Spacing Between Points**: 8–12px

##### Example Text:

* Planning to study MBBS abroad?
* But unsure which university would be the best-fit for you?
* Devoyage experts will guide on every step in your journey.
* Start with our course finder and schedule a slot with a counsellor.

---

### 🔴 5. Action Button (Call-to-Action)

#### Button:

* **Text**: `Begin`
* **Style**: Centered, rounded corners
* **Color**: Coral red (#FF5E5B)
* **Text Color**: White
* **Font Weight**: Bold
* **Padding**: Horizontal: 32px, Vertical: 14px
* **On Press**: Triggers navigation to **course finder or slot booking screen**
* **Shadow**: Optional soft drop shadow for elevation

---

### 🧭 6. Bottom Navigation Bar

#### Design:

* Stays fixed at bottom of screen
* Contains 5 navigation items:

  1. 👤 Profile icon
  2. 🔷 Home/Feed icon (filled hexagon)
  3. 𝕐 (Y-like brand icon)
  4. 📖 Knowledge hub or Blog
  5. ✈️ **This tab**: Study Abroad

#### Styling:

* **Active Tab**: Highlighted in red with underline or indicator
* **Inactive Tabs**: Gray icons
* **Navigation**: Tappable and navigable with animation

---

## 🔌 Functionalities to Implement

| Feature                      | Behavior                                                             |
| ---------------------------- | -------------------------------------------------------------------- |
| 📲 “Begin” Button            | Opens course finder or a counselor slot-booking screen               |
| 🎯 Dynamic Hero Illustration | Can be swapped with API-driven animation or image from backend       |
| 🔄 Responsive Layout         | Adapts to different screen sizes (mobile, tab)                       |
| 🛠️ Backend Integration      | Later, attach backend API for course finder and counselor listing    |
| 🧪 Testing Notes             | Button must work, illustration should load, text should not overflow |

---

## 🎨 Color & Font Guidelines

| Element         | Color / Font Size | Notes                     |
| --------------- | ----------------- | ------------------------- |
| Title           | #005F55 / 24–28px | Bold, serif or Sans Serif |
| Subtitle        | #00796B / 18–20px | Centered                  |
| Body Text       | #444444 / 16px    | Paragraph style, readable |
| Begin Button    | #FF5E5B / 16px    | White text, bold          |
| Nav Active Icon | #FF5E5B           | Red highlight             |
| Divider Line    | #E0E0E0           | Thin                      |

---

## 🧩 Folder/File Structure (Recommended)

```bash
components/
  └── StudyAbroadScreen.jsx
  └── NavigationBar.jsx
assets/
  └── abroad_illustration.png
  └── icons/
       └── flight.png
       └── user.png
data/
  └── staticContent.json
```

---

## ✅ Acceptance Checklist

* [x] Title and subtitle appear centered and styled correctly
* [x] Hero image loads perfectly on different screens
* [x] All bullet points are visible and well-spaced
* [x] "Begin" button works and is styled boldly
* [x] Bottom navigation shows this tab as active
* [x] UI works responsively and scrolls properly if needed

---

Let me know if you’d like a companion `.json` for dynamic loading of the bullet points or backend mock structure for the “Begin” button action.
