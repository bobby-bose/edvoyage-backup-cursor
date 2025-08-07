import 'package:flutter/material.dart';

import 'package:frontend/screens/exploreUniversity_screen/exploreUniversitiesScreen.dart';
import '../long_button.dart';
import 'buildFeelingsOption.dart';
import 'explorecoursescontent.dart'; // Import the necessary packages.

Widget buildExploreCoursesContainer(BuildContext context) {
  final Size size =
      MediaQuery.of(context).size; // Define the missing variable 'size'.
  const Color thirdColor = Colors.blue; // Replace 'final' with 'const'.
  const Color grey2 = Colors.grey; // Replace 'final' with 'const'.
  const Color primaryColor = Colors.black; // Replace 'final' with 'const'.

  return Center(
    child: Container(
      margin:
          EdgeInsets.symmetric(vertical: 10), // Import the 'EdgeInsets' class.
      height: size.height *
          0.3, // Correct the variable name 'size' and use the appropriate property.
      width: size.width *
          0.95, // Correct the variable name 'size' and use the appropriate property.
      decoration: BoxDecoration(
        color: thirdColor,
        borderRadius:
            BorderRadius.circular(10), // Import the 'BorderRadius' class.
        boxShadow: [
          BoxShadow(
            offset: Offset(1, 1), // Import the 'Offset' class.
            blurRadius: 2,
            color: grey2,
            spreadRadius: 2,
          ),
        ],
      ),
      child: Column(
        mainAxisAlignment: MainAxisAlignment
            .spaceEvenly, // Import the 'MainAxisAlignment' class.
        children: [
          const Text(
            'Explore Courses & Universities',
            textScaleFactor: 1.6,
            style: TextStyle(
              color: primaryColor,
              fontWeight: FontWeight.w800, // Import the 'FontWeight' class.
            ),
          ),
          buildExploreCoursesContent(), // Define the missing function 'buildExploreCoursesContent'.
          LongButton(
            action: () {
              navigateToScreen(
                  ExploreUniversitiesScreen()); // Define the missing function 'navigateToScreen' and class 'ExploreCourses'.
            },
            text: 'Explore Now',
          ),
        ],
      ),
    ),
  );
}
