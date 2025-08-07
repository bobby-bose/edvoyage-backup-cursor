import 'package:flutter/material.dart';
import '../../utils/colors/colors.dart';
import '../../utils/responsive.dart';

class GreyDot extends StatefulWidget {
  const GreyDot({super.key});

  @override
  State<GreyDot> createState() => _GreyDotState();
}

class _GreyDotState extends State<GreyDot> {
  Measurements? size;
  @override
  Widget build(BuildContext context) {
    size = Measurements(MediaQuery.of(context).size);
    return Container(
      height: size?.hp(1),
      width: size?.wp(1.5),
      decoration: BoxDecoration(color: grey2, shape: BoxShape.circle),
    );
  }
}
