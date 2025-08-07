import 'package:flutter/material.dart';

class UpgradeCard extends StatelessWidget {
  const UpgradeCard({super.key});

  @override
  Widget build(BuildContext context) {
    // Get screen dimensions
    double screenWidth = MediaQuery.of(context).size.width;
    double screenHeight = MediaQuery.of(context).size.height;

    // Scale factors
    double padding = screenWidth * 0.05;
    double borderRadius = screenWidth * 0.1; // Rounded shape
    double iconSize = screenWidth * 0.10;
    double fontSizeTitle = screenWidth * 0.05;
    double fontSizeBody = screenWidth * 0.035;

    return Container(
      width: screenWidth * 0.8,
      padding: EdgeInsets.symmetric(
          vertical: padding * 0.6, horizontal: padding * 0.8),
      decoration: BoxDecoration(
        color: const Color(0xFF0E7D68), // Dark Teal Background
        borderRadius:
            BorderRadius.circular(borderRadius), // Fully rounded shape
      ),
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          // Circular Logo
          Container(
            padding: EdgeInsets.all(padding * 0.3), // Inner padding
            decoration: BoxDecoration(
              color: const Color(0xFF037E73), // Teal background
              shape: BoxShape.circle,
              border: Border.all(
                color: Colors.white, // White outline
                width: padding * 0.1, // Responsive border width
              ),
            ),
            child: Image.asset(
              'assets/navigationlogo.png',
              width: iconSize,
              height: iconSize,
              fit: BoxFit.cover,
            ),
          ),
          SizedBox(height: padding * 0.4),
          // Title
          Text(
            "Upgrade to PRO",
            style: TextStyle(
              color: Colors.white,
              fontSize: fontSizeTitle,
              fontWeight: FontWeight.bold,
            ),
          ),
          SizedBox(height: padding * 0.3),
          // Description
          Text(
            "Access to all MCQ’s, videos and other future updates for a year with 24/7 support",
            textAlign: TextAlign.center,
            style: TextStyle(
              color: Colors.white,
              fontSize: fontSizeBody,
            ),
          ),
        ],
      ),
    );
  }
}
