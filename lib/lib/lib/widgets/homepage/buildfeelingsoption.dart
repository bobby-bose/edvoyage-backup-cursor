import 'package:flutter/material.dart';
import 'package:notes/utils/responsive.dart';

Widget buildFeelingOptions(BuildContext context) {
  Measurements? size;
  size = Measurements(MediaQuery.of(context).size);
  return Stack(
    children: [
      Container(
        margin: const EdgeInsets.only(top: 5),
        height: size.hp(15),
        width: size.wp(95),
        child: Image.asset('assets/curving.png', fit: BoxFit.fill),
      ),
      Container(
        margin: EdgeInsets.symmetric(vertical: 20),
        padding: EdgeInsets.symmetric(horizontal: 15),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            buildFeelingOptionButton('assets/exhaustedB.png', () {
              // navigateToScreen(ExhaustedSplash());
            }),
            buildFeelingOptionButton('assets/happy.png', () {
              navigateToScreen(HappySplash());
            }),
            buildFeelingOptionButton('assets/sadB.png', () {
              navigateToScreen(SadSplash());
            }),
          ],
        ),
      ),
    ],
  );
}

class HappySplash {}

class SadSplash {}

void navigateToScreen(dynamic screen) {}

Widget buildFeelingOptionButton(String assetPath, Function onPressed) {
  return Container();
}
