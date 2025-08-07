import 'package:flutter/material.dart';

Widget buildFeelingOptionButton(
    BuildContext context, String imagePath, VoidCallback onPressed) {
  return SizedBox(
    height: MediaQuery.of(context).size.height * 0.1,
    width: MediaQuery.of(context).size.width * 0.175,
    child: TextButton(
      onPressed: onPressed,
      child: Image.asset(imagePath, fit: BoxFit.fill),
    ),
  );
}
