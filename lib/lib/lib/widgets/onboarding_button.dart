import 'package:flutter/material.dart';
import 'package:notes/utils/colors/colors.dart';
import 'package:notes/utils/responsive.dart';

class OnboardingButton extends StatelessWidget {
  late Function() action;

  OnboardingButton({super.key, required this.action});

  Measurements? size;
  @override
  Widget build(BuildContext context) {
    size = Measurements(MediaQuery.of(context).size);
    return SizedBox(
      width: size?.wp(15),
      height: size?.hp(10),
      child: ElevatedButton(
        style: ButtonStyle(
          shape: WidgetStateProperty.all(CircleBorder()),
          backgroundColor: WidgetStateProperty.all(secondaryColor),
        ),
        onPressed: action,
        child: Container(
          height: size?.hp(5),
          width: size?.wp(13),
          decoration: BoxDecoration(color: thirdColor, shape: BoxShape.circle),
          child: Icon(Icons.arrow_forward_ios_rounded, color: primaryColor),
        ),
      ),
    );
  }
}
