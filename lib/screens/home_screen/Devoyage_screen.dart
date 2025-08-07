import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';

import '../../utils/avatar.dart';

class DevoyageTab extends StatefulWidget {
  const DevoyageTab({super.key});

  @override
  State<DevoyageTab> createState() => _DevoyageTabState();
}

class _DevoyageTabState extends State<DevoyageTab> {
  // late int activeMeterIndex;
  // final StreamController activeMeterIndexStreamControl =
  //     StreamController.broadcast();
  //
  // Stream get onUpdateActiveIndex => activeMeterIndexStreamControl.stream;

  // void updateExpansionTile() =>
  //     activeMeterIndexStreamControl.sink.add(activeMeterIndex);
  // int? selectedValue1;
  //
  // void onChange1(int value) {
  //   setState(() {
  //     selectedValue1 = value;
  //   });
  // }

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;
    return Scaffold(
        body: SafeArea(
      child: Column(
        children: [
          Container(
            alignment: Alignment.center,
            child: Image.asset(soon),
          ),
          SizedBox(
            height: 20,
          ),

          Text(
            'COMING  SOON!!!!...',
            style: GoogleFonts.jost(
                letterSpacing: 3,
                fontSize: 27,
                fontWeight: FontWeight.w500,
                color: Colors.black),
          ),

          // ReviewSlider(
          //   onChange: onChange1,
          // ),
        ],
      ),
    ));
  }
}
