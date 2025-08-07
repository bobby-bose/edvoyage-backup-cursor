import 'package:flutter/material.dart';
import 'package:frontend/utils/colors/colors.dart';

class three extends StatefulWidget {
  const three({super.key});

  @override
  State<three> createState() => _threeState();
}

class _threeState extends State<three> {
  @override
  Widget build(BuildContext context) {
    var size = MediaQuery.of(context).size;
    return Scaffold(
      backgroundColor: White,
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            // Add your action here
          },
          style: ElevatedButton.styleFrom(
            backgroundColor: secondaryColor, // Button background color
            padding: EdgeInsets.symmetric(
              vertical: size.height * 0.01, // Vertical padding
              horizontal: size.width * 0.3, // Horizontal padding
            ),
          ),
          child: Text(
            'Stop',
            style: TextStyle(
              color: Colors.white,
              fontSize: size.width * 0.08, // Responsive font size
            ),
          ),
        ),
      ),
    );
  }
}
