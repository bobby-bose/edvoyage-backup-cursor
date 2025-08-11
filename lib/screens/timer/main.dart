// import 'package:flutter/material.dart';

// import 'one.dart';
// import 'three.dart';
// import 'two.dart';

// class timer extends StatelessWidget {
//   const timer({super.key});

//   @override
//   Widget build(BuildContext context) {
//     double screenHeight =
//         MediaQuery.of(context).size.height; // Get screen height

//     return Scaffold(
//       appBar: AppBar(
//         backgroundColor: Colors.white, // White background for AppBar
//         elevation: 0, // Remove shadow
//         leading: IconButton(
//           icon: Icon(Icons.arrow_back, color: Colors.black), // Back button
//           onPressed: () {
//             Navigator.pop(context);
//           },
//         ),
//         title: Image.asset(
//           'assets/logo.png', // Your image
//           height: screenHeight * 0.8, // Responsive image height
//         ),
//         centerTitle: true, // Center the image
//       ),
//       body: Container(
//         color: Colors.white, // White background for body
//         child: Column(
//           children: [
//             SizedBox(
//               height: screenHeight * 0.1, // 20% height
//               child: TimerWidget(
//                 start: true,
//               ),
//             ),
//             SizedBox(
//               height: screenHeight * 0.60, // 60% height
//               child: two(),
//             ),
//             SizedBox(
//               height: screenHeight * 0.1, // 20% height
//               child: three(),
//             ),
//           ],
//         ),
//       ),
//     );
//   }
// }

import 'package:flutter/material.dart';
import 'package:frontend/widgets/botttom_nav.dart';
import 'one.dart';
import 'three.dart';
import 'two.dart';

const _selectedIndex = 4;

class TimerScreen extends StatefulWidget {
  const TimerScreen({super.key});

  @override
  State<TimerScreen> createState() => _TimerScreenState();
}

class _TimerScreenState extends State<TimerScreen> {
  bool startPressed = false;

  void startCountdown() {
    setState(() {
      startPressed = true;
    });
  }

  @override
  Widget build(BuildContext context) {
    final screenHeight = MediaQuery.of(context).size.height;

    return Scaffold(
      bottomNavigationBar:
          BottomButton(onTap: () {}, selectedIndex: _selectedIndex),
      appBar: AppBar(
        backgroundColor: Colors.white,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back, color: Colors.black),
          onPressed: () => Navigator.pop(context),
        ),
        title: Image.asset(
          'assets/logo.png',
          height: screenHeight * 0.06,
        ),
        centerTitle: true,
      ),
      body: Container(
        color: Colors.white,
        child: Column(
          children: [
            Flexible(
              flex: 2,
              child: Center(child: TimerWidget(start: startPressed)),
            ),
            const Flexible(
              flex: 6,
              child: two(),
            ),
            Flexible(
              flex: 2,
              child: three(onStartPressed: startCountdown),
            ),
          ],
        ),
      ),
    );
  }
}
