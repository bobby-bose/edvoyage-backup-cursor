import 'package:flutter/material.dart';

import 'one.dart';
import 'three.dart';
import 'two.dart';

class timerstop extends StatelessWidget {
  const timerstop({super.key});

  @override
  Widget build(BuildContext context) {
    double screenHeight =
        MediaQuery.of(context).size.height; // Get screen height

    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.white, // White background for AppBar
        elevation: 0, // Remove shadow
        leading: IconButton(
          icon: Icon(Icons.arrow_back, color: Colors.black), // Back button
          onPressed: () {
            Navigator.pop(context);
          },
        ),
        title: Image.asset(
          'assets/logo.png', // Your image
          height: screenHeight * 0.8, // Responsive image height
        ),
        centerTitle: true, // Center the image
      ),
      body: Container(
        color: Colors.white, // White background for body
        child: Column(
          children: [
            SizedBox(
              height: screenHeight * 0.1, // 20% height
              child: TimerWidget(),
            ),
            SizedBox(
              height: screenHeight * 0.60, // 60% height
              child: two(),
            ),
            SizedBox(
              height: screenHeight * 0.1, // 20% height
              child: three(),
            ),
          ],
        ),
      ),
    );
  }
}
