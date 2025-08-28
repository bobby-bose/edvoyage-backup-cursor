import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:frontend/_env/env.dart';
import 'package:frontend/screens/home_screen/homescreenreplaceable/homeScreen_happysplash.dart';
import 'package:frontend/utils/responsive.dart';
import 'package:frontend/widgets/botttom_nav.dart';
import 'package:frontend/utils/avatar.dart';
import 'package:frontend/utils/colors/colors.dart';
import 'package:frontend/widgets/long_button.dart';
import 'package:frontend/screens/exploreUniversity_screen/exploreUniversitiesScreen.dart';
import 'package:frontend/screens/notification/notification.dart';
import 'MCQQuestionWidget.dart';
import 'happy_splash.dart';
import 'sad_splash.dart';
import 'exhausted _splash.dart';
import 'package:http/http.dart' as http;
import 'package:frontend/utils/session_manager.dart';
import 'package:frontend/screens/login/sign_up.dart';

class HomeData {
  final Map<String, dynamic> questionOfTheDayData;
  final List<dynamic> allNotificationsData;
  final List<dynamic> offerNotificationsData;

  HomeData({
    required this.questionOfTheDayData,
    required this.allNotificationsData,
    required this.offerNotificationsData,
  });
}

class HomeScreen extends StatefulWidget {
  const HomeScreen({super.key});

  @override
  State<HomeScreen> createState() => _HomeScreenState();
}

class _HomeScreenState extends State<HomeScreen> {
  Measurements? size;
  HomeData? homeData;
  int universityLength = 0;
  bool isLoadingUniversityCount = false;
  int coursesLength = 0;
  bool isLoadingCoursesCount = false;

  @override
  void initState() {
    super.initState();
    // Call fetchData when the widget is first created
    fetchData();
    getLengthOfAllUniversities();
    getLengthOfAllCourses();
  }

  // Method to refresh university count (can be called on pull-to-refresh or error)
  Future<void> refreshUniversityCount() async {
    await getLengthOfAllUniversities();
  }

  // Method to refresh courses count (can be called on pull-to-refresh or error)
  Future<void> refreshCoursesCount() async {
    await getLengthOfAllCourses();
  }

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

  Future<void> fetchData() async {
    try {
      var response = await http.get(Uri.parse(BaseUrl.home));

      if (response.statusCode == 200) {
        // Parse the JSON string into a Map
        Map<String, dynamic> responseData = json.decode(response.body);

        // Accessing question_of_the_day data
        Map<String, dynamic> questionOfTheDayData =
            responseData['question_of_the_day'];
        print('Question of the day: $questionOfTheDayData');

        // Accessing all_notifications data
        List<dynamic> allNotificationsData = responseData['all_notifications'];
        print('All Notifications: $allNotificationsData');

        // Accessing offer_notifications data
        List<dynamic> offerNotificationsData =
            responseData['offer_notifications'];
        print('Offer Notifications: $offerNotificationsData');

        // Set homeData with the collected data
        setState(() {
          homeData = HomeData(
            questionOfTheDayData: questionOfTheDayData,
            allNotificationsData: allNotificationsData,
            offerNotificationsData: offerNotificationsData,
          );
        });
      } else {
        print('Failed to load data: ${response.statusCode}');
      }
    } catch (e) {
      // Handle errors here
      print('Error: $e');
    }
  }

  Future<void> _performLogout() async {
    // Clear the stored email
    await SessionManager.clearEmail();

    // Navigate to the SignUp screen
    Navigator.pushReplacement(
      context,
      MaterialPageRoute(builder: (context) => SignUp()),
    );
  }

  @override
  Widget build(BuildContext context) {
    size = Measurements(MediaQuery.of(context).size);
    return WillPopScope(
      onWillPop: () async {
        SystemNavigator.pop();
        return false;
      },
      child: Scaffold(
          bottomNavigationBar: BottomButton(onTap: () {}, selectedIndex: 2),
          backgroundColor: Colors.grey.shade200,
          appBar: AppBar(
            backgroundColor: Colors.white,
            elevation: 0.2,
            automaticallyImplyLeading: false,
            centerTitle: true,
            leading: IconButton(
              icon: Icon(
                Icons.logout,
                color: primaryColor,
              ),
              onPressed: () async {
                // Show confirmation dialog
                bool? shouldLogout = await showDialog<bool>(
                  context: context,
                  builder: (BuildContext context) {
                    return AlertDialog(
                      title: Text('Logout'),
                      content: Text('Are you sure you want to logout?'),
                      actions: [
                        TextButton(
                          onPressed: () => Navigator.of(context).pop(false),
                          child: Text('Cancel'),
                        ),
                        TextButton(
                          onPressed: () => Navigator.of(context).pop(true),
                          child: Text('Logout'),
                        ),
                      ],
                    );
                  },
                );

                if (shouldLogout == true) {
                  // Perform logout
                  await _performLogout();
                }
              },
            ),
            title: SizedBox(
              height: 200, // Set the height of the container
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
          body: SingleChildScrollView(
            scrollDirection: Axis.vertical,
            child: Padding(
                padding: const EdgeInsets.all(8.0),
                child: Column(children: [
                  Center(
                    child: Container(
                      padding: EdgeInsets.only(top: 5),
                      height: size?.hp(30),
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
                                color: primaryColor,
                                fontWeight: FontWeight.bold),
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
                                mainAxisAlignment:
                                    MainAxisAlignment.spaceBetween,
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
                                      child: Image.asset(
                                          'assets/exhaustedB.png',
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
                                    child: SizedBox(
                                      height: size?.hp(10),
                                      width: size?.wp(22),
                                      child: TextButton(
                                        onPressed: () {
                                          Navigator.push(
                                              context,
                                              PageRouteBuilder(
                                                  pageBuilder: (_, __, ___) =>
                                                      HomeScreenhappysplash()));
                                        },
                                        child: Image.asset(
                                          'assets/happy.png',
                                          fit: BoxFit.fill,
                                        ),
                                      ),
                                    ),
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
                                color: primaryColor,
                                fontWeight: FontWeight.bold),
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
                            textScaleFactor: 1.6,
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
          )),
    );
  }
}
