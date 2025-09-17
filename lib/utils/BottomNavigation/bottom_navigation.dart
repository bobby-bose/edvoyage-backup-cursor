import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:frontend/screens/home_screen/homeScreen.dart';
import 'package:frontend/screens/notes/videonotes/main.dart';
import 'package:frontend/screens/profile/profile_Screen.dart';
import 'package:frontend/widgets/drawer_menu_page.dart';
import 'package:get/get.dart';
import 'package:flutter_zoom_drawer/flutter_zoom_drawer.dart';
import 'package:frontend/screens/cavity_screen/main.dart';
import 'package:frontend/utils/colors/colors.dart';
import 'controller.dart';

BottomNavigationController controller = Get.put(BottomNavigationController());

class BottomNavigation extends StatefulWidget {
  const BottomNavigation({super.key});

  @override
  State<BottomNavigation> createState() => _BottomNavigationState();
}

class _BottomNavigationState extends State<BottomNavigation> {
  final TextEditingController nameController = TextEditingController();
  final List<Widget> _children = [
    ProfileScreen(),
    CavityScreen(),
    HomeScreen(),
    VideoSubjectScreen(),
  ];

  int selectedIndex = 2;

  double xOffset = 0;
  double yOffset = 0;
  double scaleFactor = 1;

  bool isDrawerOpen = false;

  @override
  Widget build(BuildContext context) {
    final labelTextStyle = Theme.of(context)
        .textTheme
        .titleSmall!
        .copyWith(fontFamily: 'Roboto', fontSize: 8.0);

    return Obx(() {
      return ZoomDrawer(
        menuBackgroundColor: Colors.white,
        borderRadius: 24.0,
        showShadow: true,
        angle: 0.0,
        boxShadow: const [BoxShadow(blurRadius: 5)],
        drawerShadowsBackgroundColor: Colors.white,
        slideWidth: MediaQuery.of(context).size.width * 0.69,
        duration: .5.seconds,
        reverseDuration: .5.seconds,
        menuScreen: const MenuPage(),
        mainScreen: Scaffold(
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
              items: [
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
        ),
      );
    });
  }

  Future<bool> onexit() async {
    return await showDialog(
      barrierDismissible: false,
      context: Get.context!,
      builder: (BuildContext context) {
        return Dialog(
          shape: const RoundedRectangleBorder(
              borderRadius: BorderRadius.all(Radius.circular(5.0))),
          child: Container(
            margin: const EdgeInsets.only(top: 25, left: 15, right: 15),
            height: 100,
            child: Column(
              children: <Widget>[
                const Text("Are you sure you want to exit?"),
                Container(
                  margin: const EdgeInsets.only(top: 22),
                  child: Row(
                    crossAxisAlignment: CrossAxisAlignment.center,
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: <Widget>[
                      InkWell(
                        onTap: () {
                          Get.back(result: false);
                        },
                        child: Container(
                          width: 100,
                          height: 40,
                          alignment: Alignment.center,
                          padding: const EdgeInsets.symmetric(
                              horizontal: 20, vertical: 6),
                          decoration: BoxDecoration(
                            boxShadow: [
                              BoxShadow(
                                  color: Colors.blue.withValues(alpha: 0.1),
                                  offset: const Offset(0.0, 1.0),
                                  blurRadius: 1.0,
                                  spreadRadius: 0.0)
                            ],
                            color: ColorConst.buttonColor,
                            borderRadius: BorderRadius.circular(5),
                          ),
                          child: Text(
                            "No",
                            style: TextStyle(
                                fontFamily: 'Roboto', color: Colors.white),
                          ),
                        ),
                      ),
                      InkWell(
                        onTap: () {
                          SystemChannels.platform
                              .invokeMethod('SystemNavigator.pop');
                        },
                        child: Container(
                          width: 100,
                          height: 40,
                          alignment: Alignment.center,
                          padding: const EdgeInsets.symmetric(
                              horizontal: 20, vertical: 6),
                          decoration: BoxDecoration(
                            boxShadow: [
                              BoxShadow(
                                  color: Colors.blue.withValues(alpha: 0.1),
                                  offset: const Offset(0.0, 1.0),
                                  blurRadius: 1.0,
                                  spreadRadius: 0.0)
                            ],
                            color: ColorConst.buttonColor,
                            borderRadius: BorderRadius.circular(5),
                          ),
                          child: Text("Yes",
                              style: TextStyle(
                                  fontFamily: 'Roboto', color: Colors.white)),
                        ),
                      ),
                    ],
                  ),
                )
              ],
            ),
          ),
        );
      },
    );
  }
}
