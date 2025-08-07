import 'package:flutter/material.dart';

Color primaryColor = const Color.fromRGBO(3, 126, 115, 1);
Color secondaryColor = const Color.fromRGBO(255, 99, 97, 1);
Color thirdColor = Colors.white;
Color fourthColor = Colors.black;
Color darkblack = Color(0xFF121212);
Color grey1 = Colors.grey.shade300;
Color grey2 = Color(0xFFD0D0D0);
Color grey3 = Colors.grey.shade700;
Color grey4 = Color(0xFFEAE6E6);

const offerColor = Color(0xFF1CBCAE);
const tsecondary = Color(0xFFffd022);
const ttext = Color(0xFF504E4F);
const ttext2 = Color(0xFF696768);
const Cprimary = Color.fromARGB(255, 35, 98, 95);
const Cbottom = Color(0xFFFFCE1A);
const White = Color(0xFFFFFFFF);
const Ctext2 = Color(0xFFF8F8FA);
const cdtext = Color(0xFF2A353A);
const VIPtext = Color(0xFFD61340);
const Cbg = Color(0xFFFCF0F0);
const cbg2 = Color(0xFFF1AEBB);
const cbg3 = Color(0xFFF28D03);
const cbg4 = Color(0xFFFFECD3);
const subtext = Color(0xFF667781);
const titlecolor = Color.fromARGB(255, 88, 94, 100);
const call = Color(0xFF00AF9B);
const music = Color(0xFF69A9F1);
const eye = Color(0xFF5E7E95);
const oncall = Color(0xFF32965A);
const addcontact = Color(0xFF7881FF);
const play = Color(0xFFE3E8EB);
const textColor = Color(0xFF9B9B9B);
const contr1 = Color(0xFF27B9D8);
const contr2 = Color(0xFF7882FE);
const contr3 = Color(0xFFF18072);
const borderclr = Color(0xFF149791);
const paichat = Color(0xFFEDF6F6);
const cgreen = Color(0xFF34C650);
const cblack10 = Color(0xFFEFEFEF);
const text5 = Color(0XFF575757);
const cdivider = Color(0xFF85959F);
const iconcolor = Color.fromARGB(255, 41, 32, 32);

final color3 = Color(0xFFF0F0F0);

final BodyColor = Color(0xffbacffffff);
final backgroundColor = Color(0xffb1e1e1e);
final containerBackgroundColor2 = Color(0xff000000);
final approvedLeavesColor = Color(0xff26C60C);
final whiteColor = Color(0xffFFFFFF);
final bodyColor = Color(0x1FEFA7A7);
final vBarBgcolor = Color(0xFFF6F6F6);
final vBarcolor1 = Color(0xFFC1AEF1);
final vBarcolor2 = Color(0xFFFE8B88);
final vBarcolor3 = Color(0xFF48CCFF);

class ColorConst {
  static Color border = const Color(0xFFEEEEEE);
  static Color primaryColor = const Color(0xFF1564C0);
  static Color buttonColor = const Color(0xFF1564C0);
  static Color greyTextColor = const Color(0xFF9E9E9E);
  static Color errorColor = Colors.red;
  static Color greenColor = const Color(0xff4CBB17);
  static Color scafoldColor = Colors.grey[200]!.withOpacity(.5);
}

extension HexColor on Color {
  static Color fromHex(String hexString) {
    final buffer = StringBuffer();
    if (hexString.length == 6 || hexString.length == 7) buffer.write('ff');
    buffer.write(hexString.replaceFirst('#', ''));
    return Color(int.parse(buffer.toString(), radix: 16));
  }

  String toHex({bool leadingHashSign = true}) => '${leadingHashSign ? '#' : ''}'
      '${alpha.toRadixString(16).padLeft(2, '0')}'
      '${red.toRadixString(16).padLeft(2, '0')}'
      '${green.toRadixString(16).padLeft(2, '0')}'
      '${blue.toRadixString(16).padLeft(2, '0')}';
}
