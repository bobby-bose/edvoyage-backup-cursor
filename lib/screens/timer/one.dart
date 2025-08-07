import 'package:flutter/material.dart';
import 'package:lucide_icons/lucide_icons.dart';

class TimerWidget extends StatelessWidget {
  const TimerWidget({super.key});

  @override
  Widget build(BuildContext context) {
    final double screenWidth = MediaQuery.of(context).size.width;
    final double screenHeight = MediaQuery.of(context).size.height;

    return Container(
      width: screenWidth * 0.5,
      height: screenHeight * 0.02,
      padding: EdgeInsets.symmetric(horizontal: screenWidth * 0.001),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Icon(LucideIcons.arrowDown, size: screenWidth * 0.08),
          Text(
            '00:10:00',
            style: TextStyle(
              fontSize: screenWidth * 0.06,
              fontWeight: FontWeight.bold,
            ),
          ),
          Icon(LucideIcons.arrowUp, size: screenWidth * 0.08),
        ],
      ),
    );
  }
}
