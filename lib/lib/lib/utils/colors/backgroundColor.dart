import 'package:flutter/material.dart';
import 'colors.dart';

class BackgroundColor extends StatelessWidget {
  const BackgroundColor({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      height: double.infinity,
      color: primaryColor,
    );
  }
}
