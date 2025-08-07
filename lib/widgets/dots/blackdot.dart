import 'package:flutter/material.dart';
import '../../utils/colors/colors.dart';
import '../../utils/responsive.dart';

class BlackDot extends StatefulWidget {
  const BlackDot({super.key});

  @override
  State<BlackDot> createState() => _BlackDotState();
}

class _BlackDotState extends State<BlackDot> {
  Measurements? size;
  @override
  Widget build(BuildContext context) {
    size = Measurements(MediaQuery.of(context).size);
    return Container(
      height: size?.hp(.5),
      width: size?.wp(1),
      decoration: BoxDecoration(shape: BoxShape.circle, color: fourthColor),
    );
  }
}
