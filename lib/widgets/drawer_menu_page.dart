import 'package:flutter/material.dart';
import 'package:flutter_svg/svg.dart';
import 'package:flutter_zoom_drawer/flutter_zoom_drawer.dart';

import 'package:get/get.dart';

import 'package:frontend/utils/BottomNavigation/controller.dart';
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/utils/responsive.dart';

class MenuPage extends StatelessWidget {
  const MenuPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 10),
      width: Get.width / 1.6,
      child: GetBuilder<BottomNavigationController>(
        init: BottomNavigationController(),
        initState: (_) {},
        builder: (controller) {
          return Center(
            child: SingleChildScrollView(
              child: Column(
                mainAxisAlignment: MainAxisAlignment.start,
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  vGap(10),
                  IconButton(
                    icon: Icon(
                      Icons.window,
                      color: Cprimary,
                    ),
                    onPressed: () {
                      ZoomDrawer.of(context)!.close();
                    },
                  ),
                  vGap(10),
                  Padding(
                    padding: const EdgeInsets.all(10.0),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        CircleAvatar(
                          radius: 25,
                        ),
                        vGap(10),
                        Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Jane Doe',
                              style: TextStyle(
                                  color: Cprimary, fontWeight: FontWeight.bold),
                            ),
                            vGap(5),
                            Text('Medical Student',
                                style: TextStyle(
                                    color: Colors.black,
                                    fontWeight: FontWeight.bold))
                          ],
                        )
                      ],
                    ),
                  ),
                  Divider(
                    thickness: 1,
                  ),
                  drawerItems(
                      icon: Icons.bookmark,
                      title: "Adoption",
                      onTap: () {
                        ZoomDrawer.of(context)!.close();
                        controller.tabIndex.value = 0;
                        // controller.update();

                        // Get.offNamed("/BottomNavigationController",
                        //     arguments: 0, preventDuplicates: false);
                      }),
                  drawerItems(
                      icon: Icons.settings,
                      title: "Donation",
                      onTap: () {
                        // ZoomDrawer.of(context)!.close();
                        // Get.toNamed(RoutesName.dashboardPage);
                      }),
                  Divider(
                    thickness: 1,
                  ),
                  drawerItems(
                      icon: Icons.mail,
                      title: "Add pet",
                      onTap: () {
                        // ZoomDrawer.of(context)!.close();
                        // Get.toNamed(RoutesName.allCoursesPage);
                      }),
                  drawerItems(
                    icon: Icons.terminal,
                    title: "Fevorite",
                    onTap: () {},
                  ),
                  drawerItems(
                    icon: Icons.rate_review,
                    title: "Message",
                    onTap: () {
                      ZoomDrawer.of(context)!.close();
                      controller.tabIndex.value = 3;
                    },
                    // onTap: () => Get.offNamed("/BottomNavigationController",
                    //     arguments: 3, preventDuplicates: false),
                  ),
                  drawerItems(
                    icon: Icons.share,
                    title: "Profile",
                    onTap: () {
                      // ZoomDrawer.of(context)!.close();
                      // Get.toNamed(RoutesName.financialPage);
                    },
                  ),
                  drawerItems(
                    icon: Icons.support,
                    title: "Add pet",
                    onTap: () {
                      // ZoomDrawer.of(context)!.close();
                      // Get.toNamed(RoutesName.subscriptionPage);
                    },
                  ),
                  Divider(
                    thickness: 1,
                  ),
                  drawerItems(
                    icon: Icons.bookmark,
                    title: "Add pet",
                    onTap: () {
                      // ZoomDrawer.of(context)!.close();
                      // Get.toNamed(RoutesName.subscriptionPage);
                    },
                  ),
                  Container(
                    padding: EdgeInsets.only(left: 10),
                    height: getHeight(context) / 5.5,
                    width: getWidth(context) / 2,
                    child: Stack(children: [
                      Container(
                        margin: EdgeInsets.only(top: 25),
                        padding: EdgeInsets.all(10),
                        // height: getHeight(context) / 6.5,
                        decoration: BoxDecoration(
                          color: Cprimary,
                          borderRadius: BorderRadius.circular(16.0),
                        ),
                        child: Column(
                          children: [
                            vGap(10),
                            Text("Data",
                                style: TextStyle(
                                    color: White,
                                    fontWeight: FontWeight.w400,
                                    fontSize: 16)),
                            Expanded(
                              child: Text(
                                  "datadatadatadatadatadatadatadtadatadatadatadtadatadtadatadatadatadtadatadatadatadtadatadatadatadtadatadatadatadatadatadatadata",
                                  textAlign: TextAlign.center,
                                  style: TextStyle(
                                      color: White,
                                      fontWeight: FontWeight.w400,
                                      fontSize: 14)),
                            ),
                          ],
                        ),
                      ),
                      Align(
                          alignment: Alignment.topCenter,
                          child: SizedBox(
                            child: CircleAvatar(
                              backgroundColor: White,
                              radius: 20,
                              child: CircleAvatar(
                                radius: 18.0,
                                backgroundColor: Cprimary,
                                child: Text("Y"),
                              ),
                            ),
                          )),
                    ]),
                  ),
                  vGap(10),
                  Text(
                    'Version 1.1',
                    style:
                        TextStyle(color: Cprimary, fontWeight: FontWeight.bold),
                  )
                ],
              ),
            ),
          );
        },
      ),
    );
  }

  Widget drawerItems(
      {String? svg,
      required String title,
      void Function()? onTap,
      IconData? icon,
      double? hight}) {
    return Padding(
      padding: const EdgeInsets.all(10),
      child: InkWell(
        onTap: onTap,
        child: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            svg == null
                ? Container()
                : SvgPicture.asset(
                    svg,
                    color: Cprimary,
                    height: hight ?? 25,
                  ),
            icon == null
                ? Container()
                : Icon(
                    icon,
                    color: Cprimary,
                    size: 26,
                  ),
            const SizedBox(width: 20),
            Expanded(
              child: Text(
                title,
                style: TextStyle(
                    color: Cprimary, fontSize: 17, fontWeight: FontWeight.w900),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
