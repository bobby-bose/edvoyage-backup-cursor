import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/utils/avatar.dart';
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/utils/responsive.dart';
import 'package:frontend/widgets/long_button.dart';
import 'package:frontend/screens/exploreUniversity_screen/exploreUniversitiesScreen.dart';
import 'package:frontend/screens/notification/notification.dart';
import 'package:frontend/screens/home_screen/exhausted _splash.dart';
import 'package:frontend/screens/home_screen/happy_splash.dart';
import '../../_env/env.dart';
import 'MCQQuestionWidget.dart';

class SadSplash extends StatefulWidget {
  const SadSplash({super.key});

  @override
  State<SadSplash> createState() => _SadSplashState();
}

class _SadSplashState extends State<SadSplash> {
  Measurements? size;
  int universityLength = 0;
  bool isLoadingUniversityCount = false;
  int coursesLength = 0;
  bool isLoadingCoursesCount = false;

  @override
  void initState() {
    super.initState();
    getLengthOfAllUniversities();
    getLengthOfAllCourses();
    // Timer navigation removed - screen will stay here
    // Timer(
    //     Duration(seconds: 1),
    //     () => Navigator.push(
    //         context,
    //         PageTransition(
    //             type: PageTransitionType.bottomToTop, child: SadBottom())));
  }

  // Method to refresh university count (can be called on pull-to-refresh or error)
  Future<void> refreshUniversityCount() async {
    await getLengthOfAllUniversities();
  }

  // Method to refresh courses count (can be called on pull-to-refresh or error)
  Future<void> refreshCoursesCount() async {
    await getLengthOfAllCourses();
  }

  // GET THE COUNT OF ALL UNIVERSITIES FROM THE API BaseUrl.universityStats;
  // Fetch university count from stats endpoint (more efficient than fetching full list)
  // Returns: {"success": true, "data": {"total_universities": 123, ...}}

  Future<void> getLengthOfAllUniversities() async {
    setState(() {
      isLoadingUniversityCount = true;
    });

    try {
      var response = await http.get(Uri.parse(BaseUrl.universityStats));
      if (response.statusCode == 200) {
        Map<String, dynamic> responseData = json.decode(response.body);
        print("The Response Data is: $responseData");

        if (responseData['success'] == true && responseData['data'] != null) {
          int totalUniversities =
              responseData['data']['total_universities'] ?? 0;
          print('Total Universities Count: $totalUniversities');

          setState(() {
            universityLength = totalUniversities;
            isLoadingUniversityCount = false;
          });
        } else {
          print('Invalid response format or success is false');
          setState(() {
            universityLength = 0;
            isLoadingUniversityCount = false;
          });
        }
      } else {
        print('Failed to load data: ${response.statusCode}');
        setState(() {
          universityLength = 0;
          isLoadingUniversityCount = false;
        });
      }
    } catch (e) {
      print('Error fetching university count: $e');
      setState(() {
        universityLength = 0;
        isLoadingUniversityCount = false;
      });
    }
  }

  // GET THE COUNT OF ALL COURSES FROM THE API BaseUrl.coursesStats;
  // Fetch courses count from stats endpoint (more efficient than fetching full list)
  // Returns: {"success": true, "data": {"total_courses": 123, ...}}

  Future<void> getLengthOfAllCourses() async {
    setState(() {
      isLoadingCoursesCount = true;
    });

    try {
      var response = await http.get(Uri.parse(BaseUrl.coursesStats));
      if (response.statusCode == 200) {
        Map<String, dynamic> responseData = json.decode(response.body);
        print("The Courses Response Data is: $responseData");

        if (responseData['success'] == true && responseData['data'] != null) {
          int totalCourses = responseData['data']['total_courses'] ?? 0;
          print('Total Courses Count: $totalCourses');

          setState(() {
            coursesLength = totalCourses;
            isLoadingCoursesCount = false;
          });
        } else {
          print('Invalid courses response format or success is false');
          setState(() {
            coursesLength = 0;
            isLoadingCoursesCount = false;
          });
        }
      } else {
        print('Failed to load courses data: ${response.statusCode}');
        setState(() {
          coursesLength = 0;
          isLoadingCoursesCount = false;
        });
      }
    } catch (e) {
      print('Error fetching courses count: $e');
      setState(() {
        coursesLength = 0;
        isLoadingCoursesCount = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    size = Measurements(MediaQuery.of(context).size);
    return Scaffold(
      backgroundColor: vBarBgcolor,
      appBar: AppBar(
        leading: IconButton(
          icon: Icon(
            Icons.arrow_back_ios_new,
            color: primaryColor,
            size: size!.hp(3.5), // Slightly larger than default
            weight: 700, // For a little thickness (Flutter 3.7+)
          ),
          onPressed: () {
            Navigator.of(context).pop();
          },
        ),
        backgroundColor: Colors.white,
        elevation: 0.2,
        automaticallyImplyLeading: false,
        centerTitle: true,
        title: SizedBox(
          height: 250, // Set the width of the container
          width: 200, // Set the height of the container
          child:
              Image.asset(edvoyagelogo1), // Replace with the actual image path
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
      body: SingleChildScrollView(
        child: Padding(
            padding: const EdgeInsets.all(8.0),
            child: Column(children: [
              Center(
                child: Container(
                  padding: EdgeInsets.only(top: 5),
                  height: size?.hp(7),
                  width: size?.wp(95),
                  decoration: BoxDecoration(
                      borderRadius: BorderRadius.circular(30),
                      color: Color.fromRGBO(192, 235, 231, 1),
                      border: Border.all(color: thirdColor, width: 1.5)),
                  child: Column(
                    mainAxisAlignment: MainAxisAlignment.spaceAround,
                    children: [
                      Center(
                        child: Container(
                          alignment: Alignment.center,
                          height: size?.hp(4),
                          width: size?.wp(95),
                          decoration: BoxDecoration(
                              color: Color.fromRGBO(192, 235, 231, 1),
                              borderRadius: BorderRadius.circular(25)),
                          child: Text(
                            '"Every setback is a setup for a comeback"',
                            textScaleFactor: 1.2,
                            style: TextStyle(
                                color: primaryColor,
                                fontWeight: FontWeight.bold),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),
              ),
              Center(
                child: Container(
                  margin: EdgeInsets.symmetric(
                      vertical: 5), // Reduced from 10 to 5 to prevent overflow
                  height:
                      size?.hp(30), // Reduced from 30 to 22 to prevent overflow
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
                        textScaleFactor:
                            1.4, // Reduced from 1.8 to 1.4 to prevent overflow
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
                                isLoadingUniversityCount
                                    ? SizedBox(
                                        height: 20,
                                        width: 20,
                                        child: CircularProgressIndicator(
                                          strokeWidth: 2,
                                          valueColor:
                                              AlwaysStoppedAnimation<Color>(
                                                  primaryColor),
                                        ),
                                      )
                                    : Text(
                                        universityLength > 0
                                            ? universityLength.toString()
                                            : '--',
                                        textScaleFactor: 1.5,
                                        style: TextStyle(
                                          fontWeight: FontWeight.w900,
                                          color: universityLength > 0
                                              ? null
                                              : Colors.grey,
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
                                isLoadingCoursesCount
                                    ? SizedBox(
                                        height: 20,
                                        width: 20,
                                        child: CircularProgressIndicator(
                                          strokeWidth: 2,
                                          valueColor:
                                              AlwaysStoppedAnimation<Color>(
                                                  primaryColor),
                                        ),
                                      )
                                    : Text(
                                        coursesLength > 0
                                            ? coursesLength.toString()
                                            : '--',
                                        textScaleFactor: 1.5,
                                        style: TextStyle(
                                          fontWeight: FontWeight.w900,
                                          color: coursesLength > 0
                                              ? null
                                              : Colors.grey,
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
              MCQQuestionWidget(),
            ])),
      ),
    );
  }
}
