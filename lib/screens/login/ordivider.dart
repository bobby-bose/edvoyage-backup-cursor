import 'package:flutter/material.dart';

class OrDivider extends StatelessWidget {
  const OrDivider({super.key});

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double dividerThickness = screenWidth * 0.002; // Responsive thickness
    double dividerWidth = screenWidth * 0.3; // Responsive width

    return Row(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        Expanded(
          child: Divider(
            color: Colors.grey,
            thickness: dividerThickness,
            indent: screenWidth * 0.05, // Left spacing
            endIndent: screenWidth * 0.02, // Space before OR text
          ),
        ),
        Text(
          "OR",
          style: TextStyle(
            fontSize: screenWidth * 0.04, // Responsive text size
            fontWeight: FontWeight.bold,
            color: Colors.black54,
          ),
        ),
        Expanded(
          child: Divider(
            color: Colors.grey,
            thickness: dividerThickness,
            indent: screenWidth * 0.02, // Space after OR text
            endIndent: screenWidth * 0.05, // Right spacing
          ),
        ),
      ],
    );
  }
}
