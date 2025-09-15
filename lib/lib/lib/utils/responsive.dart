import 'package:flutter/material.dart';

class Measurements {
  Size screenSize;

  Measurements(this.screenSize);

  double wp(percentage) {
    return percentage / 100 * screenSize.width;
  }

  double hp(percentage) {
    return percentage / 100 * screenSize.height;
  }

  double getWidthPx(int pixels) {
    return (pixels / 3.61) / 100 * screenSize.width;
  }
}

double getWidth(BuildContext context) {
  return MediaQuery.of(context).size.width;
}

double getHeight(BuildContext context) {
  return MediaQuery.of(context).size.height;
}

vGap(double height) {
  return SizedBox(
    height: height,
  );
}

hGap(double width) {
  return SizedBox(width: width);
}
