import 'package:flutter/material.dart';

Widget buildDivider() {
  final primaryColor = Colors.blue; // Define the missing variable primaryColor
  final EdgeInsets margin = EdgeInsets.symmetric(
      horizontal: 2); // Define the missing variable EdgeInsets
  final BorderRadius borderRadius =
      BorderRadius.circular(.25); // Define the missing variable BorderRadius

  return Container(
    margin: margin,
    height: 10,
    width: 2,
    decoration: BoxDecoration(
      color: primaryColor,
      borderRadius: borderRadius,
    ),
  );
}
