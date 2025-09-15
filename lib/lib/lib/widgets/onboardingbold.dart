import 'package:flutter/material.dart';
import 'package:notes/utils/colors/colors.dart';
import 'package:notes/utils/responsive.dart';

class BoldText extends StatelessWidget {
  late String text;

  BoldText({super.key, required this.text});

  @override
  Widget build(BuildContext context) {
    Measurements? size;
    return Container(
      height: size?.hp(3),
      width: size?.wp(70),
      alignment: Alignment.center,
      child: Text(
        text,
        textScaleFactor: 1.7,
        style: TextStyle(
          fontFamily: 'Roboto',
          color: primaryColor,
          fontWeight: FontWeight.w700,
        ),
      ),
    );
  }
}

class LateBold extends StatelessWidget {
  late String text;

  LateBold({super.key, required this.text});

  @override
  Widget build(BuildContext context) {
    return Text(
      text,
      textScaleFactor: 1.25,
      textAlign: TextAlign.center,
      style: TextStyle(
        fontFamily: 'Roboto',
        color: grey3,
        fontWeight: FontWeight.w400,
      ),
    );
  }
}
