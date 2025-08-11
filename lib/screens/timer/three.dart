// import 'package:flutter/material.dart';
// import 'package:frontend/utils/colors/colors.dart';

// class three extends StatefulWidget {
//   const three({super.key});

//   @override
//   State<three> createState() => _threeState();
// }

// class _threeState extends State<three> {
//   @override
//   Widget build(BuildContext context) {
//     var size = MediaQuery.of(context).size;
//     return Scaffold(
//       backgroundColor: White,
//       body: Center(
//         child: ElevatedButton(
//           onPressed: () {
//             // Add your action here
//           },
//           style: ElevatedButton.styleFrom(
//             backgroundColor: primaryColor, // Button background color
//             padding: EdgeInsets.symmetric(
//               vertical: size.height * 0.01, // Vertical padding
//               horizontal: size.width * 0.3, // Horizontal padding
//             ),
//           ),
//           child: Text(
//             'Start',
//             style: TextStyle(
//               color: Colors.white,
//               fontSize: size.width * 0.08, // Responsive font size
//             ),
//           ),
//         ),
//       ),
//     );
//   }
// }

import 'package:flutter/material.dart';
import 'package:frontend/utils/colors/colors.dart';

class three extends StatelessWidget {
  final VoidCallback onStartPressed;

  const three({super.key, required this.onStartPressed});

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;

    return Center(
      child: ElevatedButton(
        onPressed: onStartPressed,
        style: ElevatedButton.styleFrom(
          backgroundColor: primaryColor,
          padding: EdgeInsets.symmetric(
            vertical: size.height * 0.015,
            horizontal: size.width * 0.25,
          ),
        ),
        child: Text(
          'Start',
          style: TextStyle(
            color: Colors.white,
            fontSize: size.width * 0.06,
          ),
        ),
      ),
    );
  }
}
