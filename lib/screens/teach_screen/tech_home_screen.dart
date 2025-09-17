import 'package:flutter/material.dart';

import 'package:flutter/services.dart';
import '../../utils/colors/colors.dart';
import '../../utils/responsive.dart';

class TeachHome extends StatefulWidget {
  const TeachHome({super.key});

  @override
  State<TeachHome> createState() => _TeachHomeState();
}

class _TeachHomeState extends State<TeachHome> {
  Measurements? size;
  @override
  Widget build(BuildContext context) {
    size = Measurements(MediaQuery.of(context).size);
    return PopScope(
      canPop: false,
      onPopInvokedWithResult: (didPop, result) {
        if (!didPop) {
          SystemNavigator.pop(); // exit the app
        }
      },
      child: SafeArea(
        child: Scaffold(
          backgroundColor: grey1,
          appBar: AppBar(
            automaticallyImplyLeading: false,
            backgroundColor: thirdColor,
            elevation: .6,
            title: RichText(
              text: TextSpan(
                children: <TextSpan>[
                  TextSpan(
                      text: 'edvo',
                      style: TextStyle(
                          fontFamily: 'Roboto',
                          letterSpacing: 1,
                          fontWeight: FontWeight.bold,
                          fontSize: 26,
                          color: primaryColor)),
                  TextSpan(
                      text: 'y',
                      style: TextStyle(
                          fontFamily: 'Roboto',
                          fontWeight: FontWeight.bold,
                          fontSize: 26,
                          color: secondaryColor)),
                  TextSpan(
                      text: 'age',
                      style: TextStyle(
                          fontFamily: 'Roboto',
                          letterSpacing: 1,
                          fontWeight: FontWeight.bold,
                          fontSize: 26,
                          color: primaryColor)),
                ],
              ),
            ),
          ),
          body: SingleChildScrollView(
            child: Column(
              children: [
                Container(
                  padding: EdgeInsets.only(left: 15.5, top: 2.5),
                  width: double.infinity,
                  height: size?.hp(5),
                  color: thirdColor,
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      Icon(
                        Icons.menu_book_outlined,
                        color: primaryColor,
                        size: 25,
                      ),
                      IconButton(
                        icon: Icon(
                          Icons.notifications,
                          color: Cprimary,
                        ),
                        onPressed: () {},
                      ),
                    ],
                  ),
                ),
                Container(
                    height: size?.hp(78),
                    width: double.infinity,
                    padding: EdgeInsets.symmetric(horizontal: 10),
                    child: ListView(
                      children: [
                        SizedBox(
                          height: size?.wp(1.5),
                        ),
                        SizedBox(
                          height: size?.wp(2),
                        ),
                      ],
                    )),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
