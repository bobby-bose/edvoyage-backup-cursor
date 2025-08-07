import 'package:flutter/material.dart';

class GoogleAuthButton extends StatelessWidget {
  const GoogleAuthButton({super.key});

  @override
  Widget build(BuildContext context) {
    double screenWidth = MediaQuery.of(context).size.width;
    double buttonHeight = screenWidth * 0.13;
    double iconSize = screenWidth * 0.1;
    double fontSize = screenWidth * 0.045;
    double padding = screenWidth * 0.02;

    return ElevatedButton(
      style: ElevatedButton.styleFrom(
        backgroundColor: Color(0xFFE6F6F5), // Background color
        shape: RoundedRectangleBorder(
          borderRadius: BorderRadius.circular(
              screenWidth * 0.03), // Responsive rounded corners
          side: const BorderSide(color: Colors.grey), // Border color
        ),
        // Internal padding
      ),
      onPressed: () {
        // Handle Google authentication here
      },
      child: Container(
        width: double.infinity, // Ensures full width
        padding:
            EdgeInsets.symmetric(vertical: padding), // Adds vertical padding
        color: const Color(0xFFE6F6F5), // Background color

        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Image.asset(
              'assets/google_icon.jpg', // Replace with your Google icon asset
              width: iconSize,
              height: iconSize,
            ),
            SizedBox(width: padding * 0.5), // Space between icon and text
            Text(
              "Login with Google",
              style: TextStyle(
                fontSize: fontSize,
                color: Colors.black87,
                fontWeight: FontWeight.w500,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
