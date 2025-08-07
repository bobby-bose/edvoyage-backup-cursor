import 'package:flutter/material.dart';

import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/utils/responsive.dart';

Measurements? size;

class ComingSoon extends StatelessWidget {
  const ComingSoon({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.grey[200], // Light grey background color
      body: Center(
        child: Container(
          margin: EdgeInsets.symmetric(vertical: 270, horizontal: 10),
          padding: EdgeInsets.all(16),
          width: size?.wp(95),
          decoration: BoxDecoration(
            color: Colors.white, // White background color for the box
            borderRadius: BorderRadius.circular(10),
            boxShadow: [
              BoxShadow(
                offset: Offset(1, 1),
                blurRadius: 2,
                color: const Color.fromARGB(
                    255, 210, 204, 204), // Light grey shadow
                spreadRadius: 2,
              ),
            ],
          ),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Text(
                'Get ready!',
                textScaleFactor: 4.0, // Increased font size
                style: TextStyle(
                  fontFamily: 'Roboto',
                  color: primaryColor,
                  fontWeight: FontWeight.bold, // Bold font weight
                ),
              ),
              SizedBox(
                  height: size?.hp(
                      3)), // Added space between "Get ready" and the next text
              SizedBox(
                height: size?.hp(10),
                width: size?.wp(70),
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    Text(
                      "Something really Cool is Coming!!",
                      textScaleFactor: 1.2,
                      style: TextStyle(
                        fontFamily: 'Roboto',
                        // No specific font weight for this text
                      ),
                    ),
                  ],
                ),
              ),
              SizedBox(
                  height:
                      80), // Added space between the inner box and the button
              TextButton(
                onPressed: () {
                  Navigator.pop(context);
                },
                style: TextButton.styleFrom(
                  backgroundColor: Colors.red, // Red background color
                  shape: RoundedRectangleBorder(
                    borderRadius: BorderRadius.circular(10),
                  ),
                ),
                child: SizedBox(
                  width: 90, // Adjust the width to your desired value
                  height: 40,
                  child: Center(
                    child: Text(
                      'Notify Me',
                      style: TextStyle(
                        fontSize: 16,
                        color: Colors.white, // White text color
                        fontWeight: FontWeight.bold, // Bold font weight
                        fontFamily: 'Roboto',
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
