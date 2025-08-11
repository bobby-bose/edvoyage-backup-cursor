import 'package:flutter/material.dart';

import 'one.dart';
import 'three.dart';
import 'two.dart';

class timerstop extends StatelessWidget {
  final VoidCallback startCountdown;

  const timerstop({
    super.key,
    required this.startCountdown, // ✅ Receive it from parent
  });

  @override
  Widget build(BuildContext context) {
    double screenHeight = MediaQuery.of(context).size.height;

    return Scaffold(
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () {
            Navigator.pop(context);
          },
        ),
        title: Image.asset(
          'assets/logo.png',
          height: screenHeight * 0.8,
        ),
        centerTitle: true,
      ),
      body: Container(
        color: Colors.white,
        child: Column(
          children: [
            SizedBox(
              height: screenHeight * 0.1,
              child: TimerWidget(
                start: true,
              ),
            ),
            SizedBox(
              height: screenHeight * 0.60,
              child: two(),
            ),
            SizedBox(
              height: screenHeight * 0.1,
              child: three(
                onStartPressed: startCountdown, // ✅ pass it here
              ),
            ),
          ],
        ),
      ),
    );
  }
}
