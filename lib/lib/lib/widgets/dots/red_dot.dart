import 'package:flutter/material.dart';
import '../../utils/colors/colors.dart';
import '../../utils/responsive.dart';

class RedDot extends StatefulWidget {
  const RedDot({super.key});

  @override
  State<RedDot> createState() => _RedDotState();
}

class _RedDotState extends State<RedDot> {
  Measurements? size;
  @override
  Widget build(BuildContext context) {
    size = Measurements(MediaQuery.of(context).size);
    return Container(
      height: size?.hp(1),
      width: size?.wp(13),
      decoration: BoxDecoration(
        color: secondaryColor,
        borderRadius: BorderRadius.circular(12),
      ),
    );
  }
}
