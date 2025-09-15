import 'package:flutter/material.dart';

Widget buildCourseCountContainer(
    String image, String count, String label, BuildContext context) {
  final Size size = MediaQuery.of(context).size;
  final Color thirdColor = const Color(0xFF0000FF);
  final Color grey2 = const Color(0xFF808080);
  final BorderRadius borderRadius = BorderRadius.circular(10);

  return Container(
    height: size.height * 0.14,
    width: size.width * 0.42,
    decoration: BoxDecoration(
      color: thirdColor,
      borderRadius: borderRadius,
      boxShadow: [
        BoxShadow(
          offset: Offset(0, 0),
          spreadRadius: 1,
          color: grey2,
        ),
      ],
    ),
    child: Column(
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        SizedBox(
          height: size.height * 0.045,
          width: size.width * 0.096,
          child: Image.asset(image),
        ),
        Text(
          count,
          textScaleFactor: 1.5,
          style: TextStyle(
            fontWeight: FontWeight.w900,
          ),
        ),
        Text(
          label,
          style: TextStyle(
            fontWeight: FontWeight.w800,
          ),
        ),
      ],
    ),
  );
}
