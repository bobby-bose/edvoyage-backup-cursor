import 'package:flutter/material.dart';
import 'package:notes/utils/avatar.dart';

class BackgroundImage extends StatefulWidget {
  const BackgroundImage({super.key});

  @override
  State<BackgroundImage> createState() => _BackgroundImageState();
}

class _BackgroundImageState extends State<BackgroundImage> {
  @override
  Widget build(BuildContext context) {
    return SizedBox(
      height: double.infinity,
      child: Image.asset(
        background,
        fit: BoxFit.fitWidth,
        width: double.infinity,
        height: double.infinity,
      ),
    );
  }
}
