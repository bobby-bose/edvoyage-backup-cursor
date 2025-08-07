import 'dart:async';
import 'package:flutter/material.dart';
import 'package:page_transition/page_transition.dart';
import 'package:frontend/utils/avatar.dart';
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/utils/responsive.dart';
import 'package:frontend/widgets/long_button.dart';
import 'package:frontend/screens/exploreUniversity_screen/exploreUniversitiesScreen.dart';
import 'package:frontend/screens/notification/notification.dart';
import 'package:frontend/screens/home_screen/exhausted _splash.dart';
import 'package:frontend/screens/home_screen/happy_bottom.dart';
import 'package:frontend/screens/home_screen/sad_splash.dart';

class HappySplash extends StatefulWidget {
  const HappySplash({super.key});

  @override
  State<HappySplash> createState() => _HappySplashState();
}

class _HappySplashState extends State<HappySplash> {
  Measurements? size;

  @override
  void initState() {
    super.initState();
    Timer(
        Duration(seconds: 1),
        () => Navigator.push(
            context,
            PageTransition(
                type: PageTransitionType.bottomToTop, child: HappyBottom())));
  }

  @override
  Widget build(BuildContext context) {
    size = Measurements(MediaQuery.of(context).size);
    return Scaffold(
        backgroundColor: vBarBgcolor,
        appBar: AppBar(
          backgroundColor: Colors.white,
          elevation: 0.2,
          automaticallyImplyLeading: false,
          centerTitle: true,
          title: SizedBox(
            height: 250, // Set the width of the container
            width: 200, // Set the height of the container
            child: Image.asset(
                edvoyagelogo1), // Replace with the actual image path
          ),
          actions: [
            IconButton(
                icon: Icon(
                  Icons.notifications,
                  color: primaryColor,
                ),
                onPressed: () {
                  Navigator.push(
                      context,
                      MaterialPageRoute(
                          builder: (context) => NotificationScreen()));
                })
          ],
        ),
        body: Padding(
            padding: const EdgeInsets.all(8.0),
            child: Column(children: [
              Center(
                child: Container(
                  padding: EdgeInsets.only(top: 5),
                  height: size?.hp(26),
                  width: size?.wp(95),
                  decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(30),
                      color: Color.fromRGBO(192, 235, 231, 1),
                      border: Border.all(color: thirdColor, width: 1.5)),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      Text(
                        'How are you feeling today?',
                        style: TextStyle(
                            color: primaryColor, fontWeight: FontWeight.bold),
                      ),
                      Stack(children: [
                        Container(
                          margin: EdgeInsets.only(top: 5),
                          height: size?.hp(15),
                          width: size?.wp(95),
                          child: Image.asset(
                            'assets/curving.png',
                            fit: BoxFit.fill,
                          ),
                        ),
                        Container(
                          margin: EdgeInsets.symmetric(vertical: 20),
                          padding: EdgeInsets.symmetric(horizontal: 15),
                          child: Row(
                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                            children: [
                              SizedBox(
                                height: size?.hp(10),
                                width: size?.wp(17.5),
                                child: TextButton(
                                  onPressed: () {
                                    Navigator.push(
                                        context,
                                        PageRouteBuilder(
                                            pageBuilder: (_, __, ___) =>
                                                ExhuastedSplash()));
                                  },
                                  child: Image.asset('assets/exhaustedB.png',
                                      fit: BoxFit.fill),
                                ),
                              ),
                              Container(
                                height: size?.hp(11),
                                width: size?.wp(25),
                                decoration: BoxDecoration(
                                  color: thirdColor,
                                  shape: BoxShape.circle,
                                ),
                                child: TextButton(
                                    onPressed: () {},
                                    child: Image.asset(
                                      'assets/happy.png',
                                      fit: BoxFit.fill,
                                    )),
                              ),
                              SizedBox(
                                height: size?.hp(10),
                                width: size?.wp(17.5),
                                child: TextButton(
                                    onPressed: () {
                                      Navigator.push(
                                          context,
                                          PageRouteBuilder(
                                              pageBuilder: (_, __, ___) =>
                                                  SadSplash()));
                                    },
                                    child: Image.asset('assets/sadB.png',
                                        fit: BoxFit.fill)),
                              )
                            ],
                          ),
                        )
                      ]),
                      Row(
                        crossAxisAlignment: CrossAxisAlignment.end,
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          Container(
                            margin: EdgeInsets.symmetric(horizontal: 2),
                            height: 10,
                            width: 2,
                            decoration: BoxDecoration(
                                color: primaryColor,
                                borderRadius: BorderRadius.circular(.25)),
                          ),
                          Container(
                            height: 15,
                            width: 3,
                            decoration: BoxDecoration(
                                color: secondaryColor,
                                borderRadius: BorderRadius.circular(.25)),
                          ),
                          Container(
                            margin: EdgeInsets.symmetric(horizontal: 2),
                            height: 10,
                            width: 2,
                            decoration: BoxDecoration(
                                color: primaryColor,
                                borderRadius: BorderRadius.circular(.25)),
                          )
                        ],
                      ),
                      Text(
                        'Happy',
                        style: TextStyle(
                            color: primaryColor, fontWeight: FontWeight.bold),
                      )
                    ],
                  ),
                ),
              ),
              Center(
                child: Container(
                  margin: EdgeInsets.symmetric(vertical: 10),
                  height: size?.hp(30),
                  width: size?.wp(95),
                  decoration: BoxDecoration(
                      color: thirdColor,
                      borderRadius: BorderRadius.circular(10),
                      boxShadow: [
                        BoxShadow(
                            offset: Offset(1, 1),
                            blurRadius: 2,
                            color: grey2,
                            spreadRadius: 2)
                      ]),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                    children: [
                      Text(
                        'Explore Courses & Universities',
                        textScaleFactor: 1.8,
                        style: TextStyle(
                          color: primaryColor,
                          fontWeight: FontWeight.w800,
                        ),
                      ),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceEvenly,
                        children: [
                          Container(
                            height: size?.hp(14),
                            width: size?.wp(42),
                            decoration: BoxDecoration(
                                color: thirdColor,
                                borderRadius: BorderRadius.circular(10),
                                boxShadow: [
                                  BoxShadow(
                                      offset: Offset(0, 0),
                                      spreadRadius: 1,
                                      color: grey2)
                                ]),
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                SizedBox(
                                  height: size?.hp(4.5),
                                  width: size?.wp(9.6),
                                  child: Image.asset(
                                    universityimage,
                                  ),
                                ),
                                Text(
                                  '300+',
                                  textScaleFactor: 1.5,
                                  style: TextStyle(
                                    fontWeight: FontWeight.w900,
                                  ),
                                ),
                                Text(
                                  'Universiteis',
                                  style: TextStyle(
                                    fontWeight: FontWeight.w800,
                                  ),
                                )
                              ],
                            ),
                          ),
                          Container(
                            height: size?.hp(14),
                            width: size?.wp(42),
                            decoration: BoxDecoration(
                                color: thirdColor,
                                borderRadius: BorderRadius.circular(10),
                                boxShadow: [
                                  BoxShadow(
                                      offset: Offset(0, 0),
                                      spreadRadius: 1,
                                      color: grey2)
                                ]),
                            child: Column(
                              mainAxisAlignment: MainAxisAlignment.center,
                              children: [
                                SizedBox(
                                  height: size?.hp(4.5),
                                  width: size?.wp(9.6),
                                  child: Image.asset(
                                    coursesimage,
                                  ),
                                ),
                                Text(
                                  '30,000+',
                                  textScaleFactor: 1.5,
                                  style: TextStyle(
                                    fontWeight: FontWeight.w900,
                                  ),
                                ),
                                Text(
                                  'Courses',
                                  style: TextStyle(
                                    fontWeight: FontWeight.w800,
                                  ),
                                )
                              ],
                            ),
                          )
                        ],
                      ),
                      LongButton(
                          action: () {
                            Navigator.push(
                                context,
                                MaterialPageRoute(
                                    builder: (context) =>
                                        ExploreUniversitiesScreen()));
                          },
                          text: 'Explore Now'),
                    ],
                  ),
                ),
              ),
              Center(
                  child: CircularProgressIndicator(
                color: Cprimary,
                backgroundColor: secondaryColor,
              ))
            ])));
  }
}
