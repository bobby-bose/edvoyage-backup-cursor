import 'package:flutter/material.dart';

class Topbar extends StatelessWidget {
  final String firstText;
  final String secondText;
  final VoidCallback? onFirstTap;
  final VoidCallback? onSecondTap;

  const Topbar({
    super.key,
    required this.firstText,
    required this.secondText,
    this.onFirstTap,
    this.onSecondTap,
  });

  @override
  Widget build(BuildContext context) {
    // This is the teal color used in your screenshot
    const Color linkColor = Color(0xFF008080);
    const TextStyle linkStyle = TextStyle(
      color: linkColor,
      fontSize: 16,
      fontWeight: FontWeight.w500,
    );
    const TextStyle separatorStyle = TextStyle(
      color: linkColor,
      fontSize: 16,
      fontWeight: FontWeight.w500,
    );

    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16.0, vertical: 8.0),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.center,
        children: [
          // The icon at the beginning
          const Icon(Icons.menu_book, color: linkColor, size: 24),
          const SizedBox(width: 8),

          // The first separator
          const Text(" / ", style: separatorStyle),

          Text(firstText, style: linkStyle),

          // The second separator
          const Text(" / ", style: separatorStyle),

          Text(secondText, style: linkStyle),
        ],
      ),
    );
  }
}
