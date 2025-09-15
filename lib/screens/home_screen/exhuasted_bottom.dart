import 'package:flutter/material.dart';

import 'package:frontend/screens/home_screen/homeScreen.dart';
import 'package:frontend/screens/notes/notes.dart';
import 'package:frontend/screens/notes/videonotes/video_player.dart';
import 'package:get/get.dart';

import 'package:frontend/utils/BottomNavigation/bottom_navigation.dart';
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/screens/comingsoon.dart';
import 'package:frontend/screens/profile/profile_Screen.dart';
import 'package:frontend/screens/Notes/main.dart';

class ExhaustedBottom extends StatefulWidget {
  const ExhaustedBottom({super.key});

  @override
  State<ExhaustedBottom> createState() => _ExhaustedBottomState();
}

class _ExhaustedBottomState extends State<ExhaustedBottom> {
  final List<Widget> _children = [
    ProfileScreen(),
    ComingSoon(),
    HomeScreen(),
    VideoSubjectScreen(),
  ];

  int selectedIndex =
      0; // Changed from 2 to 0 to show ProfileScreen instead of HomeScreen

  double xOffset = 0;
  double yOffset = 0;
  double scaleFactor = 1;
  @override
  Widget build(BuildContext context) {
    final labelTextStyle = Theme.of(context)
        .textTheme
        .titleSmall!
        .copyWith(fontFamily: 'Roboto', fontSize: 8.0);

    return Obx(() {
      int index = controller.tabIndex.toInt();
      return Scaffold(
        backgroundColor: Color(0xFFEFEFEF),
        body: _children[selectedIndex],
        bottomNavigationBar: SizedBox(
          height: 50.0,
          child: BottomNavigationBar(
            type: BottomNavigationBarType.fixed,
            selectedItemColor: secondaryColor,
            unselectedItemColor: primaryColor,
            currentIndex: selectedIndex,
            showSelectedLabels: false,
            showUnselectedLabels: false,
            selectedLabelStyle: labelTextStyle,
            unselectedLabelStyle: labelTextStyle,
            onTap: (index) {
              setState(() {
                selectedIndex = index;
              });
            },
            items: const [
              BottomNavigationBarItem(
                icon: ImageIcon(AssetImage("assets/frame.png")),
                label: 'Home',
              ),
              BottomNavigationBarItem(
                icon: ImageIcon(AssetImage("assets/diamonds.png")),
                label: 'SEARCH',
              ),
              BottomNavigationBarItem(
                icon: ImageIcon(AssetImage("assets/Group 98.png")),
                label: 'CART',
              ),
              BottomNavigationBarItem(
                icon: ImageIcon(AssetImage("assets/book.png")),
                label: 'ACCOUNT',
              ),
            ],
          ),
        ),
      );
    });
  }
}
