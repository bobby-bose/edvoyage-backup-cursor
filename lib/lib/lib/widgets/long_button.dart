import 'package:flutter/material.dart';

import 'package:notes/utils/colors/colors.dart';
import 'package:notes/utils/responsive.dart';

class LongButton extends StatelessWidget {
  late String text;
  late Function() action;

  LongButton({super.key, required this.action, required this.text});

  Measurements? size;
  @override
  Widget build(BuildContext context) {
    size = Measurements(MediaQuery.of(context).size);
    return Padding(
      padding: const EdgeInsets.all(8.0),
      child: Container(
        width: size?.wp(87),
        height: size?.hp(5),
        decoration: BoxDecoration(
          color: secondaryColor,
          borderRadius: BorderRadius.circular(10),
        ),
        child: TextButton(
          onPressed: action,
          child: Text(
            text,
            textScaleFactor: 1.25,
            style: TextStyle(
              fontFamily: 'Roboto',
              color: thirdColor,
              fontWeight: FontWeight.w700,
            ),
          ),
        ),
      ),
    );
  }
}
